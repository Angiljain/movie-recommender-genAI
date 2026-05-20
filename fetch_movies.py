import urllib.request
import json
import csv
import os
import sys
import time
from dotenv import load_dotenv

# Force unbuffered stdout so progress is visible in real time on Windows
sys.stdout.reconfigure(line_buffering=True)

# Load environment variables
load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

# Path to the movie dataset
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
MOVIES_CSV = os.path.join(DATA_DIR, "movies.csv")

# Rate-limit: TMDB allows ~40 requests per 10 seconds
REQUEST_DELAY = 0.26  # ~3.8 req/s, stays well under the limit


def _tmdb_get(path, params=None):
    """Make a GET request to TMDB API v3 and return the parsed JSON."""
    base = "https://api.themoviedb.org/3"
    qs = f"api_key={TMDB_API_KEY}"
    if params:
        for k, v in params.items():
            qs += f"&{k}={v}"
    url = f"{base}{path}?{qs}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode("utf-8"))


def get_genres():
    """Fetch the TMDB genre id → name mapping."""
    if not TMDB_API_KEY:
        return {}
    try:
        data = _tmdb_get("/genre/movie/list")
        return {g["id"]: g["name"] for g in data["genres"]}
    except Exception as e:
        print(f"  [WARN] Error fetching genres: {e}")
        return {}


def _parse_movie(item, genres_map):
    """Convert a raw TMDB movie dict to our standard record, or None."""
    if not (item.get("overview") and item.get("title")):
        return None

    year = 0
    if item.get("release_date"):
        try:
            year = int(item["release_date"].split("-")[0])
        except Exception:
            pass

    genre_ids = item.get("genre_ids", [])
    genres = [genres_map.get(gid, "") for gid in genre_ids if genres_map.get(gid)]
    genres_str = "|".join(genres)
    if not genres_str:
        return None

    return {
        "id": item["id"],
        "title": item["title"],
        "overview": item["overview"].replace("\n", " ").replace("\r", ""),
        "genre": genres_str,
        "year": year,
        "language": item.get("original_language", "Unknown"),
        "rating": round(item.get("vote_average", 0.0), 1),
    }


def _fetch_pages(endpoint, genres_map, seen_ids, movies, params=None, max_pages=50, label=""):
    """
    Paginate through a TMDB list/discover endpoint.
    Appends unique movies to `movies` and their ids to `seen_ids`.
    Returns the number of new movies added during this call.
    """
    added = 0
    for page in range(1, max_pages + 1):
        p = dict(params or {})
        p["page"] = page
        try:
            time.sleep(REQUEST_DELAY)
            data = _tmdb_get(endpoint, p)
        except Exception as e:
            print(f"    [ERR] {label} page {page}: {e}")
            break

        results = data.get("results", [])
        if not results:
            break

        for item in results:
            mid = item.get("id")
            if mid in seen_ids:
                continue
            rec = _parse_movie(item, genres_map)
            if rec:
                movies.append(rec)
                seen_ids.add(mid)
                added += 1

        total_pages = min(data.get("total_pages", 1), 500)  # TMDB caps at 500
        if page >= total_pages:
            break

    return added


