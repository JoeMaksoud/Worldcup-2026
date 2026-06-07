# matches.py — All 104 FIFA World Cup 2026 matches, kickoff times in Dubai (UTC+4)

MATCHES = [
    # ── GROUP STAGE ──────────────────────────────────────────────
    {"id": 1,  "date": "2026-06-11", "time": "23:00", "stage": "gs",  "group": "A", "home": "Mexico",              "away": "South Africa",       "venue": "Estadio Azteca, Mexico City"},
    {"id": 2,  "date": "2026-06-12", "time": "06:00", "stage": "gs",  "group": "A", "home": "South Korea",         "away": "Czechia",            "venue": "Estadio Akron, Zapopan"},
    {"id": 3,  "date": "2026-06-12", "time": "23:00", "stage": "gs",  "group": "B", "home": "Canada",              "away": "Bosnia & Herzegovina","venue": "BMO Field, Toronto"},
    {"id": 4,  "date": "2026-06-13", "time": "05:00", "stage": "gs",  "group": "D", "home": "USA",                 "away": "Paraguay",           "venue": "SoFi Stadium, Inglewood"},
    {"id": 5,  "date": "2026-06-13", "time": "23:00", "stage": "gs",  "group": "B", "home": "Qatar",               "away": "Switzerland",        "venue": "Levi's Stadium, Santa Clara"},
    {"id": 6,  "date": "2026-06-14", "time": "02:00", "stage": "gs",  "group": "C", "home": "Brazil",              "away": "Morocco",            "venue": "MetLife Stadium, East Rutherford"},
    {"id": 7,  "date": "2026-06-14", "time": "05:00", "stage": "gs",  "group": "C", "home": "Haiti",               "away": "Scotland",           "venue": "Gillette Stadium, Foxborough"},
    {"id": 8,  "date": "2026-06-14", "time": "08:00", "stage": "gs",  "group": "D", "home": "Australia",           "away": "Türkiye",            "venue": "BC Place, Vancouver"},
    {"id": 9,  "date": "2026-06-14", "time": "21:00", "stage": "gs",  "group": "E", "home": "Germany",             "away": "Curaçao",            "venue": "NRG Stadium, Houston"},
    {"id": 10, "date": "2026-06-15", "time": "00:00", "stage": "gs",  "group": "F", "home": "Netherlands",         "away": "Japan",              "venue": "AT&T Stadium, Arlington"},
    {"id": 11, "date": "2026-06-15", "time": "03:00", "stage": "gs",  "group": "E", "home": "Ivory Coast",         "away": "Ecuador",            "venue": "Lincoln Financial Field, Philadelphia"},
    {"id": 12, "date": "2026-06-15", "time": "06:00", "stage": "gs",  "group": "F", "home": "Sweden",              "away": "Tunisia",            "venue": "Estadio BBVA, Monterrey"},
    {"id": 13, "date": "2026-06-15", "time": "20:00", "stage": "gs",  "group": "H", "home": "Spain",               "away": "Cape Verde",         "venue": "Mercedes-Benz Stadium, Atlanta"},
    {"id": 14, "date": "2026-06-15", "time": "23:00", "stage": "gs",  "group": "G", "home": "Belgium",             "away": "Egypt",              "venue": "Lumen Field, Seattle"},
    {"id": 15, "date": "2026-06-16", "time": "02:00", "stage": "gs",  "group": "H", "home": "Saudi Arabia",        "away": "Uruguay",            "venue": "Hard Rock Stadium, Miami Gardens"},
    {"id": 16, "date": "2026-06-16", "time": "05:00", "stage": "gs",  "group": "G", "home": "Iran",                "away": "New Zealand",        "venue": "SoFi Stadium, Inglewood"},
    {"id": 17, "date": "2026-06-16", "time": "23:00", "stage": "gs",  "group": "I", "home": "France",              "away": "Senegal",            "venue": "MetLife Stadium, East Rutherford"},
    {"id": 18, "date": "2026-06-17", "time": "02:00", "stage": "gs",  "group": "I", "home": "Iraq",                "away": "Norway",             "venue": "Gillette Stadium, Foxborough"},
    {"id": 19, "date": "2026-06-17", "time": "05:00", "stage": "gs",  "group": "J", "home": "Argentina",           "away": "Algeria",            "venue": "Arrowhead Stadium, Kansas City"},
    {"id": 20, "date": "2026-06-17", "time": "08:00", "stage": "gs",  "group": "J", "home": "Austria",             "away": "Jordan",             "venue": "Levi's Stadium, Santa Clara"},
    {"id": 21, "date": "2026-06-17", "time": "21:00", "stage": "gs",  "group": "K", "home": "Portugal",            "away": "DR Congo",           "venue": "NRG Stadium, Houston"},
    {"id": 22, "date": "2026-06-18", "time": "00:00", "stage": "gs",  "group": "L", "home": "England",             "away": "Croatia",            "venue": "AT&T Stadium, Arlington"},
    {"id": 23, "date": "2026-06-18", "time": "03:00", "stage": "gs",  "group": "L", "home": "Ghana",               "away": "Panama",             "venue": "BMO Field, Toronto"},
    {"id": 24, "date": "2026-06-18", "time": "06:00", "stage": "gs",  "group": "K", "home": "Uzbekistan",          "away": "Colombia",           "venue": "Estadio Azteca, Mexico City"},
    {"id": 25, "date": "2026-06-18", "time": "20:00", "stage": "gs",  "group": "A", "home": "Czechia",             "away": "South Africa",       "venue": "Mercedes-Benz Stadium, Atlanta"},
    {"id": 26, "date": "2026-06-18", "time": "23:00", "stage": "gs",  "group": "B", "home": "Switzerland",         "away": "Bosnia & Herzegovina","venue": "SoFi Stadium, Inglewood"},
    {"id": 27, "date": "2026-06-19", "time": "02:00", "stage": "gs",  "group": "B", "home": "Canada",              "away": "Qatar",              "venue": "BC Place, Vancouver"},
    {"id": 28, "date": "2026-06-19", "time": "05:00", "stage": "gs",  "group": "A", "home": "Mexico",              "away": "South Korea",        "venue": "Estadio Akron, Zapopan"},
    {"id": 29, "date": "2026-06-19", "time": "23:00", "stage": "gs",  "group": "D", "home": "USA",                 "away": "Australia",          "venue": "Lumen Field, Seattle"},
    {"id": 30, "date": "2026-06-20", "time": "02:00", "stage": "gs",  "group": "C", "home": "Scotland",            "away": "Morocco",            "venue": "Gillette Stadium, Foxborough"},
    {"id": 31, "date": "2026-06-20", "time": "04:30", "stage": "gs",  "group": "C", "home": "Brazil",              "away": "Haiti",              "venue": "Lincoln Financial Field, Philadelphia"},
    {"id": 32, "date": "2026-06-20", "time": "07:00", "stage": "gs",  "group": "D", "home": "Türkiye",             "away": "Paraguay",           "venue": "Levi's Stadium, Santa Clara"},
    {"id": 33, "date": "2026-06-20", "time": "21:00", "stage": "gs",  "group": "F", "home": "Netherlands",         "away": "Sweden",             "venue": "NRG Stadium, Houston"},
    {"id": 34, "date": "2026-06-21", "time": "00:00", "stage": "gs",  "group": "E", "home": "Germany",             "away": "Ivory Coast",        "venue": "BMO Field, Toronto"},
    {"id": 35, "date": "2026-06-21", "time": "04:00", "stage": "gs",  "group": "E", "home": "Ecuador",             "away": "Curaçao",            "venue": "Arrowhead Stadium, Kansas City"},
    {"id": 36, "date": "2026-06-21", "time": "08:00", "stage": "gs",  "group": "F", "home": "Tunisia",             "away": "Japan",              "venue": "Estadio BBVA, Monterrey"},
    {"id": 37, "date": "2026-06-21", "time": "20:00", "stage": "gs",  "group": "H", "home": "Spain",               "away": "Saudi Arabia",       "venue": "Mercedes-Benz Stadium, Atlanta"},
    {"id": 38, "date": "2026-06-21", "time": "23:00", "stage": "gs",  "group": "G", "home": "Belgium",             "away": "Iran",               "venue": "SoFi Stadium, Inglewood"},
    {"id": 39, "date": "2026-06-22", "time": "02:00", "stage": "gs",  "group": "H", "home": "Uruguay",             "away": "Cape Verde",         "venue": "Hard Rock Stadium, Miami Gardens"},
    {"id": 40, "date": "2026-06-22", "time": "05:00", "stage": "gs",  "group": "G", "home": "New Zealand",         "away": "Egypt",              "venue": "BC Place, Vancouver"},
    {"id": 41, "date": "2026-06-22", "time": "21:00", "stage": "gs",  "group": "J", "home": "Argentina",           "away": "Austria",            "venue": "AT&T Stadium, Arlington"},
    {"id": 42, "date": "2026-06-23", "time": "01:00", "stage": "gs",  "group": "I", "home": "France",              "away": "Iraq",               "venue": "Lincoln Financial Field, Philadelphia"},
    {"id": 43, "date": "2026-06-23", "time": "04:00", "stage": "gs",  "group": "I", "home": "Norway",              "away": "Senegal",            "venue": "MetLife Stadium, East Rutherford"},
    {"id": 44, "date": "2026-06-23", "time": "07:00", "stage": "gs",  "group": "J", "home": "Jordan",              "away": "Algeria",            "venue": "Levi's Stadium, Santa Clara"},
    {"id": 45, "date": "2026-06-23", "time": "21:00", "stage": "gs",  "group": "K", "home": "Portugal",            "away": "Uzbekistan",         "venue": "NRG Stadium, Houston"},
    {"id": 46, "date": "2026-06-24", "time": "00:00", "stage": "gs",  "group": "L", "home": "England",             "away": "Ghana",              "venue": "Gillette Stadium, Foxborough"},
    {"id": 47, "date": "2026-06-24", "time": "03:00", "stage": "gs",  "group": "L", "home": "Panama",              "away": "Croatia",            "venue": "BMO Field, Toronto"},
    {"id": 48, "date": "2026-06-24", "time": "06:00", "stage": "gs",  "group": "K", "home": "Colombia",            "away": "DR Congo",           "venue": "Estadio Akron, Zapopan"},
    {"id": 49, "date": "2026-06-24", "time": "23:00", "stage": "gs",  "group": "B", "home": "Switzerland",         "away": "Canada",             "venue": "BC Place, Vancouver"},
    {"id": 50, "date": "2026-06-24", "time": "23:00", "stage": "gs",  "group": "B", "home": "Bosnia & Herzegovina","away": "Qatar",              "venue": "Lumen Field, Seattle"},
    {"id": 51, "date": "2026-06-25", "time": "02:00", "stage": "gs",  "group": "C", "home": "Scotland",            "away": "Brazil",             "venue": "Hard Rock Stadium, Miami Gardens"},
    {"id": 52, "date": "2026-06-25", "time": "02:00", "stage": "gs",  "group": "C", "home": "Morocco",             "away": "Haiti",              "venue": "Mercedes-Benz Stadium, Atlanta"},
    {"id": 53, "date": "2026-06-25", "time": "05:00", "stage": "gs",  "group": "A", "home": "Czechia",             "away": "Mexico",             "venue": "Estadio Azteca, Mexico City"},
    {"id": 54, "date": "2026-06-25", "time": "05:00", "stage": "gs",  "group": "A", "home": "South Africa",        "away": "South Korea",        "venue": "Estadio BBVA, Monterrey"},
    {"id": 55, "date": "2026-06-26", "time": "00:00", "stage": "gs",  "group": "E", "home": "Curaçao",             "away": "Ivory Coast",        "venue": "Lincoln Financial Field, Philadelphia"},
    {"id": 56, "date": "2026-06-26", "time": "00:00", "stage": "gs",  "group": "E", "home": "Ecuador",             "away": "Germany",            "venue": "MetLife Stadium, East Rutherford"},
    {"id": 57, "date": "2026-06-26", "time": "03:00", "stage": "gs",  "group": "F", "home": "Japan",               "away": "Sweden",             "venue": "AT&T Stadium, Arlington"},
    {"id": 58, "date": "2026-06-26", "time": "03:00", "stage": "gs",  "group": "F", "home": "Tunisia",             "away": "Netherlands",        "venue": "Arrowhead Stadium, Kansas City"},
    {"id": 59, "date": "2026-06-26", "time": "06:00", "stage": "gs",  "group": "D", "home": "Türkiye",             "away": "USA",                "venue": "SoFi Stadium, Inglewood"},
    {"id": 60, "date": "2026-06-26", "time": "06:00", "stage": "gs",  "group": "D", "home": "Paraguay",            "away": "Australia",          "venue": "Levi's Stadium, Santa Clara"},
    {"id": 61, "date": "2026-06-26", "time": "23:00", "stage": "gs",  "group": "I", "home": "Norway",              "away": "France",             "venue": "Gillette Stadium, Foxborough"},
    {"id": 62, "date": "2026-06-26", "time": "23:00", "stage": "gs",  "group": "I", "home": "Senegal",             "away": "Iraq",               "venue": "BMO Field, Toronto"},
    {"id": 63, "date": "2026-06-27", "time": "04:00", "stage": "gs",  "group": "H", "home": "Cape Verde",          "away": "Saudi Arabia",       "venue": "NRG Stadium, Houston"},
    {"id": 64, "date": "2026-06-27", "time": "04:00", "stage": "gs",  "group": "H", "home": "Uruguay",             "away": "Spain",              "venue": "Estadio Akron, Zapopan"},
    {"id": 65, "date": "2026-06-27", "time": "07:00", "stage": "gs",  "group": "G", "home": "Egypt",               "away": "Iran",               "venue": "Lumen Field, Seattle"},
    {"id": 66, "date": "2026-06-27", "time": "07:00", "stage": "gs",  "group": "G", "home": "New Zealand",         "away": "Belgium",            "venue": "BC Place, Vancouver"},
    {"id": 67, "date": "2026-06-28", "time": "01:00", "stage": "gs",  "group": "L", "home": "Panama",              "away": "England",            "venue": "MetLife Stadium, East Rutherford"},
    {"id": 68, "date": "2026-06-28", "time": "01:00", "stage": "gs",  "group": "L", "home": "Croatia",             "away": "Ghana",              "venue": "Lincoln Financial Field, Philadelphia"},
    {"id": 69, "date": "2026-06-28", "time": "03:30", "stage": "gs",  "group": "K", "home": "Colombia",            "away": "Portugal",           "venue": "Hard Rock Stadium, Miami Gardens"},
    {"id": 70, "date": "2026-06-28", "time": "03:30", "stage": "gs",  "group": "K", "home": "DR Congo",            "away": "Uzbekistan",         "venue": "Mercedes-Benz Stadium, Atlanta"},
    {"id": 71, "date": "2026-06-28", "time": "06:00", "stage": "gs",  "group": "J", "home": "Algeria",             "away": "Austria",            "venue": "Arrowhead Stadium, Kansas City"},
    {"id": 72, "date": "2026-06-28", "time": "06:00", "stage": "gs",  "group": "J", "home": "Jordan",              "away": "Argentina",          "venue": "AT&T Stadium, Arlington"},
    # ── ROUND OF 32 ──────────────────────────────────────────────
    {"id": 73, "date": "2026-06-28", "time": "23:00", "stage": "r32", "home": "Runner-up A",  "away": "Runner-up B",  "venue": "SoFi Stadium, Inglewood"},
    {"id": 74, "date": "2026-06-29", "time": "21:00", "stage": "r32", "home": "Winner C",     "away": "Runner-up F",  "venue": "NRG Stadium, Houston"},
    {"id": 75, "date": "2026-06-30", "time": "00:30", "stage": "r32", "home": "Winner E",     "away": "Best 3rd",     "venue": "Gillette Stadium, Foxborough"},
    {"id": 76, "date": "2026-06-30", "time": "05:00", "stage": "r32", "home": "Winner F",     "away": "Runner-up C",  "venue": "Estadio BBVA, Monterrey"},
    {"id": 77, "date": "2026-06-30", "time": "21:00", "stage": "r32", "home": "Runner-up E",  "away": "Runner-up I",  "venue": "AT&T Stadium, Arlington"},
    {"id": 78, "date": "2026-07-01", "time": "01:00", "stage": "r32", "home": "Winner I",     "away": "Best 3rd",     "venue": "MetLife Stadium, East Rutherford"},
    {"id": 79, "date": "2026-07-01", "time": "05:00", "stage": "r32", "home": "Winner A",     "away": "Best 3rd",     "venue": "Estadio Azteca, Mexico City"},
    {"id": 80, "date": "2026-07-01", "time": "20:00", "stage": "r32", "home": "Winner L",     "away": "Best 3rd",     "venue": "Mercedes-Benz Stadium, Atlanta"},
    {"id": 81, "date": "2026-07-02", "time": "00:00", "stage": "r32", "home": "Winner G",     "away": "Best 3rd",     "venue": "Lumen Field, Seattle"},
    {"id": 82, "date": "2026-07-02", "time": "04:00", "stage": "r32", "home": "Winner D",     "away": "Best 3rd",     "venue": "Levi's Stadium, Santa Clara"},
    {"id": 83, "date": "2026-07-02", "time": "23:00", "stage": "r32", "home": "Winner H",     "away": "Runner-up J",  "venue": "SoFi Stadium, Inglewood"},
    {"id": 84, "date": "2026-07-03", "time": "03:00", "stage": "r32", "home": "Runner-up K",  "away": "Runner-up L",  "venue": "BMO Field, Toronto"},
    {"id": 85, "date": "2026-07-03", "time": "07:00", "stage": "r32", "home": "Winner B",     "away": "Best 3rd",     "venue": "BC Place, Vancouver"},
    {"id": 86, "date": "2026-07-03", "time": "22:00", "stage": "r32", "home": "Runner-up D",  "away": "Runner-up G",  "venue": "AT&T Stadium, Arlington"},
    {"id": 87, "date": "2026-07-04", "time": "02:00", "stage": "r32", "home": "Winner J",     "away": "Runner-up H",  "venue": "Hard Rock Stadium, Miami Gardens"},
    {"id": 88, "date": "2026-07-04", "time": "05:30", "stage": "r32", "home": "Winner K",     "away": "Best 3rd",     "venue": "Arrowhead Stadium, Kansas City"},
    # ── ROUND OF 16 ──────────────────────────────────────────────
    {"id": 89, "date": "2026-07-04", "time": "21:00", "stage": "r16", "home": "W73/W75",  "away": "TBD", "venue": "NRG Stadium, Houston"},
    {"id": 90, "date": "2026-07-05", "time": "01:00", "stage": "r16", "home": "W74/W77",  "away": "TBD", "venue": "Lincoln Financial Field, Philadelphia"},
    {"id": 91, "date": "2026-07-06", "time": "00:00", "stage": "r16", "home": "W76/W78",  "away": "TBD", "venue": "MetLife Stadium, East Rutherford"},
    {"id": 92, "date": "2026-07-06", "time": "04:00", "stage": "r16", "home": "W79/W80",  "away": "TBD", "venue": "AT&T Stadium, Arlington"},
    {"id": 93, "date": "2026-07-07", "time": "00:00", "stage": "r16", "home": "W81/W83",  "away": "TBD", "venue": "SoFi Stadium, Inglewood"},
    {"id": 94, "date": "2026-07-07", "time": "04:00", "stage": "r16", "home": "W82/W84",  "away": "TBD", "venue": "Lumen Field, Seattle"},
    {"id": 95, "date": "2026-07-08", "time": "00:00", "stage": "r16", "home": "W85/W86",  "away": "TBD", "venue": "Mercedes-Benz Stadium, Atlanta"},
    {"id": 96, "date": "2026-07-08", "time": "04:00", "stage": "r16", "home": "W87/W88",  "away": "TBD", "venue": "Hard Rock Stadium, Miami Gardens"},
    # ── QUARTER-FINALS ───────────────────────────────────────────
    {"id": 97,  "date": "2026-07-10", "time": "01:00", "stage": "qf", "home": "QF1", "away": "QF2", "venue": "MetLife Stadium, East Rutherford"},
    {"id": 98,  "date": "2026-07-10", "time": "05:00", "stage": "qf", "home": "QF3", "away": "QF4", "venue": "AT&T Stadium, Arlington"},
    {"id": 99,  "date": "2026-07-11", "time": "01:00", "stage": "qf", "home": "QF5", "away": "QF6", "venue": "SoFi Stadium, Inglewood"},
    {"id": 100, "date": "2026-07-12", "time": "01:00", "stage": "qf", "home": "QF7", "away": "QF8", "venue": "NRG Stadium, Houston"},
    # ── SEMI-FINALS ──────────────────────────────────────────────
    {"id": 101, "date": "2026-07-15", "time": "04:00", "stage": "sf", "home": "SF1", "away": "SF2", "venue": "MetLife Stadium, East Rutherford"},
    {"id": 102, "date": "2026-07-16", "time": "04:00", "stage": "sf", "home": "SF3", "away": "SF4", "venue": "AT&T Stadium, Arlington"},
    # ── THIRD PLACE ──────────────────────────────────────────────
    {"id": 103, "date": "2026-07-18", "time": "23:00", "stage": "3p", "home": "3rd Place 1", "away": "3rd Place 2", "venue": "MetLife Stadium, East Rutherford"},
    # ── FINAL ────────────────────────────────────────────────────
    {"id": 104, "date": "2026-07-19", "time": "23:00", "stage": "f",  "home": "Finalist 1",  "away": "Finalist 2",  "venue": "MetLife Stadium, East Rutherford"},
]

