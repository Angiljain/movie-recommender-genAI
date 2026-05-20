from .voyage_embeddings import VoyageEmbeddings
from .vector_db import VectorStore

class RecommenderEngine:
    def __init__(self):
        self.emb_client = VoyageEmbeddings()
        self.store = VectorStore()

    async def recommend(self, query: str, top_k: int = 10, language: str = None, industry: str = None, min_rating: float = None, explain: bool = False):
        """
        Recommend movies based on a natural language query.
        Optional filters: language, industry, min_rating
        """
        query_emb = (await self.emb_client.embed([query]))[0]
        # Get extra results to account for filtering and sorting
        hits = self.store.query(query_emb, top_k=top_k*4, language=language, industry=industry)
        
        if min_rating:
            hits = [h for h in hits if float(h.get("rating", 0)) >= float(min_rating)]
            
        if "latest" in query.lower():
            # Sort by year descending (latest first). Handle empty/None year strings.
            hits.sort(key=lambda x: str(x.get("year", "")) or "0000", reverse=True)
        
        # Keep top_k after filtering/sorting
        hits = hits[:top_k]
        
        for hit in hits:
            hit["reason"] = ""
                
        return hits

    async def get_by_industry(self, industry: str, query: str = None, top_k: int = 10):
        """Get movies from a specific industry"""
        if not query:
            query = f"popular {industry} movies"
        return await self.recommend(query, top_k=top_k, industry=industry, explain=False)

    async def get_by_language(self, language: str, query: str = None, top_k: int = 10):
        """Get movies in a specific language"""
        if not query:
            query = f"movies in {language}"
        return await self.recommend(query, top_k=top_k, language=language, explain=False)

    async def get_trending(self, top_k: int = 10):
        """Get trending movies across all industries"""
        return await self.recommend("trending popular movies", top_k=top_k)

