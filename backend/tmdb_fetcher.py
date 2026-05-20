import httpx
from .config import settings

IMG_BASE = "https://image.tmdb.org/t/p/w500"

# Map ISO 639-1 codes to language names for TMDB API
LANGUAGE_MAP = {
    "en": "en-US", "hi": "hi-IN", "es": "es-ES", "fr": "fr-FR",
    "ja": "ja-JP", "ko": "ko-KR", "de": "de-DE", "it": "it-IT",
    "zh": "zh-CN", "pt": "pt-BR", "ru": "ru-RU", "ar": "ar-SA",
    "te": "te-IN", "ta": "ta-IN", "ml": "ml-IN", "bn": "bn-IN",
    "th": "th-TH", "tr": "tr-TR", "pl": "pl-PL", "nl": "nl-NL",
    "sv": "sv-SE", "da": "da-DK", "no": "no-NO", "fi": "fi-FI",
    "kn": "kn-IN", "mr": "mr-IN", "gu": "gu-IN", "pa": "pa-IN",
}

class TMDBClient:
    def __init__(self):
        self.api_key = settings.TMDB_API_KEY
        self.client = httpx.AsyncClient(base_url=settings.TMDB_BASE_URL)

    async def _get(self, endpoint: str, params: dict = None):
        p = params.copy() if params else {}
        p["api_key"] = self.api_key
        resp = await self.client.get(endpoint, params=p)
        resp.raise_for_status()
        return resp.json()

    async def fetch_movie(self, movie_id: int) -> dict:
        data = await self._get(f"/movie/{movie_id}", {"language": "en-US"})
        data["poster_url"] = IMG_BASE + data["poster_path"] if data.get("poster_path") else None
        data["backdrop_url"] = IMG_BASE + data["backdrop_path"] if data.get("backdrop_path") else None
        data["genres_text"] = ", ".join(g["name"] for g in data.get("genres", []))
        data["release_year"] = data.get("release_date", "").split("-")[0] if data.get("release_date") else None
        data["rating"] = data.get("vote_average")
        return data

    async def fetch_trending(self, page: int = 1, language: str = None) -> list[dict]:
        """Fetch trending movies. If language is specified, fetch movies in that language."""
        params = {"page": page, "language": "en-US"}
        
        if language and language != "en":
            # Use discover endpoint for specific language filtering
            raw = await self._get("/discover/movie", {
                "page": page,
                "language": "en-US",
                "with_original_language": language,
                "sort_by": "popularity.desc",
                "vote_count.gte": "50",
            })
        else:
            raw = await self._get("/trending/movie/week", params)
        
        movies = []
        for m in raw.get("results", []):
            movies.append({
                "id": m["id"],
                "title": m.get("title", m.get("name", "")),
                "overview": m.get("overview", ""),
                "genres_text": "",
                "poster_url": IMG_BASE + m["poster_path"] if m.get("poster_path") else None,
                "rating": m.get("vote_average"),
                "popularity": m.get("popularity"),
                "release_year": m.get("release_date", "").split("-")[0] if m.get("release_date") else None,
                "original_language": m.get("original_language", "en"),
            })
        return movies

    async def fetch_by_language(self, language: str, page: int = 1) -> list[dict]:
        """Fetch popular movies filtered by a specific original language."""
        raw = await self._get("/discover/movie", {
            "page": page,
            "language": "en-US",
            "with_original_language": language,
            "sort_by": "popularity.desc",
            "vote_count.gte": "20",
        })
        movies = []
        for m in raw.get("results", []):
            movies.append({
                "id": m["id"],
                "title": m.get("title", m.get("name", "")),
                "overview": m.get("overview", ""),
                "genres_text": "",
                "poster_url": IMG_BASE + m["poster_path"] if m.get("poster_path") else None,
                "rating": m.get("vote_average"),
                "popularity": m.get("popularity"),
                "release_year": m.get("release_date", "").split("-")[0] if m.get("release_date") else None,
                "original_language": m.get("original_language", language),
            })
        return movies

    async def fetch_bollywood(self, page: int = 1) -> list[dict]:
        """Fetch Bollywood (Hindi) movies"""
        return await self.fetch_by_language("hi", page)

    async def fetch_tollywood(self, page: int = 1) -> list[dict]:
        """Fetch Tollywood (Telugu) movies"""
        return await self.fetch_by_language("te", page)

    async def fetch_kollywood(self, page: int = 1) -> list[dict]:
        """Fetch Kollywood (Tamil) movies"""
        return await self.fetch_by_language("ta", page)

    async def fetch_sandalwood(self, page: int = 1) -> list[dict]:
        """Fetch Sandalwood (Kannada) movies"""
        return await self.fetch_by_language("kn", page)

    async def fetch_mollywood(self, page: int = 1) -> list[dict]:
        """Fetch Mollywood (Malayalam) movies"""
        return await self.fetch_by_language("ml", page)

    async def fetch_korean(self, page: int = 1) -> list[dict]:
        """Fetch Korean movies"""
        return await self.fetch_by_language("ko", page)

    async def fetch_japanese(self, page: int = 1) -> list[dict]:
        """Fetch Japanese movies"""
        return await self.fetch_by_language("ja", page)

    async def fetch_anime(self, page: int = 1) -> list[dict]:
        """Fetch anime movies"""
        raw = await self._get("/discover/movie", {
            "page": page,
            "language": "en-US",
            "with_genres": "16",  # Animation genre
            "with_original_language": "ja",  # Japanese language
            "sort_by": "popularity.desc",
            "vote_count.gte": "10",
        })
        movies = []
        for m in raw.get("results", []):
            movies.append({
                "id": m["id"],
                "title": m.get("title", ""),
                "overview": m.get("overview", ""),
                "genres_text": "Anime",
                "poster_url": IMG_BASE + m["poster_path"] if m.get("poster_path") else None,
                "rating": m.get("vote_average"),
                "popularity": m.get("popularity"),
                "release_year": m.get("release_date", "").split("-")[0] if m.get("release_date") else None,
                "original_language": "ja",
                "industry": "anime",
            })
        return movies

    async def fetch_spanish(self, page: int = 1) -> list[dict]:
        """Fetch Spanish movies"""
        return await self.fetch_by_language("es", page)

    async def fetch_french(self, page: int = 1) -> list[dict]:
        """Fetch French movies"""
        return await self.fetch_by_language("fr", page)

    async def fetch_chinese(self, page: int = 1) -> list[dict]:
        """Fetch Chinese movies"""
        return await self.fetch_by_language("zh", page)

    async def fetch_german(self, page: int = 1) -> list[dict]:
        """Fetch German movies"""
        return await self.fetch_by_language("de", page)

    async def fetch_italian(self, page: int = 1) -> list[dict]:
        """Fetch Italian movies"""
        return await self.fetch_by_language("it", page)

    async def fetch_russian(self, page: int = 1) -> list[dict]:
        """Fetch Russian movies"""
        return await self.fetch_by_language("ru", page)

    async def fetch_turkish(self, page: int = 1) -> list[dict]:
        """Fetch Turkish movies"""
        return await self.fetch_by_language("tr", page)

    async def fetch_thai(self, page: int = 1) -> list[dict]:
        """Fetch Thai movies"""
        return await self.fetch_by_language("th", page)

    async def fetch_by_genres(self, genre_ids: list[int], page: int = 1) -> list[dict]:
        """Fetch movies by genre IDs"""
        raw = await self._get("/discover/movie", {
            "page": page,
            "language": "en-US",
            "with_genres": ",".join(map(str, genre_ids)),
            "sort_by": "popularity.desc",
            "vote_count.gte": "50",
        })
        movies = []
        for m in raw.get("results", []):
            movies.append({
                "id": m["id"],
                "title": m.get("title", ""),
                "overview": m.get("overview", ""),
                "genres_text": "",
                "poster_url": IMG_BASE + m["poster_path"] if m.get("poster_path") else None,
                "rating": m.get("vote_average"),
                "popularity": m.get("popularity"),
                "release_year": m.get("release_date", "").split("-")[0] if m.get("release_date") else None,
                "original_language": m.get("original_language", "en"),
            })
        return movies

    async def search(self, query: str, page: int = 1) -> list[dict]:
        """Search movies by title or description"""
        raw = await self._get("/search/movie", {
            "query": query,
            "page": page,
            "language": "en-US",
        })
        movies = []
        for m in raw.get("results", []):
            movies.append({
                "id": m["id"],
                "title": m.get("title", ""),
                "overview": m.get("overview", ""),
                "genres_text": "",
                "poster_url": IMG_BASE + m["poster_path"] if m.get("poster_path") else None,
                "rating": m.get("vote_average"),
                "popularity": m.get("popularity"),
                "release_year": m.get("release_date", "").split("-")[0] if m.get("release_date") else None,
                "original_language": m.get("original_language", "en"),
            })
        return movies