STAGE_LABELS = {
    "gs":  "Group Stage",
    "r32": "Round of 32",
    "r16": "Round of 16",
    "qf":  "Quarter-final",
    "sf":  "Semi-final",
    "3p":  "Third Place",
    "f":   "Final",
}

# Points multiplier per stage
STAGE_MULTIPLIER = {
    "gs": 1, "r32": 1, "r16": 1,
    "qf": 2, "3p": 2,
    "sf": 3,
    "f":  4,
}

KNOCKOUT_STAGES = {"r32", "r16", "qf", "sf", "3p", "f"}


def calc_points(pred: dict, result: dict, stage: str) -> int:
    """Return points earned for a prediction given the actual result."""
    if not result or result.get("home_score") is None:
        return 0
    mult = STAGE_MULTIPLIER.get(stage, 1)
    hs, as_ = result["home_score"], result["away_score"]
    ph, pa = pred.get("home_score"), pred.get("away_score")
    if ph is None or pa is None:
        return 0

    if stage in KNOCKOUT_STAGES and hs == as_:
        # Draw after 90 → penalty decider
        pen = result.get("penalty_winner")
        if pen:
            exact = (ph == hs and pa == as_ and pred.get("penalty_winner") == pen)
            winner_ok = pred.get("penalty_winner") == pen
            if exact:
                return 3 * mult
            if winner_ok:
                return 1 * mult
        return 0
    else:
        if ph == hs and pa == as_:
            return 3 * mult
        actual_outcome = "H" if hs > as_ else ("A" if as_ > hs else "D")
        pred_outcome   = "H" if ph > pa  else ("A" if pa  > ph  else "D")
        if pred_outcome == actual_outcome:
            return 1 * mult
    return 0
