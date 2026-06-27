# api_football.py — WC26 Live Football API (rapidapi.com/Emiledaou/api/wc26-live-football-api)
import streamlit as st
import requests
from datetime import datetime, timezone, timedelta

DUBAI    = timezone(timedelta(hours=4))
API_HOST = "wc26-live-football-api.p.rapidapi.com"

STAGE_MAP = {
    "group":       "gs",
    "round of 32": "r32",
    "round of 16": "r16",
    "quarter":     "qf",
    "semi":        "sf",
    "third":       "3p",
    "final":       "f",
}

FINISHED_STATUSES = {"FT","AET","PEN","finished","Finished","FINISHED","ft","aet","pen"}
LIVE_STATUSES     = {"1H","HT","2H","ET","BT","P","SUSP","INT","LIVE","live","Live"}


def _headers() -> dict:
    return {
        "X-RapidAPI-Key":  st.secrets.get("RAPIDAPI_KEY", ""),
        "X-RapidAPI-Host": API_HOST,
    }


def _get(endpoint: str, params: dict | None = None) -> dict | list | None:
    try:
        r = requests.get(
            f"https://{API_HOST}/{endpoint}",
            headers=_headers(),
            params=params or {},
            timeout=10,
        )
        return r.json() if r.status_code == 200 else None
    except Exception:
        return None


def is_api_configured() -> bool:
    return bool(st.secrets.get("RAPIDAPI_KEY", "").strip())


@st.cache_data(ttl=300)
def _fetch_all_matches() -> list[dict]:
    data = _get("matches")
    if not data:
        return []
    if isinstance(data, list):
        return data
    for key in ("matches", "fixtures", "data", "results"):
        if key in data and isinstance(data[key], list):
            return data[key]
    return []


@st.cache_data(ttl=60)
def _fetch_live_matches_raw() -> list[dict]:
    data = _get("live")
    if not data:
        return []
    if isinstance(data, list):
        return data
    for key in ("matches", "live", "data"):
        if key in data and isinstance(data[key], list):
            return data[key]
    return []


def _map_stage(round_str: str) -> str | None:
    r = (round_str or "").lower()
    for key, val in STAGE_MAP.items():
        if key in r:
            if key == "final" and any(x in r for x in ("semi", "quarter", "third")):
                continue
            return val
    return None


def _parse_match(m: dict) -> dict | None:
    # Normalise team names
    home_raw = m.get("home_team") or m.get("homeTeam") or m.get("home") or {}
    away_raw = m.get("away_team") or m.get("awayTeam") or m.get("away") or {}
    home_name = home_raw.get("name") if isinstance(home_raw, dict) else str(home_raw)
    away_name = away_raw.get("name") if isinstance(away_raw, dict) else str(away_raw)
    if not home_name or not away_name:
        return None

    # Normalise score
    score_raw  = m.get("score") or m.get("goals") or {}
    home_score = score_raw.get("home") if isinstance(score_raw, dict) else m.get("home_score")
    away_score = score_raw.get("away") if isinstance(score_raw, dict) else m.get("away_score")

    # Normalise status
    status_raw = m.get("status") or m.get("match_status") or ""
    status = status_raw.get("short") or status_raw.get("long", "") if isinstance(status_raw, dict) else str(status_raw)

    # Normalise round/stage
    round_raw  = m.get("round") or m.get("stage") or ""
    if isinstance(round_raw, dict):
        round_raw = round_raw.get("name") or ""
    if not round_raw and isinstance(m.get("league"), dict):
        round_raw = m["league"].get("round", "")
    stage = _map_stage(str(round_raw))

    # Penalty winner
    penalty_winner = None
    if isinstance(score_raw, dict):
        pen = score_raw.get("penalty") or {}
        if isinstance(pen, dict):
            hp = pen.get("home") or 0
            ap = pen.get("away") or 0
            if hp != ap:
                penalty_winner = "home" if hp > ap else "away"

    return {
        "api_id":         m.get("id") or m.get("fixture_id") or m.get("match_id"),
        "home":           home_name,
        "away":           away_name,
        "home_score":     int(home_score) if home_score is not None else None,
        "away_score":     int(away_score) if away_score is not None else None,
        "status":         status,
        "stage":          stage,
        "round":          str(round_raw),
        "penalty_winner": penalty_winner,
    }


def get_finished_results() -> list[dict]:
    out = []
    for m in _fetch_all_matches():
        p = _parse_match(m)
        if p and p["status"] in FINISHED_STATUSES and p["home_score"] is not None and p["stage"]:
            out.append(p)
    return out


def get_upcoming_with_teams() -> list[dict]:
    out = []
    for m in _fetch_all_matches():
        p = _parse_match(m)
        if not p or not p["stage"] or p["stage"] == "gs":
            continue
        if p["status"] in FINISHED_STATUSES:
            continue
        if "tbd" in p["home"].lower() or "tbd" in p["away"].lower():
            continue
        out.append(p)
    return out


def any_live_now() -> bool:
    return bool(_fetch_live_matches_raw())


def get_live_matches() -> list[dict]:
    return [p for m in _fetch_live_matches_raw() if (p := _parse_match(m))]
