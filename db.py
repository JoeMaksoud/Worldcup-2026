# db.py — Supabase client + all data access helpers
import streamlit as st
from supabase import create_client, Client
import bcrypt


@st.cache_resource
def get_client() -> Client:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_ANON_KEY"]
    return create_client(url, key)


# ── AUTH ──────────────────────────────────────────────────────────────────────

def register_user(username: str, password: str) -> dict | None:
    """Create a new user. Returns user dict or None if username taken."""
    db = get_client()
    existing = db.table("users").select("id").eq("username", username).execute()
    if existing.data:
        return None
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    # First user becomes admin
    count = db.table("users").select("id", count="exact").execute()
    is_admin = (count.count == 0)
    result = db.table("users").insert({
        "username": username,
        "password_hash": hashed,
        "is_admin": is_admin,
    }).execute()
    return result.data[0] if result.data else None


def login_user(username: str, password: str) -> dict | None:
    """Verify credentials. Returns user dict or None."""
    db = get_client()
    result = db.table("users").select("*").eq("username", username).execute()
    if not result.data:
        return None
    user = result.data[0]
    if bcrypt.checkpw(password.encode(), user["password_hash"].encode()):
        return user
    return None


def get_all_users() -> list[dict]:
    db = get_client()
    return db.table("users").select("id, username, is_admin").execute().data


# ── PREDICTIONS ───────────────────────────────────────────────────────────────

def save_prediction(user_id: str, match_id: int, home_score: int,
                    away_score: int, penalty_winner: str | None) -> None:
    db = get_client()
    db.table("predictions").upsert({
        "user_id": user_id,
        "match_id": match_id,
        "home_score": home_score,
        "away_score": away_score,
        "penalty_winner": penalty_winner,
    }, on_conflict="user_id,match_id").execute()


def get_predictions_for_user(user_id: str) -> dict[int, dict]:
    """Returns {match_id: prediction_dict}"""
    db = get_client()
    rows = db.table("predictions").select("*").eq("user_id", user_id).execute().data
    return {r["match_id"]: r for r in rows}


def get_all_predictions() -> list[dict]:
    db = get_client()
    return db.table("predictions").select("*").execute().data


# ── RESULTS ───────────────────────────────────────────────────────────────────

def save_result(match_id: int, home_score: int,
                away_score: int, penalty_winner: str | None) -> None:
    db = get_client()
    db.table("results").upsert({
        "match_id": match_id,
        "home_score": home_score,
        "away_score": away_score,
        "penalty_winner": penalty_winner,
    }, on_conflict="match_id").execute()


@st.cache_data(ttl=60)
def get_all_results() -> dict[int, dict]:
    """Returns {match_id: result_dict}. Cached for 60 s."""
    db = get_client()
    rows = db.table("results").select("*").execute().data
    return {r["match_id"]: r for r in rows}
