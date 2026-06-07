# ⚽ WC2026 Prediction League

A Streamlit web app for running a FIFA World Cup 2026 prediction game with friends.

## Features
- 🔐 User accounts (register / login with hashed passwords)
- 📅 Match calendar with all 104 games — kickoff times in **Dubai time (UTC+4)**
- ✍️ Predict scores for every match; edit until 30 min before kickoff
- 🎯 Knockout draw predictions → penalty shootout winner picker
- 🏆 Live leaderboard with auto-calculated points
- ⚙️ Admin panel to enter results (first registered user = admin)

## Scoring

| Stage | Correct Winner | Exact Score |
|---|---|---|
| Group Stage, R32, R16 | 1 pt | 3 pts |
| Quarter-finals & 3rd Place | 2 pts | 6 pts |
| Semi-finals | 3 pts | 9 pts |
| Final | 4 pts | 12 pts |

Entry fee: **5 AED per match** (104 matches = 520 AED per player)

---

## Setup Guide

### Step 1 — Supabase (database)

1. Go to [supabase.com](https://supabase.com) and create a free account
2. Click **New Project**, give it a name (e.g. `wc2026`), set a strong DB password, choose a region close to Dubai (e.g. `ap-southeast-1` Singapore)
3. Once the project is ready, go to **SQL Editor** → **New Query**
4. Paste the entire contents of `supabase_schema.sql` and click **Run**
5. Go to **Project Settings → API** and copy:
   - `Project URL` → this is your `SUPABASE_URL`
   - `anon / public` key → this is your `SUPABASE_ANON_KEY`

### Step 2 — GitHub (code hosting)

1. Go to [github.com](https://github.com) and create a free account (if you don't have one)
2. Click **New repository**, name it `wc2026-predictor`, set it to **Public** (required for free Streamlit Cloud)
3. Upload all files from this folder to the repo (drag & drop in the GitHub UI, or use `git push`)
4. **Important:** do NOT upload `.streamlit/secrets.toml` — it's in `.gitignore` for a reason

### Step 3 — Streamlit Cloud (hosting)

1. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with your GitHub account
2. Click **New app**
3. Select your `wc2026-predictor` repo, branch `main`, main file `app.py`
4. Before deploying, click **Advanced settings → Secrets** and paste:

```toml
SUPABASE_URL = "https://YOUR_PROJECT_ID.supabase.co"
SUPABASE_ANON_KEY = "your-anon-key-here"
```

5. Click **Deploy** — it'll be live in ~2 minutes at a URL like `https://yourname-wc2026-predictor-app-xxxx.streamlit.app`

### Step 4 — Share with friends

Send everyone the Streamlit URL. The **first person to register** automatically becomes admin.

---

## File Structure

```
wc2026-predictor/
├── app.py                  # Main entry point, auth, navigation
├── db.py                   # Supabase client + all data helpers
├── matches.py              # All 104 matches + scoring logic
├── requirements.txt        # Python dependencies
├── supabase_schema.sql     # Run once in Supabase SQL Editor
├── .gitignore
├── .streamlit/
│   ├── config.toml         # Theme (dark, gold accent)
│   └── secrets.toml        # NOT in git — add via Streamlit Cloud UI
└── pages/
    ├── calendar.py         # Match calendar + prediction forms
    ├── leaderboard.py      # Live standings
    └── admin.py            # Result entry panel
```
