import uvicorn
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from .recommender import RecommenderEngine
from .tmdb_fetcher import TMDBClient
from .vector_db import VectorStore
from .voyage_embeddings import VoyageEmbeddings
from .data_loader import initialize_database
import asyncio

app = FastAPI(
    title="GenAI Movie Recommender",
    description="Semantic movie recommendation engine powered by TMDB, Voyage AI, ChromaDB, and Gemini.",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RecommendRequest(BaseModel):
    query: str
    language: Optional[str] = None
    industry: Optional[str] = None
    min_rating: Optional[float] = None

class IndustryRequest(BaseModel):
    industry: str  # bollywood, korean, japanese, anime, etc.
    query: Optional[str] = None
    top_k: Optional[int] = 20

class LanguageRequest(BaseModel):
    language: str  # Language code: hi, ko, ja, ta, te, etc.

class RecommendResponseItem(BaseModel):
    title: str
    overview: str
    rating: Optional[float]
    score: float
    poster_url: Optional[str]
    reason: str
    id: Optional[int] = None
    language: Optional[str] = None
    genres: Optional[str] = None
    year: Optional[str] = None

class RecommendResponse(BaseModel):
    recommendations: List[RecommendResponseItem]

recommender = RecommenderEngine()
tmdb = TMDBClient()
vector_store = VectorStore()
emb_client = VoyageEmbeddings()

@app.get("/")
async def root():
    return {
        "status": "healthy",
        "service": "GenAI Movie Recommender API",
        "version": "2.0.0",
        "documentation": "/docs"
    }

@app.on_event("startup")
async def startup_event():
    # Load data using initialize_database which handles both language and industry
    asyncio.create_task(initialize_database())

@app.post("/recommend", response_model=RecommendResponse)
async def recommend(req: RecommendRequest):
    try:
        hits = await recommender.recommend(
            req.query,
            top_k=10,
            language=req.language,
            industry=req.industry,
            min_rating=req.min_rating,
        )
        return RecommendResponse(
            recommendations=[
                RecommendResponseItem(
                    title=h["title"],
                    overview=h["overview"],
                    rating=h["rating"],
                    score=h["score"],
                    poster_url=h["poster_url"],
                    reason=h["reason"],
                    id=h.get("id"),
                    language=h.get("language"),
                    genres=h.get("genres"),
                    year=h.get("year"),
                )
                for h in hits
            ]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/industry/recommendations")
async def industry_recommendations(req: IndustryRequest):
    """Get recommendations from a specific industry"""
    try:
        hits = await recommender.get_by_industry(
            req.industry,
            query=req.query,
            top_k=req.top_k
        )
        return {
            "industry": req.industry,
            "recommendations": hits
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/industries")
async def get_industries():
    """Get list of supported industries"""
    return {
        "industries": [
            "hollywood",
            "bollywood",
            "tollywood",
            "kollywood",
            "sandalwood",
            "mollywood",
            "korean",
            "japanese",
            "anime",
            "international"
        ]
    }

@app.get("/languages")
async def get_languages():
    """Get list of supported languages"""
    return {
        "languages": {
            "en": "English",
            "hi": "Hindi",
            "te": "Telugu",
            "ta": "Tamil",
            "kn": "Kannada",
            "ml": "Malayalam",
            "ko": "Korean",
            "ja": "Japanese",
            "es": "Spanish",
            "fr": "French",
            "de": "German",
            "it": "Italian",
            "pt": "Portuguese",
            "ru": "Russian",
            "zh": "Chinese",
        }
    }

@app.post("/language/recommendations")
async def language_recommendations(req: LanguageRequest):
    """Get recommendations in a specific language"""
    try:
        hits = await recommender.get_by_language(req.language, top_k=10)
        return {
            "language": req.language,
            "recommendations": hits
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/movies/trending")
async def trending():
    movies = await tmdb.fetch_trending()
    return movies

@app.get("/movie/{movie_id}")
async def movie_detail(movie_id: int):
    try:
        data = await tmdb.fetch_movie(movie_id)
        return data
    except Exception:
        raise HTTPException(status_code=404, detail="Movie not found")

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
