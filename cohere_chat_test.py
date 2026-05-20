import os
import httpx
from dotenv import load_dotenv

load_dotenv('.env')
key = os.environ.get('COHERE_API_KEY')
if not key:
    raise SystemExit('COHERE_API_KEY not found')

headers = {'Authorization': f'Bearer {key}', 'Content-Type': 'application/json'}
models = ['command-xlarge-nightly', 'command-xlarge', 'command-light', 'command-medium', 'command-small', 'command', 'xlarge']
for model in models:
    print('MODEL', model)
    payload = {'model': model, 'message': 'Hello movie assistant'}
    r = httpx.post('https://api.cohere.ai/v1/chat', headers=headers, json=payload, timeout=30)
    print(r.status_code)
    print(r.text)
    print('---')
