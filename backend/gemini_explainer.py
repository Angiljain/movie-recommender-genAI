import httpx
import json
from .config import settings


def _build_gemini_url(path: str) -> str:
    return f"{settings.GEMINI_BASE_URL}/{settings.GEMINI_MODEL}:{path}"


class GeminiExplainer:
    def __init__(self):
        self.client = httpx.AsyncClient()

    async def _call_llm(self, payload: dict) -> str:
        url = _build_gemini_url("generateContent") + f"?key={settings.GEMINI_API_KEY}"
        resp = await self.client.post(
            url,
            headers={"Content-Type": "application/json"},
            json=payload,
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()
        if "candidates" in data and len(data["candidates"]) > 0:
            return data["candidates"][0]["content"]["parts"][0]["text"]
        return ""

    async def explain(self, movie_titles: list[str], user_query: str) -> list[str]:
        if not settings.GEMINI_API_KEY:
            return ["(explanation unavailable)"] * len(movie_titles)
            
        prompt = (
            f"User asked: \"{user_query}\".\n"
            f"For each of the following movies, write a one-sentence recommendation reason "
            f"that ties the movie to the query. Return the reasons as a valid JSON object containing a single key 'reasons' which is an array of strings in the exact same order.\n"
            f"Movies: {', '.join(movie_titles)}"
        )
        payload = {
            "contents": [{"role": "user", "parts": [{"text": prompt}]}],
            "generationConfig": {
                "responseMimeType": "application/json"
            }
        }

        try:
            text = await self._call_llm(payload)
            text = text.strip()
            
            # Extract JSON from potential markdown blocks
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0].strip()
            elif "```" in text:
                text = text.split("```")[1].split("```")[0].strip()
                
            data = json.loads(text)
            reasons = data.get("reasons", [])
            
            if len(reasons) < len(movie_titles):
                reasons.extend(["(explanation unavailable)"] * (len(movie_titles) - len(reasons)))
            elif len(reasons) > len(movie_titles):
                reasons = reasons[:len(movie_titles)]
            return reasons
        except Exception as e:
            print(f"Error calling LLM Explainer: {e}")
            return ["(explanation unavailable)"] * len(movie_titles)
