# pages/leaderboard.py
import streamlit as st
import db
from matches import MATCHES, calc_points, STAGE_MULTIPLIER

MATCH_MAP = {m["id"]: m for m in MATCHES}
MEDALS = ["🥇", "🥈", "🥉"]

def show():
    st.title("🏆 Leaderboard")

    users   = db.get_all_users()
    all_pred = db.get_all_predictions()
    results  = db.get_all_results()

    if not users:
        st.info("No players registered yet.")
        return

    # Build per-user stats
    pred_by_user: dict[str, list] = {u["id"]: [] for u in users}
    for p in all_pred:
        if p["user_id"] in pred_by_user:
            pred_by_user[p["user_id"]].append(p)

    rows = []
    for u in users:
        pts = correct = exact = predicted = 0
        for p in pred_by_user[u["id"]]:
            m = MATCH_MAP.get(p["match_id"])
            r = results.get(p["match_id"])
            if not m or not r:
                predicted += 1
                continue
            score = calc_points(p, r, m["stage"])
            mult  = STAGE_MULTIPLIER.get(m["stage"], 1)
            pts      += score
            predicted += 1
            if score > 0:
                correct += 1
            if score >= 3 * mult:
                exact += 1
        rows.append({**u, "points": pts, "correct": correct, "exact": exact, "predicted": predicted})

    rows.sort(key=lambda r: (-r["points"], -r["correct"], -r["exact"]))

    # Summary stats
    total_players = len(users)
    results_in = len(results)

    c1, c2 = st.columns(2)
    c1.metric("Players", total_players)
    c2.metric("Matches with Results", f"{results_in} / 104")

    st.divider()

    # Leaderboard rows
    current_user_id = st.session_state.user["id"]
    for i, row in enumerate(rows):
        is_me = row["id"] == current_user_id
        medal = MEDALS[i] if i < 3 else f"#{i+1}"
        admin = " 👑" if row.get("is_admin") else ""
        me_tag = " **(you)**" if is_me else ""

        border = "border:1px solid rgba(245,200,66,.5);" if is_me else "border:1px solid #2a3550;"
        bg = "background:rgba(245,200,66,.06);" if is_me else "background:#1a2235;"

        pts_color = "#f5c842" if i == 0 else ("#c0c0c0" if i == 1 else ("#cd7f32" if i == 2 else "#f1f5f9"))

        st.markdown(f"""
        <div style="{bg}{border}border-radius:10px;padding:14px 20px;margin-bottom:8px;
                    display:flex;align-items:center;gap:20px;">
            <div style="font-size:26px;min-width:40px;text-align:center;">{medal}</div>
            <div style="flex:1;">
                <div style="font-weight:700;font-size:16px;">{row['username']}{admin}{me_tag}</div>
                <div style="font-size:12px;color:#94a3b8;margin-top:2px;">
                    {row['predicted']} predicted · {row['correct']} correct · {row['exact']} exact
                </div>
            </div>
            <div style="text-align:right;">
                <div style="font-size:36px;font-weight:900;color:{pts_color};line-height:1;">{row['points']}</div>
                <div style="font-size:11px;color:#94a3b8;">points</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # Scoring rules reference
    with st.expander("📋 Scoring Rules"):
        st.markdown("""
| Stage | Correct Winner | Exact Score |
|---|---|---|
| Group Stage, R32, R16 | 1 pt | 3 pts |
| Quarter-finals & 3rd Place | 2 pts | 6 pts |
| Semi-finals | 3 pts | 9 pts |
| Final | 4 pts | 12 pts |

**Knockout draws:** predict a draw score + the penalty shootout winner.  
Penalty winner correct = same as "correct winner" points for that stage.  
Exact score + penalty winner = full exact score points.
        """)
