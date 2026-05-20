import asyncio
import json
import os
import httpx
from dotenv import load_dotenv

load_dotenv('.env')
from backend.config import settings
from backend.chat_assistant import ChatAssistant

async def main():
    print('COHERE_BASE_URL=', settings.COHERE_BASE_URL)
    print('COHERE_MODEL=', settings.COHERE_MODEL)
    assistant = ChatAssistant()
    user_message = 'Suggest a sci-fi movie'
    history = []
    conversation = 'You are a helpful movie recommendation AI assistant. Use the movie recommendations from the database context provided below to answer the user\'s query if it matches their request. Be friendly and conversational.\n\n'
    conversation += f'User: {user_message}\nAssistant:'
    payload = {'model': settings.COHERE_MODEL, 'message': conversation}
    print('payload=', payload)
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(settings.COHERE_BASE_URL, headers={'Authorization': f'Bearer {settings.COHERE_API_KEY}', 'Content-Type': 'application/json'}, json=payload, timeout=30)
            print('status', resp.status_code)
            print(resp.text)
    except Exception as e:
        print('exception', repr(e))
    print('\n--- now using ChatAssistant.chat() ---')
    try:
        result = await assistant.chat(user_message, history)
        print('assistant result:', result)
    except Exception as e:
        print('assistant exception', repr(e))

if __name__ == '__main__':
    asyncio.run(main())
