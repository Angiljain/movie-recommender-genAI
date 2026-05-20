from qdrant_client import QdrantClient
from qdrant_client.http import models
from .config import settings

class CollectionProxy:
    def __init__(self, qdrant_client, collection_name):
        self.client = qdrant_client
        self.name = collection_name

    def count(self) -> int:
        try:
            info = self.client.get_collection(self.name)
            return info.points_count
        except Exception:
            return 0

class VectorStore:
    def __init__(self):
        # If QDRANT_URL and QDRANT_API_KEY are provided, connect to the Cloud instance.
        # Otherwise, fall back to a local directory for seamless local development.
        if settings.QDRANT_URL and settings.QDRANT_API_KEY:
            self.client = QdrantClient(
                url=settings.QDRANT_URL,
                api_key=settings.QDRANT_API_KEY,
            )
        else:
            self.client = QdrantClient(path="./qdrant_db")
            
        self.collection_name = "movies"
        self._ensure_collection()
        self.collection = CollectionProxy(self.client, self.collection_name)

    def _ensure_collection(self):
        try:
            self.client.get_collection(collection_name=self.collection_name)
        except Exception:
            # Create collection with Voyage AI embeddings dimension size (1536)
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=1536,
                    distance=models.Distance.COSINE
                )
            )

    def upsert(self, movies: list[dict], embeddings: list[list[float]]):
        points = []
        for i, m in enumerate(movies):
            point_id = int(m["id"])
            metadata = {
                "title": m.get("title", ""),
                "overview": m.get("overview", ""),
                "genres": m.get("genres_text", "") or m.get("genres", ""),
                "poster_url": m.get("poster_url") or "",
                "year": str(m.get("release_year") or m.get("year") or ""),
                "rating": float(m.get("rating") or m.get("vote_average") or 0.0),
                "popularity": float(m.get("popularity") or 0.0),
                "language": m.get("original_language") or m.get("language") or "en",
                "industry": m.get("industry", "international"),
            }
            points.append(
                models.PointStruct(
                    id=point_id,
                    vector=embeddings[i],
                    payload=metadata
                )
            )
            
        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )

    def query(self, query_embedding: list[float], top_k: int = 10, language: str = None, industry: str = None):
        """Query the vector store. If language or industry is specified, filter results."""
        filter_conditions = []
        if language:
            filter_conditions.append(
                models.FieldCondition(
                    key="language",
                    match=models.MatchValue(value=language)
                )
            )
        if industry:
            filter_conditions.append(
                models.FieldCondition(
                    key="industry",
                    match=models.MatchValue(value=industry)
                )
            )
            
        qdrant_filter = None
        if filter_conditions:
            qdrant_filter = models.Filter(must=filter_conditions)
            
        try:
            res = self.client.query_points(
                collection_name=self.collection_name,
                query=query_embedding,
                limit=top_k,
                query_filter=qdrant_filter
            )
            results = res.points
        except Exception:
            # Fallback without filter if it errors
            res = self.client.query_points(
                collection_name=self.collection_name,
                query=query_embedding,
                limit=top_k
            )
            results = res.points
            
        hits = []
        for r in results:
            meta = r.payload
            hits.append({
                "id": int(r.id),
                "title": meta.get("title"),
                "overview": meta.get("overview"),
                "poster_url": meta.get("poster_url"),
                "year": meta.get("year"),
                "rating": meta.get("rating"),
                "language": meta.get("language", "en"),
                "industry": meta.get("industry", "international"),
                "genres": meta.get("genres", ""),
                "score": round(r.score, 3),
            })
        return hits

