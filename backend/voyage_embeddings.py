import asyncio
import httpx
from .config import settings


class VoyageEmbeddings:
    def __init__(self):
        self.url = settings.VOYAGE_BASE_URL
        self.headers = {
            "Authorization": f"Bearer {settings.VOYAGE_API_KEY}",
            "Content-Type": "application/json",
        }
        self.client = httpx.AsyncClient(
            headers=self.headers,
            follow_redirects=True,
            timeout=60,
        )

    async def _embed_batch(self, batch_texts: list[str]) -> list[list[float]]:
        payload = {"model": "voyage-large-2", "input": batch_texts}
        max_retries = 3
        backoff = 1.0

        for attempt in range(1, max_retries + 1):
            try:
                resp = await self.client.post(self.url, json=payload)
                resp.raise_for_status()
                return [item["embedding"] for item in resp.json()["data"]]
            except httpx.HTTPStatusError as exc:
                status = exc.response.status_code
                if status == 429 and attempt < max_retries:
                    await asyncio.sleep(backoff)
                    backoff *= 2
                    continue
                raise
            except httpx.RequestError:
                if attempt < max_retries:
                    await asyncio.sleep(backoff)
                    backoff *= 2
                    continue
                raise

    async def embed(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []

        embeddings = []
        batch_size = 16
        for i in range(0, len(texts), batch_size):
            batch = texts[i : i + batch_size]
            embeddings.extend(await self._embed_batch(batch))
            if i + batch_size < len(texts):
                await asyncio.sleep(0.5)

        return embeddings
