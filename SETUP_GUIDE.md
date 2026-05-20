# 🎬 Movie Recommender GenAI - Complete Setup Guide

## ✅ Prerequisites Check

Your system needs:
- **Python 3.10+** - [Download](https://www.python.org/downloads/)
- **Node.js 16+** - [Download](https://nodejs.org/)
- **Git** (optional, for version control)

Verify installation:
```bash
python --version
node --version
npm --version
```

---

## 🔑 API Keys Configuration

All API keys are already configured in `.env`. Verify they're set:

```bash
cat .env
```

Should include:
- ✅ `TMDB_API_KEY` - The Movie Database API
- ✅ `VOYAGE_API_KEY` - Voyage AI embeddings
- ✅ `GEMINI_API_KEY` - Google Gemini LLM

---

## 🚀 Quick Start

### Option 1: PowerShell Scripts (Recommended on Windows)

**Terminal 1 - Backend:**
```powershell
.\run_backend.ps1
```

**Terminal 2 - Frontend:**
```powershell
.\run_frontend.ps1
```

Then visit: **http://localhost:3000**

---

### Option 2: Manual Setup

#### Backend Setup
```bash
# Create virtual environment
python -m venv venv

# Activate it (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Or Command Prompt:
venv\Scripts\activate.bat

# Install dependencies
pip install -r requirements.txt

# Start FastAPI server
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

**Backend will be ready at:**
- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

#### Frontend Setup
```bash
cd frontend

# Install dependencies (only first time)
npm install

# Start dev server
npm run dev
```

**Frontend will be ready at:**
- App: http://localhost:3000

---

## 📋 Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                   Frontend (Next.js)                    │
│              http://localhost:3000                      │
│  - Search page with semantic recommendations            │
│  - Movie detail pages                                   │
└──────────────────────┬──────────────────────────────────┘
                       │ axios (HTTP)
                       ↓
┌─────────────────────────────────────────────────────────┐
│                Backend (FastAPI)                        │
│            http://localhost:8000                        │
├─────────────────────────────────────────────────────────┤
│ POST /recommend    → RecommenderEngine                  │
│                    ├→ Voyage AI (embeddings)            │
│                    ├→ ChromaDB (vector search)          │
│                    └→ Gemini (explanations)             │
│                                                         │
│ GET /movies/trending → TMDB API                        │
│ GET /movie/{id}    → TMDB API + Vector Store           │
└─────────────────────────────────────────────────────────┘
```

---

## 📝 API Endpoints

### Search & Recommendations
```bash
POST /recommend
Content-Type: application/json

{
  "query": "mind-bending sci-fi about time travel"
}

# Returns top 10 movies with AI explanations
```

### Trending Movies
```bash
GET /movies/trending?page=1

# Returns trending movies from TMDB
```

### Movie Details
```bash
GET /movie/550

# Returns detailed info about Fight Club (ID: 550)
```

---

## 🔄 First Run

**On first startup, the backend will:**
1. Initialize ChromaDB vector store
2. Fetch trending movies from TMDB (~40 movies)
3. Generate embeddings using Voyage AI
4. Store everything for fast semantic search

This takes ~30-60 seconds. You'll see:
```
INFO:     Started server process [...]
INFO:     Application startup complete
Loading initial dataset...
[████████████████████] 100% - Loaded 40 movies
```

---

## 🧪 Testing the System

### Test Backend API (in PowerShell or terminal):
```bash
# Test recommendation endpoint
curl -X POST http://localhost:8000/recommend `
  -H "Content-Type: application/json" `
  -d "{\"query\": \"funny movies about friendship\"}"

# Interactive API docs
# Visit: http://localhost:8000/docs
```

---

## ⚙️ Environment Variables

### Backend (.env)
```env
TMDB_API_KEY=your_key_here
VOYAGE_API_KEY=your_key_here
GEMINI_API_KEY=your_key_here
EMBEDDING_PROVIDER=voyage
CHROMA_PERSIST_DIR=./chroma_db
```

### Frontend (frontend/.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## 🐛 Troubleshooting

### Backend won't start
```bash
# Check if port 8000 is in use
netstat -ano | findstr :8000

# Kill process on port 8000 (Windows)
taskkill /PID <PID> /F

# Try different port
python -m uvicorn backend.main:app --port 8001
# Then update frontend: NEXT_PUBLIC_API_URL=http://localhost:8001
```

### Frontend can't connect to backend
- Check if backend is running: `http://localhost:8000/docs`
- Check `NEXT_PUBLIC_API_URL` in `frontend/.env.local`
- Check CORS headers in browser console (F12 → Network tab)

### Out of memory / slow response
- ChromaDB defaults to in-memory + persistence
- First query takes longer (loading vector store)
- Subsequent queries are cached

### API key errors
```bash
# Verify keys are loaded
python -c "from backend.config import settings; print(settings.TMDB_API_KEY[:10])"
```

---

## 📊 Performance Tips

1. **First Query is Slower**: ChromaDB loads the vector store (~2-5s)
2. **Subsequent Queries**: ~500ms with semantic search
3. **Gemini Responses**: Add 2-5 seconds for AI explanations
4. **Increase Performance**:
   - Close other apps
   - Use Chrome/Edge (better performance)
   - Increase vector store with more TMDB data

---

## 🎯 Next Steps

1. ✅ **Run the project**: Use the startup scripts
2. 🔍 **Try the search**: Enter queries like:
   - "A feel-good comedy about romance"
   - "Dark, twisted thriller with plot twists"
   - "Animated movies for kids"
3.  **Explore the API**: Visit http://localhost:8000/docs

---

## 🛠️ Development

### Backend File Structure
```
backend/
├── main.py              # FastAPI app & endpoints
├── config.py            # Settings & environment
├── recommender.py       # Core recommendation logic
├── voyage_embeddings.py # Voyage AI client
├── vector_db.py         # ChromaDB wrapper
├── tmdb_fetcher.py      # TMDB API client
├── gemini_explainer.py  # Gemini explanation generation
└── __init__.py
```

### Frontend File Structure
```
frontend/
├── src/
│   ├── pages/
│   │   ├── index.tsx         # Home page (search)
│   │   └── movie/[id].tsx    # Movie detail page
│   ├── components/
│   │   ├── SearchBar.tsx     # Search interface
│   │   ├── MovieCard.tsx     # Movie display
│   │   ├── Carousel.tsx      # Carousel component
│   │   └── Header.tsx        # Navigation
│   └── styles/
│       └── globals.css       # Tailwind + custom styles
└── next.config.js
```

---

## 📞 Support

For issues:
1. Check this guide's Troubleshooting section
2. Review API docs: http://localhost:8000/docs
3. Check browser console (F12) for frontend errors
4. Check terminal output for backend logs

---

**Enjoy your AI-powered movie recommendations! 🎬🍿**