def fetch_movies(target=10000):
    """
    Fetch a large, diverse movie dataset from TMDB using multiple strategies:
      1. Standard list endpoints (popular, top_rated, now_playing, upcoming)
      2. Discover by decade (1950-2026)
      3. Discover by genre
      4. Discover by language (Hindi, Korean, Japanese, French, Spanish, German …)
      5. Discover by vote count (hidden gems with fewer votes)
    All results are deduplicated by TMDB movie ID.
    """
    if not TMDB_API_KEY:
        print("Error: TMDB_API_KEY is not set in .env file.")
        return

    print("=" * 60)
    print(f"  TMDB Large Dataset Fetch -- target >= {target:,} unique movies")
    print("=" * 60)

    genres_map = get_genres()
    if not genres_map:
        print("[FATAL] Could not load genre map. Aborting.")
        return
    print(f"\n  Loaded {len(genres_map)} genres from TMDB.\n")

    movies = []
    seen_ids = set()

    def _status():
        """Print running total."""
        print(f"  >>> Total unique movies so far: {len(movies):,}")

    # ── Strategy 1: Standard list endpoints (100 pages each ≈ 2000 per list) ──
    list_endpoints = [
        ("/movie/popular", "Popular"),
        ("/movie/top_rated", "Top Rated"),
        ("/movie/now_playing", "Now Playing"),
        ("/movie/upcoming", "Upcoming"),
    ]
    for ep, label in list_endpoints:
        print(f"  [{label}] Fetching up to 100 pages …")
        n = _fetch_pages(ep, genres_map, seen_ids, movies, max_pages=100, label=label)
        print(f"    + {n:,} new movies")
        _status()
        if len(movies) >= target:
            break

    # ── Strategy 2: Discover by decade ──────────────────────────────────────
    if len(movies) < target:
        decades = [
            (1950, 1969), (1970, 1979), (1980, 1989), (1990, 1994),
            (1995, 1999), (2000, 2004), (2005, 2009), (2010, 2014),
            (2015, 2017), (2018, 2019), (2020, 2021), (2022, 2023),
            (2024, 2026),
        ]
        for y_start, y_end in decades:
            label = f"Discover {y_start}-{y_end}"
            print(f"  [{label}] …")
            params = {
                "sort_by": "vote_count.desc",
                "primary_release_date.gte": f"{y_start}-01-01",
                "primary_release_date.lte": f"{y_end}-12-31",
                "vote_count.gte": 10,
            }
            n = _fetch_pages("/discover/movie", genres_map, seen_ids, movies,
                             params=params, max_pages=60, label=label)
            print(f"    + {n:,} new movies")
            _status()
            if len(movies) >= target:
                break

    # ── Strategy 3: Discover by genre ──────────────────────────────────────
    if len(movies) < target:
        for gid, gname in genres_map.items():
            label = f"Genre: {gname}"
            print(f"  [{label}] …")
            params = {
                "sort_by": "popularity.desc",
                "with_genres": gid,
                "vote_count.gte": 5,
            }
            n = _fetch_pages("/discover/movie", genres_map, seen_ids, movies,
                             params=params, max_pages=40, label=label)
            print(f"    + {n:,} new movies")
            _status()
            if len(movies) >= target:
                break

    # ── Strategy 4: Discover by language ───────────────────────────────────
    if len(movies) < target:
        languages = [
            ("hi", "Hindi"), ("ko", "Korean"), ("ja", "Japanese"),
            ("fr", "French"), ("es", "Spanish"), ("de", "German"),
            ("it", "Italian"), ("pt", "Portuguese"), ("zh", "Chinese"),
            ("ru", "Russian"), ("ta", "Tamil"), ("te", "Telugu"),
            ("ml", "Malayalam"), ("th", "Thai"), ("tr", "Turkish"),
            ("pl", "Polish"), ("sv", "Swedish"), ("da", "Danish"),
            ("nl", "Dutch"), ("ar", "Arabic"),
        ]
        for lang_code, lang_name in languages:
            label = f"Language: {lang_name}"
            print(f"  [{label}] …")
            params = {
                "sort_by": "vote_count.desc",
                "with_original_language": lang_code,
                "vote_count.gte": 5,
            }
            n = _fetch_pages("/discover/movie", genres_map, seen_ids, movies,
                             params=params, max_pages=30, label=label)
            print(f"    + {n:,} new movies")
            _status()
            if len(movies) >= target:
                break

    # ── Strategy 5: High-rated hidden gems ────────────────────────────────
    if len(movies) < target:
        print("  [Hidden Gems] vote_average ≥ 7, low popularity …")
        params = {
            "sort_by": "vote_average.desc",
            "vote_count.gte": 50,
            "vote_average.gte": 7,
        }
        n = _fetch_pages("/discover/movie", genres_map, seen_ids, movies,
                         params=params, max_pages=80, label="Hidden Gems")
        print(f"    + {n:,} new movies")
        _status()

    # ── Save ──────────────────────────────────────────────────────────────
    print(f"\n{'=' * 60}")
    print(f"  DONE -- {len(movies):,} unique movies collected")
    print(f"{'=' * 60}\n")

    os.makedirs(DATA_DIR, exist_ok=True)

    print(f"  Saving to {MOVIES_CSV} …")
    with open(MOVIES_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f, fieldnames=["id", "title", "overview", "genre", "year", "language", "rating"]
        )
        writer.writeheader()
        writer.writerows(movies)

    print("  [OK] Saved! You can now start the backend to ingest this dataset.\n")


if __name__ == "__main__":
    fetch_movies(target=10000)
