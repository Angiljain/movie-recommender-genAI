"""Data loader for populating the vector store with movies from multiple industries."""

import asyncio
from .tmdb_fetcher import TMDBClient
from .voyage_embeddings import VoyageEmbeddings
from .vector_db import VectorStore

# Define industries and their configurations
INDUSTRIES = {
    "hollywood": {"method": "fetch_trending", "pages": 2},
    "bollywood": {"method": "fetch_bollywood", "pages": 2},
    "tollywood": {"method": "fetch_tollywood", "pages": 1},
    "kollywood": {"method": "fetch_kollywood", "pages": 1},
    "sandalwood": {"method": "fetch_sandalwood", "pages": 1},
    "mollywood": {"method": "fetch_mollywood", "pages": 1},
    "korean": {"method": "fetch_korean", "pages": 2},
    "japanese": {"method": "fetch_japanese", "pages": 2},
    "anime": {"method": "fetch_anime", "pages": 1},
    "spanish": {"method": "fetch_spanish", "pages": 1},
    "french": {"method": "fetch_french", "pages": 1},
    "chinese": {"method": "fetch_chinese", "pages": 1},
    "german": {"method": "fetch_german", "pages": 1},
    "italian": {"method": "fetch_italian", "pages": 1},
    "russian": {"method": "fetch_russian", "pages": 1},
    "turkish": {"method": "fetch_turkish", "pages": 1},
    "thai": {"method": "fetch_thai", "pages": 1},
}

# Genre mappings (TMDB genre IDs)
GENRES = {
    "action": 28,
    "comedy": 35,
    "drama": 18,
    "horror": 27,
    "romance": 10749,
    "thriller": 53,
    "sci-fi": 878,
    "fantasy": 14,
    "animation": 16,
    "adventure": 12,
    "crime": 80,
    "documentary": 99,
    "family": 10751,
    "history": 36,
    "mystery": 9648,
    "war": 10752,
    "western": 37,
}

class DataLoader:
    def __init__(self):
        self.tmdb = TMDBClient()
        self.embeddings = VoyageEmbeddings()
        self.store = VectorStore()

    async def load_industry_data(self):
        """Load movies from all industries"""
        print("\n=== Starting Industry Data Load ===\n")
        
        for industry, config in INDUSTRIES.items():
            await self._load_industry(industry, config)
        
        print("\n=== Industry Data Load Complete ===\n")
        total_count = self.store.collection.count()
        print(f"Total movies in database: {total_count}")

    async def _load_industry(self, industry: str, config: dict):
        """Load movies for a specific industry"""
        print(f"\nLoading {industry.upper()}...")
        
        method = getattr(self.tmdb, config["method"])
        pages = config["pages"]
        
        all_movies = []
        for page in range(1, pages + 1):
            try:
                movies = await method(page=page)
                if not movies:
                    break
                all_movies.extend(movies)
                print(f"  Page {page}: {len(movies)} movies")
            except Exception as e:
                print(f"  Error loading page {page}: {e}")
        
        if not all_movies:
            print(f"  No movies found for {industry}")
            return
        
        # Fetch detailed info for each movie
        try:
            detailed_movies = await asyncio.gather(
                *[self.tmdb.fetch_movie(m["id"]) for m in all_movies],
                return_exceptions=True
            )
            detailed_movies = [m for m in detailed_movies if not isinstance(m, Exception)]
        except Exception as e:
            print(f"  Error fetching details: {e}")
            return
        
        # Add industry tag to metadata
        for movie in detailed_movies:
            movie["industry"] = industry
        
        # Create embeddings
        texts = [
            f"{m.get('title', '')} {m.get('overview', '')} {m.get('genres_text', '')}"
            for m in detailed_movies
        ]
        
        try:
            embeddings = await self.embeddings.embed(texts)
            print(f"  Created {len(embeddings)} embeddings")
        except Exception as e:
            print(f"  Error creating embeddings: {e}")
            return
        
        # Upsert to vector store
        try:
            self.store.upsert(detailed_movies, embeddings)
            print(f"  Stored {len(detailed_movies)} {industry} movies")
        except Exception as e:
            print(f"  Error storing movies: {e}")

        # Small pause between industry loads to avoid API throttling
        await asyncio.sleep(4.0)

    async def load_by_genre(self, genre_name: str):
        """Load movies for a specific genre"""
        if genre_name not in GENRES:
            print(f"Genre {genre_name} not found")
            return
        
        print(f"\nLoading {genre_name.upper()} movies...")
        
        genre_id = GENRES[genre_name]
        all_movies = []
        
        for page in range(1, 4):  # Load 3 pages per genre
            try:
                movies = await self.tmdb.fetch_by_genres([genre_id], page=page)
                if not movies:
                    break
                all_movies.extend(movies)
            except Exception as e:
                print(f"  Error loading page {page}: {e}")
        
        if not all_movies:
            print(f"  No movies found for genre {genre_name}")
            return
        
        # Fetch detailed info
        try:
            detailed_movies = await asyncio.gather(
                *[self.tmdb.fetch_movie(m["id"]) for m in all_movies],
                return_exceptions=True
            )
            detailed_movies = [m for m in detailed_movies if not isinstance(m, Exception)]
        except Exception as e:
            print(f"  Error fetching details: {e}")
            return
        
        # Add genre tag
        for movie in detailed_movies:
            movie["genre"] = genre_name
        
        # Create embeddings and store
        texts = [
            f"{m.get('title', '')} {m.get('overview', '')} {m.get('genres_text', '')}"
            for m in detailed_movies
        ]
        
        try:
            embeddings = await self.embeddings.embed(texts)
            self.store.upsert(detailed_movies, embeddings)
            print(f"  Stored {len(detailed_movies)} {genre_name} movies")
        except Exception as e:
            print(f"  Error: {e}")


async def initialize_database():
    """Initialize the database with movies from all industries"""
    loader = DataLoader()
    
    # Check if database is already populated
    if loader.store.collection.count() > 50:
        print("Database already populated with movies")
        return
    
    await loader.load_industry_data()
