# GenAI Movie Recommender

A modern movie recommendation system built for fast semantic discovery.
This project uses Voyage AI embeddings, TMDB movie metadata, and Qdrant vector search to recommend movies based on natural language queries.

## What it does
- Uses **Voyage AI** to generate high-quality semantic embeddings for movie descriptions.
- Stores vectors in **Qdrant** for fast nearest-neighbor retrieval (supports local file storage or Qdrant Cloud).
- Fetches movie metadata from **TMDB**.
- Returns ranked movie recommendations instantly.
- Provides a **Next.js** frontend to search and browse recommendations.

## Configuration & Environment Variables

Configure the following environment variables for deployment or runtime:

### Backend Variables (`.env`)
```env
TMDB_API_KEY=your_tmdb_api_key
VOYAGE_API_KEY=your_voyage_api_key
QDRANT_URL=your_qdrant_cloud_endpoint_url (optional, defaults to local folder if omitted)
QDRANT_API_KEY=your_qdrant_api_key (optional, defaults to local folder if omitted)
```

### Frontend Variables (`frontend/.env.local`)
```env
NEXT_PUBLIC_API_URL=https://your-deployed-backend-url.com
```

## Deployment

### Backend (FastAPI)
The backend is a FastAPI application that can be deployed stateless on platforms like **Render**, **Railway**, **Fly.io**, or **AWS**.
- **Start Command**: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
- Ensure the keys are configured in your platform's environment settings.

### Frontend (Next.js)
The frontend is a Next.js application designed to be deployed on **Vercel** or **Netlify**.
- **Build Command**: `npm run build`
- **Start Command**: `npm start`
- Ensure `NEXT_PUBLIC_API_URL` is set to your deployed FastAPI backend URL.

## Backend API Endpoints
- `POST /recommend` — search for movies with natural language queries
- `GET /movies/trending` — fetch TMDB trending movies
- `GET /movie/{id}` — fetch a movie by TMDB ID
- `GET /industries` — list supported industry tags
- `GET /languages` — list supported language codes
- `POST /industry/recommendations` — recommendations by industry
- `POST /language/recommendations` — recommendations by language

## Frontend
The frontend is a Next.js application with a home search page, detailed recommendation overlays, and movie detail pages.

## Project Structure
```
├── backend/
│   ├── main.py              # FastAPI app and API routes
│   ├── config.py            # environment config and settings
│   ├── tmdb_fetcher.py      # TMDB API client
│   ├── voyage_embeddings.py # Voyage AI embedding client
│   ├── vector_db.py         # Qdrant wrapper
│   ├── recommender.py       # recommendation logic
│   └── data_loader.py       # dataset ingestion and embedding creation
├── frontend/
│   ├── src/
│   │   ├── pages/           # Next.js pages
│   │   ├── components/      # UI components
│   │   └── styles/          # global styles
│   ├── next.config.js
│   ├── package.json
│   ├── tsconfig.json
│   └── tailwind.config.ts
└── requirements.txt
```

## Notes
- The system supports multiple movie industries and languages out-of-the-box.


