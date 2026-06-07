# pages/calendar.py
import streamlit as st
from datetime import datetime, timezone, timedelta
import db
from matches import MATCHES, STAGE_LABELS, STAGE_MULTIPLIER, KNOCKOUT_STAGES

DUBAI = timezone(timedelta(hours=4))

STAGE_COLORS = {
    "gs":  "#1e3a5f",
    "r32": "#1a2e1a",
    "r16": "#2a1f0e",
    "qf":  "#2d1515",
    "sf":  "#2a1040",
    "3p":  "#1c2020",
    "f":   "#1a1200",
}
STAGE_TEXT = {
    "gs":  "#60a5fa",
    "r32": "#4ade80",
    "r16": "#fbbf24",
    "qf":  "#f87171",
    "sf":  "#c084fc",
    "3p":  "#5eead4",
    "f":   "#f5c842",
}


def is_locked(match: dict) -> bool:
    """True if kickoff is within 30 min or already past."""
    dt_str = f"{match['date']}T{match['time']}:00+04:00"
    kickoff = datetime.fromisoformat(dt_str)
    now = datetime.now(tz=DUBAI)
    return now >= kickoff - timedelta(minutes=30)


def stage_badge(stage: str) -> str:
    bg = STAGE_COLORS.get(stage, "#222")
    fg = STAGE_TEXT.get(stage, "#fff")
    label = STAGE_LABELS.get(stage, stage)
    return (
        f'<span style="background:{bg};color:{fg};padding:2px 8px;'
        f'border-radius:4px;font-size:11px;font-weight:700;'
        f'text-transform:uppercase;letter-spacing:.05em;">{label}</span>'
    )


def mult_badge(stage: str) -> str:
    m = STAGE_MULTIPLIER.get(stage, 1)
    if m <= 1:
        return ""
    return (
        f'<span style="background:#2a1a00;color:#f5c842;padding:2px 8px;'
        f'border-radius:4px;font-size:11px;font-weight:700;">{m}× POINTS</span>'
    )


def show(user: dict):
    st.title("📅 Match Calendar")

    # Load user predictions + results
    preds = db.get_predictions_for_user(user["id"])
    results = db.get_all_results()

    # Group matches by date
    from collections import defaultdict
    by_date: dict[str, list] = defaultdict(list)
    for m in MATCHES:
        by_date[m["date"]].append(m)

    # Month tabs
    months = sorted({d[:7] for d in by_date})
    month_labels = [datetime.strptime(m, "%Y-%m").strftime("%b %Y") for m in months]
    tab_objs = st.tabs(month_labels)

    for tab, month in zip(tab_objs, months):
        with tab:
            dates = sorted(d for d in by_date if d.startswith(month))
            for date in dates:
                matches_on_day = sorted(by_date[date], key=lambda m: m["time"])
                predicted_count = sum(1 for m in matches_on_day if m["id"] in preds)
                total = len(matches_on_day)
                has_result = any(m["id"] in results for m in matches_on_day)

                label = datetime.strptime(date, "%Y-%m-%d").strftime("%A, %d %b")
                status_icon = "✅" if predicted_count == total else ("🟡" if predicted_count else "⬜")
                result_note = " · 📊 Results in" if has_result else ""

                with st.expander(
                    f"{status_icon} **{label}** — {total} match{'es' if total > 1 else ''} · "
                    f"{predicted_count}/{total} predicted{result_note}",
                    expanded=(date == datetime.now(tz=DUBAI).strftime("%Y-%m-%d")),
                ):
                    for match in matches_on_day:
                        render_match(match, preds.get(match["id"]), results.get(match["id"]), user)


