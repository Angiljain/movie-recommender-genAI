# 🎬 GenAI Movie Recommender

A modern movie recommendation system built for local development and fast semantic discovery.
This project uses Voyage AI embeddings, TMDB movie metadata, and ChromaDB vector search to recommend movies based on natural language queries.

## 🧠 What it does
- Uses **Voyage AI** to generate high-quality semantic embeddings for movie descriptions.
- Stores vectors in **ChromaDB** for fast nearest-neighbor retrieval.
- Fetches movie metadata from **TMDB**.
- Returns ranked movie recommendations with AI-generated explanation text.
- Provides a **Next.js** frontend to search and browse recommendations locally.

## 🚀 Local Setup

### Prerequisites
- Python 3.11+ (or compatible)
- Node.js 18+ / npm
- TMDB API key
- Voyage AI API key

### 1. Install backend dependencies
```powershell
cd A:\Projects\Movie recommendor genai
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Create environment variables
Create a `.env` file in the project root with:
```env
TMDB_API_KEY=your_tmdb_api_key
VOYAGE_API_KEY=your_voyage_api_key
```

> `GEMINI_API_KEY` is not required for core recommendation flow, since the app is focused on Voyage-based embeddings.

### 3. Run the backend
```powershell
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

### 4. Run the frontend
```powershell
cd frontend
npm install
npm run dev
```

### 5. Open the app
- Frontend: `http://localhost:3000`
- Backend docs: `http://localhost:8000/docs`

## 🧩 Backend API Endpoints
- `POST /recommend` — search for movies with natural language queries
- `GET /movies/trending` — fetch TMDB trending movies
- `GET /movie/{id}` — fetch a movie by TMDB ID
- `GET /industries` — list supported industry tags
- `GET /languages` — list supported language codes
- `POST /industry/recommendations` — recommendations by industry
- `POST /language/recommendations` — recommendations by language

## 📦 Frontend
The frontend is a Next.js application with a home search page and movie detail pages.
It uses the backend recommendation API to display results and movie cards.

## 🗂️ Project Structure
```
A:\Projects\Movie recommendor genai/
├── backend/
│   ├── main.py              # FastAPI app and API routes
│   ├── config.py            # environment config and settings
│   ├── tmdb_fetcher.py      # TMDB API client
│   ├── voyage_embeddings.py # Voyage AI embedding client
│   ├── vector_db.py         # ChromaDB wrapper
│   ├── recommender.py       # recommendation logic
│   ├── gemini_explainer.py  # optional explanation generator
│   ├── data_loader.py       # dataset ingestion and embedding creation
│   └── __init__.py
├── frontend/
│   ├── src/
│   │   ├── pages/           # Next.js pages
│   │   ├── components/      # UI components
│   │   └── styles/          # global styles
│   ├── next.config.js
│   ├── package.json
│   ├── tsconfig.json
│   └── tailwind.config.ts
├── chroma_db/               # local ChromaDB persistence store
├── data/                    # movie CSV data
├── requirements.txt
├── run_backend.ps1          # PowerShell backend starter
├── run_frontend.ps1         # PowerShell frontend starter
└── README.md
```

## 💡 Notes
- The app is designed to run locally on `localhost`.
- Chat functionality has been removed from the UI, leaving a focused Voyage embedding recommendation experience.
- If you want to refresh the movie index, delete `chroma_db/chroma.sqlite3` and restart the backend.

## 🛠️ Troubleshooting
- If the frontend reports TypeScript or ESLint errors, run `npm install` and ensure `tsconfig.json` has `baseUrl: '.'`.
- If the backend cannot start, verify `TMDB_API_KEY` and `VOYAGE_API_KEY` are set in `.env`.
- Use `http://localhost:8000/docs` to inspect available API routes.
