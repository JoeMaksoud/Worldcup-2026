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
    db = get_client()
    existing = db.table("users").select("id").eq("username", username).execute()
    if existing.data:
        return None
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    count = db.table("users").select("id", count="exact").execute()
    is_admin = (count.count == 0)
    result = db.table("users").insert({
        "username": username,
        "password_hash": hashed,
        "is_admin": is_admin,
    }).execute()
    return result.data[0] if result.data else None


def login_user(username: str, password: str) -> dict | None:
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
        "user_id":        user_id,
        "match_id":       match_id,
        "home_score":     home_score,
        "away_score":     away_score,
        "penalty_winner": penalty_winner,
    }, on_conflict="user_id,match_id").execute()


def get_predictions_for_user(user_id: str) -> dict[int, dict]:
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
        "match_id":       match_id,
        "home_score":     home_score,
        "away_score":     away_score,
        "penalty_winner": penalty_winner,
        "manual_override": False,
    }, on_conflict="match_id").execute()


def save_result_manual(match_id: int, home_score: int,
                       away_score: int, penalty_winner: str | None) -> None:
    """Admin manual entry — sets manual_override=True so API won't overwrite."""
    db = get_client()
    db.table("results").upsert({
        "match_id":        match_id,
        "home_score":      home_score,
        "away_score":      away_score,
        "penalty_winner":  penalty_winner,
        "manual_override": True,
    }, on_conflict="match_id").execute()


def clear_manual_override(match_id: int) -> None:
    """Let API take back control for this match."""
    db = get_client()
    db.table("results").update(
        {"manual_override": False}
    ).eq("match_id", match_id).execute()


def get_all_results() -> dict[int, dict]:
    db = get_client()
    rows = db.table("results").select("*").execute().data
    return {r["match_id"]: r for r in rows}


# ── MATCH TEAM OVERRIDES (knockout bracket) ───────────────────────────────────

def get_match_overrides() -> dict[int, dict]:
    """Returns {match_id: {home, away}} for knockout matches where teams are now known."""
    db = get_client()
    rows = db.table("match_overrides").select("*").execute().data
    return {r["match_id"]: r for r in rows}


def save_match_override(match_id: int, home: str, away: str) -> None:
    db = get_client()
    db.table("match_overrides").upsert({
        "match_id": match_id,
        "home": home,
        "away": away,
    }, on_conflict="match_id").execute()


# ── API SYNC ──────────────────────────────────────────────────────────────────

def sync_results_from_api(api_results: list[dict], our_matches: list[dict]) -> tuple[int, int]:
    """
    Match API results to our match IDs using api_id directly (WC26 API uses same IDs as us).
    Falls back to fuzzy name matching if needed.
    Skips matches with manual_override=True.
    Returns (synced_count, skipped_count).
    """
    existing = get_all_results()
    our_match_ids = {m["id"] for m in our_matches}
    synced = skipped = 0

    for api_r in api_results:
        # Try direct ID match first
        mid = api_r.get("api_id")
        if mid not in our_match_ids:
            # Fall back to name matching
            match = _find_match(api_r, our_matches)
            mid = match["id"] if match else None
        if not mid:
            continue

        # Skip if admin has manually overridden this result
        if existing.get(mid, {}).get("manual_override"):
            skipped += 1
            continue

        save_result(mid, api_r["home_score"], api_r["away_score"], api_r["penalty_winner"])
        synced += 1

    return synced, skipped


def sync_teams_from_api(api_upcoming: list[dict], our_matches: list[dict]) -> int:
    """Update knockout match team names from API once teams are confirmed."""
    updated = 0
    for api_f in api_upcoming:
        match = _find_match_by_stage_and_teams(api_f, our_matches)
        if not match:
            continue
        save_match_override(match["id"], api_f["home"], api_f["away"])
        updated += 1
    return updated


def _find_match(api_r: dict, our_matches: list[dict]) -> dict | None:
    """Find our match record by fuzzy team name match + stage."""
    api_home = api_r["home"].lower()
    api_away = api_r["away"].lower()
    stage    = api_r["stage"]
    for m in our_matches:
        if m["stage"] != stage:
            continue
        if (api_home in m["home"].lower() or m["home"].lower() in api_home) and \
           (api_away in m["away"].lower() or m["away"].lower() in api_away):
            return m
    return None


def _find_match_by_stage_and_teams(api_f: dict, our_matches: list[dict]) -> dict | None:
    """Find a TBD knockout match slot by stage — simplistic first-available."""
    stage = api_f["stage"]
    for m in our_matches:
        if m["stage"] == stage and ("TBD" in m.get("home", "") or
                                     "TBD" in m.get("away", "") or
                                     m["home"].startswith("W") or
                                     m["home"].startswith("QF") or
                                     m["home"].startswith("SF")):
            return m
    return None
