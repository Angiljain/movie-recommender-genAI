import chromadb
from chromadb.config import Settings as ChromaSettings
from .config import settings

class VectorStore:
    def __init__(self):
        self.client = chromadb.PersistentClient(
            path=settings.CHROMA_PERSIST_DIR,
            settings=ChromaSettings(anonymized_telemetry=False)
        )
        self.collection = self.client.get_or_create_collection(name="movies")

    def upsert(self, movies: list[dict], embeddings: list[list[float]]):
        ids = [str(m["id"]) for m in movies]
        metadatas = []
        for m in movies:
            metadata = {
                "title": m.get("title", ""),
                "overview": m.get("overview", ""),
                "genres": m.get("genres_text", ""),
                "poster_url": m.get("poster_url") or "",
                "year": m.get("release_year") or "",
                "rating": float(m.get("rating") or 0.0),
                "popularity": float(m.get("popularity") or 0.0),
                "language": m.get("original_language", "en"),
                "industry": m.get("industry", "international"),
            }
            metadatas.append(metadata)

        documents = [f"{m.get('title', '')} {m.get('overview', '')} {m.get('genres_text', '')}" for m in movies]
        
        # Batch upsert to chroma
        self.collection.upsert(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
        )

    def query(self, query_embedding: list[float], top_k: int = 10, language: str = None, industry: str = None):
        """Query the vector store. If language or industry is specified, filter results."""
        where_filter = None
        if language and industry:
            where_filter = {"$and": [{"language": {"$eq": language}}, {"industry": {"$eq": industry}}]}
        elif language:
            where_filter = {"language": {"$eq": language}}
        elif industry:
            where_filter = {"industry": {"$eq": industry}}
        
        try:
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k,
                include=["documents", "metadatas", "distances"],
                where=where_filter,
            )
        except Exception:
            # If filtering fails (e.g., no docs match), query without filter
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k,
                include=["documents", "metadatas", "distances"],
            )

        if not results["ids"] or len(results["ids"][0]) == 0:
            return []
            
        hits = []
        for i, rid in enumerate(results["ids"][0]):
            meta = results["metadatas"][0][i]
            dist = results["distances"][0][i]
            hits.append({
                "id": int(rid),
                "title": meta.get("title"),
                "overview": meta.get("overview"),
                "poster_url": meta.get("poster_url"),
                "year": meta.get("year"),
                "rating": meta.get("rating"),
                "language": meta.get("language", "en"),
                "industry": meta.get("industry", "international"),
                "genres": meta.get("genres", ""),
                "score": round(1 - dist, 3),  # assuming cosine distance, 1-dist is similarity
            })
        return hits
