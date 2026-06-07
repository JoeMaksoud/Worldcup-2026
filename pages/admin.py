# pages/admin.py
import streamlit as st
import db
from matches import MATCHES, STAGE_LABELS, KNOCKOUT_STAGES
from collections import defaultdict
from datetime import datetime

STAGE_ORDER = ["gs", "r32", "r16", "qf", "sf", "3p", "f"]


def show():
    st.title("⚙️ Admin Panel")
    st.caption("Enter match results · Scores auto-calculate for all players")

    results = db.get_all_results()
    users   = db.get_all_users()

    st.info(f"**{len(users)}** registered players · **{len(results)}** results entered so far")

    # Stage filter
    selected_stage = st.selectbox(
        "Filter by stage",
        ["All"] + STAGE_ORDER,
        format_func=lambda s: "All Stages" if s == "All" else STAGE_LABELS.get(s, s),
    )

    filtered = MATCHES if selected_stage == "All" else [m for m in MATCHES if m["stage"] == selected_stage]

    # Group by date
    by_date: dict[str, list] = defaultdict(list)
    for m in filtered:
        by_date[m["date"]].append(m)

    for date in sorted(by_date):
        label = datetime.strptime(date, "%Y-%m-%d").strftime("%A, %d %b %Y")
        day_matches = sorted(by_date[date], key=lambda m: m["time"])
        done = sum(1 for m in day_matches if m["id"] in results)

        with st.expander(f"📅 **{label}** — {done}/{len(day_matches)} results entered"):
            for match in day_matches:
                render_result_form(match, results.get(match["id"]))


def render_result_form(match: dict, result: dict | None):
    stage  = match["stage"]
    is_ko  = stage in KNOCKOUT_STAGES

    has_result = result is not None
    status_icon = "✅" if has_result else "⬜"
    header = (
        f"{status_icon} **{match['home']} vs {match['away']}** "
        f"— {STAGE_LABELS.get(stage, stage)} · {match['time']} Dubai"
    )
    if has_result:
        header += f"  →  **{result['home_score']} – {result['away_score']}**"
        if result.get("penalty_winner"):
            pen_team = match["home"] if result["penalty_winner"] == "home" else match["away"]
            header += f" (pens: {pen_team})"

    with st.container():
        st.markdown(header)
        col1, col2, col3, col4 = st.columns([2, 1, 1, 2])
        with col1:
            st.markdown(f"<div style='text-align:right;padding-top:6px;font-weight:600;'>{match['home']}</div>", unsafe_allow_html=True)
        with col2:
            h_val = st.number_input(
                "Home", min_value=0, max_value=20,
                value=int(result["home_score"]) if result else 0,
                key=f"rh_{match['id']}", label_visibility="collapsed",
            )
        with col3:
            a_val = st.number_input(
                "Away", min_value=0, max_value=20,
                value=int(result["away_score"]) if result else 0,
                key=f"ra_{match['id']}", label_visibility="collapsed",
            )
        with col4:
            st.markdown(f"<div style='padding-top:6px;font-weight:600;'>{match['away']}</div>", unsafe_allow_html=True)

        pen_winner = result.get("penalty_winner") if result else None
        if is_ko and h_val == a_val:
            st.markdown("<div style='font-size:12px;color:#94a3b8;'>Draw → select penalty winner</div>", unsafe_allow_html=True)
            p1, p2, p3 = st.columns([1, 1, 2])
            with p1:
                if st.button(f"{match['home']}", key=f"rph_{match['id']}",
                             type="primary" if pen_winner == "home" else "secondary",
                             use_container_width=True):
                    pen_winner = "home"
            with p2:
                if st.button(f"{match['away']}", key=f"rpa_{match['id']}",
                             type="primary" if pen_winner == "away" else "secondary",
                             use_container_width=True):
                    pen_winner = "away"
            if pen_winner is None and result and result.get("penalty_winner"):
                pen_winner = result["penalty_winner"]

        save_col, _ = st.columns([1, 4])
        with save_col:
            if st.button("💾 Save Result", key=f"rsave_{match['id']}", type="primary", use_container_width=True):
                db.save_result(match["id"], h_val, a_val, pen_winner if (is_ko and h_val == a_val) else None)
                db.get_all_results.clear()  # bust cache
                st.success("Result saved!")
                st.rerun()
        st.divider()
