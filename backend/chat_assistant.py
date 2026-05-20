import httpx
from .config import settings
from .recommender import RecommenderEngine


def _build_gemini_url(path: str) -> str:
    return f"{settings.GEMINI_BASE_URL}/{settings.GEMINI_MODEL}:{path}"


class ChatAssistant:
    def __init__(self):
        self.client = httpx.AsyncClient()
        self.recommender = RecommenderEngine()

    async def chat(self, user_message: str, history: list[dict] = None) -> str:
        industry = None
        language = None
        msg_lower = user_message.lower()
        
        industries = ["hollywood", "bollywood", "tollywood", "kollywood", "sandalwood", "mollywood", "korean", "japanese", "anime", "international"]
        for ind in industries:
            if ind in msg_lower:
                industry = ind
                break
                
        languages = {"english": "en", "hindi": "hi", "telugu": "te", "tamil": "ta", "kannada": "kn", "malayalam": "ml", "spanish": "es", "french": "fr", "german": "de"}
        for lang_name, lang_code in languages.items():
            if lang_name in msg_lower:
                language = lang_code
                break

        if "korean" in msg_lower and not language: language = "ko"
        if "japanese" in msg_lower and not language: language = "ja"

        context = ""
        try:
            hits = await self.recommender.recommend(user_message, top_k=5, language=language, industry=industry, explain=False)
            if hits:
                context = "Movie recommendations from the database:\n"
                for h in hits:
                    context += f"- Title: {h['title']} ({h.get('year', 'N/A')}), Industry: {h.get('industry', 'N/A')}, Language: {h.get('language', 'N/A')}\n  Overview: {h['overview']}\n"
        except Exception as e:
            print(f"Error retrieving context: {e}")

        system_prompt = "You are a helpful movie recommendation AI assistant. Use the movie recommendations from the database context provided below to answer the user's query if it matches their request. Be friendly and conversational.\n\n"
        if context:
            system_prompt += f"{context}\n\n"
            
        gemini_history = []
        if history:
            for turn in history:
                role = "model" if turn["role"] == "assistant" else "user"
                gemini_history.append({"role": role, "parts": [{"text": turn["content"]}]})
                
        gemini_history.append({"role": "user", "parts": [{"text": user_message}]})

        payload = {
            "system_instruction": {"parts": [{"text": system_prompt}]},
            "contents": gemini_history,
        }

        url = _build_gemini_url("generateContent") + f"?key={settings.GEMINI_API_KEY}"

        try:
            resp = await self.client.post(
                url,
                headers={"Content-Type": "application/json"},
                json=payload,
                timeout=30,
            )
            resp.raise_for_status()
            data = resp.json()
            if "candidates" in data and len(data["candidates"]) > 0:
                return data["candidates"][0]["content"]["parts"][0]["text"].strip()
            return "Sorry, I could not retrieve a response."
        except Exception as e:
            print(f"Error calling Gemini Chat: {e}")
            if context:
                return (
                    "I found some movies that match your request. "
                    "Here are a few suggestions based on the database context above."
                )
            return "Sorry, I am unable to process your message at this time."
