# app.py — WC 2026 Prediction League
import streamlit as st
import db

st.set_page_config(
    page_title="WC2026 Predictor",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
[data-testid="stSidebar"] { background: #111827; }
.match-card {
    background: #1a2235;
    border: 1px solid #2a3550;
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 12px;
}
.stage-badge {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: .05em;
}
.leaderboard-row {
    background: #1a2235;
    border: 1px solid #2a3550;
    border-radius: 10px;
    padding: 14px 20px;
    margin-bottom: 8px;
}
.gold  { color: #f5c842; }
.green { color: #22c55e; }
.red   { color: #ef4444; }
.muted { color: #94a3b8; font-size: 13px; }
div[data-testid="stNumberInput"] input { text-align: center; font-size: 1.4rem; font-weight: 700; }
</style>
""", unsafe_allow_html=True)


# ── Session state defaults ────────────────────────────────────────────────────
if "user" not in st.session_state:
    st.session_state.user = None


# ── Auth gate ─────────────────────────────────────────────────────────────────
def show_auth():
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("## ⚽ WC2026 Predictor")
        st.caption("Prediction League · 5 AED / Match")
        st.divider()
        tab_login, tab_reg = st.tabs(["Sign In", "Register"])

        with tab_login:
            username = st.text_input("Username", key="li_user")
            password = st.text_input("Password", type="password", key="li_pass")
            if st.button("Sign In", use_container_width=True, type="primary"):
                user = db.login_user(username, password)
                if user:
                    st.session_state.user = user
                    st.rerun()
                else:
                    st.error("Invalid username or password.")

        with tab_reg:
            new_user = st.text_input("Choose a username", key="reg_user")
            new_pass = st.text_input("Choose a password", type="password", key="reg_pass")
            new_pass2 = st.text_input("Confirm password", type="password", key="reg_pass2")
            if st.button("Create Account", use_container_width=True, type="primary"):
                if not new_user or not new_pass:
                    st.error("Username and password are required.")
                elif new_pass != new_pass2:
                    st.error("Passwords don't match.")
                elif len(new_pass) < 6:
                    st.error("Password must be at least 6 characters.")
                else:
                    user = db.register_user(new_user, new_pass)
                    if user:
                        st.session_state.user = user
                        st.success("Account created! Welcome 🎉")
                        st.rerun()
                    else:
                        st.error("Username already taken.")
        st.caption("First person to register becomes admin.")


# ── Main app ──────────────────────────────────────────────────────────────────
def show_app():
    user = st.session_state.user

    with st.sidebar:
        st.markdown(f"### ⚽ WC2026")
        admin_badge = " 👑" if user.get("is_admin") else ""
        st.markdown(f"**{user['username']}**{admin_badge}")
        st.divider()
        page = st.radio(
            "Navigate",
            ["📅 Calendar", "🏆 Leaderboard"] + (["⚙️ Admin"] if user.get("is_admin") else []),
            label_visibility="collapsed",
        )
        st.divider()
        if st.button("Logout", use_container_width=True):
            st.session_state.user = None
            st.rerun()

    if page == "📅 Calendar":
        from pages import calendar as cal_page
        cal_page.show(user)
    elif page == "🏆 Leaderboard":
        from pages import leaderboard as lb_page
        lb_page.show()
    elif page == "⚙️ Admin":
        from pages import admin as admin_page
        admin_page.show()


# ── Entry point ───────────────────────────────────────────────────────────────
if st.session_state.user is None:
    show_auth()
else:
    show_app()
