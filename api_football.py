# api_football.py — WC26 Live Football API
import streamlit as st
import requests

API_HOST = "wc26-live-football-api.p.rapidapi.com"

STAGE_MAP = {
    "matchday": "gs",
    "group":    "gs",
    "round of 32": "r32",
    "round of 16": "r16",
    "quarter":  "qf",
    "semi":     "sf",
    "third":    "3p",
    "final":    "f",
}

FINISHED_STATUSES = {"FT", "AET", "PEN", "ft", "aet", "pen"}

# API team name → our matches.py team name
TEAM_NAME_MAP = {
    "Czech Republic": "Czechia",
    "Türkiye":        "Türkiye",
    "Turkey":         "Türkiye",
    "Ivory Coast":    "Ivory Coast",
    "Cote d'Ivoire":  "Ivory Coast",
    "Bosnia":         "Bosnia & Herzegovina",
    "Bosnia and Herzegovina": "Bosnia & Herzegovina",
    "DR Congo":       "DR Congo",
    "Congo DR":       "DR Congo",
    "New Zealand":    "New Zealand",
    "South Korea":    "South Korea",
    "Korea Republic": "South Korea",
    "USA":            "USA",
    "United States":  "USA",
}


def _normalise_team(name: str) -> str:
    return TEAM_NAME_MAP.get(name, name)


def _headers() -> dict:
    return {
        "X-RapidAPI-Key":  st.secrets.get("RAPIDAPI_KEY", ""),
        "X-RapidAPI-Host": API_HOST,
    }


def _get(endpoint: str) -> dict | list | None:
    try:
        r = requests.get(
            f"https://{API_HOST}/{endpoint}",
            headers=_headers(),
            timeout=10,
        )
        return r.json() if r.status_code == 200 else None
    except Exception:
        return None


def is_api_configured() -> bool:
    return bool(st.secrets.get("RAPIDAPI_KEY", "").strip())


@st.cache_data(ttl=86400)
def _fetch_all_matches() -> list[dict]:
    data = _get("matches")
    if not data or not isinstance(data, dict):
        return []
    inner = data.get("data", {})
    if isinstance(inner, list):
        return inner
    if isinstance(inner, dict):
        all_matches = []
        for v in inner.values():
            if isinstance(v, list):
                all_matches.extend(v)
        return all_matches
    return []


@st.cache_data(ttl=86400)
def _fetch_live_matches_raw() -> list[dict]:
    data = _get("live")
    if not data:
        return []
    if isinstance(data, list):
        return data
    inner = data.get("data", data.get("live", []))
    if isinstance(inner, list):
        return inner
    if isinstance(inner, dict):
        all_matches = []
        for v in inner.values():
            if isinstance(v, list):
                all_matches.extend(v)
        return all_matches
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
    home_raw = m.get("home", "")
    away_raw = m.get("away", "")
    if not home_raw or not away_raw:
        return None

    home = _normalise_team(home_raw)
    away = _normalise_team(away_raw)

    # Status at root level
    status = m.get("status", "")
    played = m.get("played", False)

    # Scores from live_data
    live       = m.get("live_data") or {}
    home_score = live.get("score_home")
    away_score = live.get("score_away")

    # Fallback: parse root "score" string e.g. "2-1"
    if home_score is None and m.get("score"):
        try:
            parts = str(m["score"]).split("-")
            home_score = int(parts[0].strip())
            away_score = int(parts[1].strip())
        except Exception:
            pass

    # Stage from root round
    round_str = m.get("round") or ""
    stage = _map_stage(round_str)

    # Penalty winner — infer from goals if PEN
    penalty_winner = None
    if status == "PEN":
        goals = live.get("goals") or []
        home_goals = sum(1 for g in goals if _normalise_team(g.get("team", "")) == home)
        away_goals = sum(1 for g in goals if _normalise_team(g.get("team", "")) == away)
        penalty_winner = "home" if home_goals > away_goals else "away"

    return {
        "api_id":         m.get("id"),
        "home":           home,
        "away":           away,
        "home_score":     int(home_score) if home_score is not None else None,
        "away_score":     int(away_score) if away_score is not None else None,
        "status":         status,
        "played":         played,
        "stage":          stage,
        "round":          round_str,
        "penalty_winner": penalty_winner,
    }


def get_finished_results() -> list[dict]:
    _fetch_all_matches.clear()  # force fresh fetch on manual sync
    out = []
    for m in _fetch_all_matches():
        p = _parse_match(m)
        if not p:
            continue
        is_finished = p["status"] in FINISHED_STATUSES or p.get("played")
        if is_finished and p["home_score"] is not None and p["stage"]:
            out.append(p)
    return out


def get_upcoming_with_teams() -> list[dict]:
    _fetch_all_matches.clear()  # force fresh fetch on manual sync
    out = []
    for m in _fetch_all_matches():
        p = _parse_match(m)
        if not p or not p["stage"] or p["stage"] == "gs":
            continue
        if p.get("played") or p["status"] in FINISHED_STATUSES:
            continue
        if "tbd" in p["home"].lower() or "tbd" in p["away"].lower():
            continue
        out.append(p)
    return out


def any_live_now() -> bool:
    return bool(_fetch_live_matches_raw())


def get_live_matches() -> list[dict]:
    return [p for m in _fetch_live_matches_raw() if (p := _parse_match(m))]
