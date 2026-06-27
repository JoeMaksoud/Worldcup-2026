# pages/_admin.py
import streamlit as st
import db
import api_football as api
from matches import MATCHES, STAGE_LABELS, KNOCKOUT_STAGES
from collections import defaultdict
from datetime import datetime

STAGE_ORDER = ["gs", "r32", "r16", "qf", "sf", "3p", "f"]


def show():
    st.title("⚙️ Admin Panel")

    results  = db.get_all_results()
    users    = db.get_all_users()
    overrides = db.get_match_overrides()

    st.info(f"**{len(users)}** registered players · **{len(results)}** results entered")

    # ── Password Reset ─────────────────────────────────────────────────────────
    show_password_reset(users)

    st.divider()

    # ── Live Sync Section ──────────────────────────────────────────────────────
    st.subheader("🌐 Live Data Sync")

    if not api.is_api_configured():
        st.warning("⚠️ No RapidAPI key found. Add `RAPIDAPI_KEY` to your Streamlit secrets to enable live sync.")
    else:
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Sync Results**")
            st.caption("Pulls finished match scores from API-Football and updates the leaderboard automatically.")
            if st.button("🔄 Sync Results Now", type="primary", use_container_width=True, key="sync_results"):
                with st.spinner("Fetching from API-Football..."):
                    api_results = api.get_finished_results()
                if not api_results:
                    st.warning("No finished matches found in API yet.")
                else:
                    synced, skipped = db.sync_results_from_api(api_results, MATCHES)
                    st.success(f"✅ Synced **{synced}** results. Skipped **{skipped}** (manual override active).")

        with col2:
            st.markdown("**Sync Knockout Teams**")
            st.caption("Updates bracket team names as teams qualify through each round.")
            if st.button("🔄 Sync Bracket Now", use_container_width=True, key="sync_teams"):
                with st.spinner("Fetching upcoming fixtures..."):
                    api_upcoming = api.get_upcoming_with_teams()
                updated = db.sync_teams_from_api(api_upcoming, MATCHES)
                if updated:
                    st.success(f"✅ Updated **{updated}** knockout match team names.")
                else:
                    st.info("No new team names to update yet.")

        # Auto-sync status
        if api.any_live_now():
            st.success("🔴 **Live matches happening now!** Sync results to get latest scores.")

    st.divider()

    # ── Manual Results Entry ───────────────────────────────────────────────────
    st.subheader("✏️ Manual Results Entry")
    st.caption("Use this to correct any API errors. Manual entries won't be overwritten by auto-sync.")

    selected_stage = st.selectbox(
        "Filter by stage",
        ["All"] + STAGE_ORDER,
        format_func=lambda s: "All Stages" if s == "All" else STAGE_LABELS.get(s, s),
        key="stage_filter",
    )

    filtered = MATCHES if selected_stage == "All" else [m for m in MATCHES if m["stage"] == selected_stage]

    by_date: dict[str, list] = defaultdict(list)
    for m in filtered:
        by_date[m["date"]].append(m)

    for date in sorted(by_date):
        label = datetime.strptime(date, "%Y-%m-%d").strftime("%A, %d %b %Y")
        day_matches = sorted(by_date[date], key=lambda m: m["time"])
        done = sum(1 for m in day_matches if m["id"] in results)

        with st.expander(f"📅 **{label}** — {done}/{len(day_matches)} results entered"):
            for match in day_matches:
                # Apply bracket overrides for knockout team names
                display = dict(match)
                if match["id"] in overrides:
                    display["home"] = overrides[match["id"]]["home"]
                    display["away"] = overrides[match["id"]]["away"]
                render_result_form(display, results.get(match["id"]))


def render_result_form(match: dict, result: dict | None):
    stage  = match["stage"]
    is_ko  = stage in KNOCKOUT_STAGES

    has_result   = result is not None
    is_manual    = result.get("manual_override", False) if result else False
    status_icon  = "✅" if has_result else "⬜"
    manual_badge = " 🔒 Manual" if is_manual else (" 🤖 Auto" if has_result else "")

    header = (f"{status_icon} **{match['home']} vs {match['away']}** "
              f"— {STAGE_LABELS.get(stage, stage)} · {match['time']} Dubai{manual_badge}")
    if has_result:
        header += f"  →  **{result['home_score']} – {result['away_score']}**"
        if result.get("penalty_winner"):
            pen_team = match["home"] if result["penalty_winner"] == "home" else match["away"]
            header += f" (pens: {pen_team})"

    with st.container():
        st.markdown(header)

        col1, col2, col3, col4 = st.columns([2, 1, 1, 2])
        with col1:
            st.markdown(f"<div style='text-align:right;padding-top:6px;font-weight:600;'>{match['home']}</div>",
                        unsafe_allow_html=True)
        with col2:
            h_val = st.number_input("Home", min_value=0, max_value=20,
                                    value=int(result["home_score"]) if result else 0,
                                    key=f"rh_{match['id']}", label_visibility="collapsed")
        with col3:
            a_val = st.number_input("Away", min_value=0, max_value=20,
                                    value=int(result["away_score"]) if result else 0,
                                    key=f"ra_{match['id']}", label_visibility="collapsed")
        with col4:
            st.markdown(f"<div style='padding-top:6px;font-weight:600;'>{match['away']}</div>",
                        unsafe_allow_html=True)

        pen_winner = result.get("penalty_winner") if result else None
        if is_ko and h_val == a_val:
            st.markdown("<div style='font-size:12px;color:#94a3b8;'>Draw → select penalty winner</div>",
                        unsafe_allow_html=True)
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

        btn_col1, btn_col2, _ = st.columns([1, 1, 3])
        with btn_col1:
            if st.button("💾 Save (Manual)", key=f"rsave_{match['id']}", type="primary", use_container_width=True):
                db.save_result_manual(match["id"], h_val, a_val,
                                      pen_winner if (is_ko and h_val == a_val) else None)
                st.success("Saved as manual override — API won't overwrite this.")
                st.rerun()

        with btn_col2:
            if is_manual:
                if st.button("🤖 Release to API", key=f"release_{match['id']}", use_container_width=True):
                    db.clear_manual_override(match["id"])
                    st.success("Manual override removed — API can now update this result.")
                    st.rerun()

        st.divider()


def show_password_reset(users: list[dict]):
    st.subheader("🔑 Reset Player Password")
    current_user_id = st.session_state.user["id"]
    other_users = [u for u in users if u["id"] != current_user_id]

    if not other_users:
        st.info("No other players registered yet.")
        return

    usernames = [u["username"] for u in other_users]
    selected_username = st.selectbox("Select player", usernames, key="reset_user_select")
    new_password      = st.text_input("New password", type="password", key="reset_new_pass")
    confirm_password  = st.text_input("Confirm new password", type="password", key="reset_confirm_pass")

    if st.button("Reset Password", type="primary", key="reset_btn"):
        if not new_password:
            st.error("Please enter a new password.")
        elif len(new_password) < 6:
            st.error("Password must be at least 6 characters.")
        elif new_password != confirm_password:
            st.error("Passwords don't match.")
        else:
            import bcrypt
            selected_user = next(u for u in other_users if u["username"] == selected_username)
            new_hash = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
            db.get_client().table("users").update(
                {"password_hash": new_hash}
            ).eq("id", selected_user["id"]).execute()
            st.success(f"✅ Password for **{selected_username}** has been reset.")