def render_match(match: dict, pred: dict | None, result: dict | None, user: dict):
    locked = is_locked(match)
    stage = match["stage"]
    mult = STAGE_MULTIPLIER.get(stage, 1)
    is_ko = stage in KNOCKOUT_STAGES

    badges = stage_badge(stage)
    if mult > 1:
        badges += f" &nbsp; {mult_badge(stage)}"
    if locked and not result:
        badges += ' &nbsp; <span style="background:#2a1515;color:#ef4444;padding:2px 8px;border-radius:4px;font-size:11px;font-weight:700;">LOCKED</span>'

    st.markdown(f"""
    <div style="background:#1a2235;border:1px solid #2a3550;border-radius:12px;padding:16px 20px;margin-bottom:8px;">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">
            <div>{badges}</div>
            <div style="font-size:12px;color:#94a3b8;">{match['time']} Dubai · {match['venue'].split(',')[0]}</div>
        </div>
        <div style="font-size:16px;font-weight:700;text-align:center;margin-bottom:4px;">
            {match['home']} <span style="color:#475569;font-size:14px;">vs</span> {match['away']}
        </div>
        {f'<div style="text-align:center;font-size:13px;color:#94a3b8;">{match.get("group","") and "Group " + match["group"]}</div>' if match.get("group") else ""}
    </div>
    """, unsafe_allow_html=True)

    # Show result if available
    if result:
        hs, as_ = result["home_score"], result["away_score"]
        pen = result.get("penalty_winner")
        pen_note = ""
        if pen:
            winner_name = match["home"] if pen == "home" else match["away"]
            pen_note = f" · 🟡 Pens: **{winner_name}** wins"

        col_r1, col_r2, col_r3 = st.columns([2, 1, 2])
        with col_r1:
            st.markdown(f"<div style='text-align:right;font-size:13px;color:#94a3b8;'>Result</div>", unsafe_allow_html=True)
        with col_r2:
            st.markdown(f"<div style='text-align:center;font-size:26px;font-weight:900;'>{hs} – {as_}</div>", unsafe_allow_html=True)
        with col_r3:
            if pen_note:
                st.markdown(pen_note)

        # Show user's prediction and points
        if pred:
            from matches import calc_points
            pts = calc_points(pred, result, stage)
            pts_color = "#22c55e" if pts >= 3 * mult else ("#f5c842" if pts > 0 else "#475569")
            pts_label = f"+{pts} pts" if pts > 0 else "0 pts"
            pred_pen = pred.get("penalty_winner")
            pred_pen_note = f" (pens: {match['home'] if pred_pen == 'home' else match['away']})" if pred_pen else ""
            st.markdown(
                f"Your pick: **{pred['home_score']} – {pred['away_score']}**{pred_pen_note} "
                f"&nbsp;→&nbsp; <span style='color:{pts_color};font-weight:700;font-size:18px;'>{pts_label}</span>",
                unsafe_allow_html=True,
            )
        st.divider()
        return

    # No result — show prediction form
    if locked:
        if pred:
            pred_pen = pred.get("penalty_winner")
            pen_str = f" · Pens: {match['home'] if pred_pen == 'home' else match['away']}" if pred_pen else ""
            st.markdown(
                f"🔒 Locked · Your pick: **{pred['home_score']} – {pred['away_score']}**{pen_str}",
                unsafe_allow_html=True,
            )
        else:
            st.markdown("🔒 Locked · No prediction submitted")
        st.divider()
        return

    # Editable form
    col_home, col_score, col_away = st.columns([3, 2, 3])
    with col_home:
        st.markdown(f"<div style='text-align:right;padding-top:8px;font-weight:600;'>{match['home']}</div>", unsafe_allow_html=True)
    with col_score:
        sc1, sc2 = st.columns(2)
        with sc1:
            h_val = st.number_input(
                "H", min_value=0, max_value=20,
                value=int(pred["home_score"]) if pred else 0,
                key=f"h_{match['id']}", label_visibility="collapsed",
            )
        with sc2:
            a_val = st.number_input(
                "A", min_value=0, max_value=20,
                value=int(pred["away_score"]) if pred else 0,
                key=f"a_{match['id']}", label_visibility="collapsed",
            )
    with col_away:
        st.markdown(f"<div style='padding-top:8px;font-weight:600;'>{match['away']}</div>", unsafe_allow_html=True)

    # Penalty picker for knockout draws
    pen_winner = None
    if is_ko and h_val == a_val:
        st.markdown("<div style='font-size:12px;color:#94a3b8;margin-top:6px;'>Draw after 90 min → pick penalty winner</div>", unsafe_allow_html=True)
        pen_col1, pen_col2 = st.columns(2)
        current_pen = pred.get("penalty_winner") if pred else None
        with pen_col1:
            if st.button(f"🏆 {match['home']} wins pens", key=f"pen_h_{match['id']}",
                         type="primary" if current_pen == "home" else "secondary",
                         use_container_width=True):
                pen_winner = "home"
        with pen_col2:
            if st.button(f"🏆 {match['away']} wins pens", key=f"pen_a_{match['id']}",
                         type="primary" if current_pen == "away" else "secondary",
                         use_container_width=True):
                pen_winner = "away"
        if pen_winner is None and current_pen:
            pen_winner = current_pen

    save_col, _ = st.columns([1, 3])
    with save_col:
        btn_label = "Update ✓" if pred else "Save prediction"
        if st.button(btn_label, key=f"save_{match['id']}", type="primary", use_container_width=True):
            db.save_prediction(user["id"], match["id"], h_val, a_val, pen_winner)
            st.success("Saved!", icon="✅")
            st.rerun()

    if pred:
        pred_pen = pred.get("penalty_winner")
        pen_str = f" · pens: {match['home'] if pred_pen == 'home' else match['away']}" if pred_pen else ""
        st.markdown(
            f"<div style='font-size:12px;color:#22c55e;'>✓ Current: {pred['home_score']} – {pred['away_score']}{pen_str}</div>",
            unsafe_allow_html=True,
        )
    st.divider()
