# ⚡ Quick Start - Movie Recommender GenAI

## 🎯 In 2 Minutes

### Step 1: Open Two PowerShell Terminals

**Terminal 1 - Backend:**
```powershell
cd a:\Projects\Movie recommor genai
.\run_backend.ps1
```

Wait for: `Application startup complete`

**Terminal 2 - Frontend:**
```powershell
cd a:\Projects\Movie recommor genai
.\run_frontend.ps1
```

Wait for: `ready - started server on 0.0.0.0:3000`

### Step 2: Open Browser
Go to **http://localhost:3000**

---

## 🎬 What You Can Do

### 🔍 **Search Page** (Home)
- Enter: "A mind-bending sci-fi thriller about time travel"
- Get: 10 movies with AI-written explanations why they match

### 🎞️ **Movie Details**
- Click any movie card to see full details
- Shows rating, overview, genres, and poster

---

## ✅ Verification

### Backend Working?
Visit: **http://localhost:8000/docs**
- Try POST `/recommend` with query "funny movies"
- Should return movie recommendations

### Frontend Working?
Visit: **http://localhost:3000**
- Type in search box
- Should see loading then results

---

## 🛠️ If Something Doesn't Work

**Backend won't start:**
- Check Python installed: `python --version`
- Check port 8000 free: `netstat -ano | findstr :8000`
- Check .env file exists with API keys

**Frontend won't load:**
- Check Node.js installed: `node --version`
- Delete `frontend/node_modules` and rerun `npm install`
- Check `.env.local` has `NEXT_PUBLIC_API_URL=http://localhost:8000`

**No recommendations showing:**
- Wait 30 seconds (first load initializes database)
- Check browser console (F12) for errors
- Check backend terminal for errors

---

## 📚 Full Documentation
See `SETUP_GUIDE.md` for complete setup instructions and troubleshooting.

---

**That's it! Enjoy! 🎬🍿**
