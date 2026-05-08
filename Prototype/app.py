import streamlit as st
from utils.storage import load_wardrobe, load_profile, load_colour_season

st.set_page_config(
    page_title="DRIP — AI Stylist",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Session state defaults ──────────────────────────────────────────────────
if "wardrobe" not in st.session_state:
    st.session_state.wardrobe = load_wardrobe()
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "profile" not in st.session_state:
    st.session_state.profile = load_profile()
if "api_key" not in st.session_state:
    st.session_state.api_key = ""
if "colour_season" not in st.session_state:
    st.session_state.colour_season = load_colour_season()

# ── Sidebar nav ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("# 💧 DRIP")
    st.markdown("*Your AI Fashion Stylist*")
    st.divider()

    api_key = st.text_input(
        "🔑 Anthropic API Key",
        value=st.session_state.api_key,
        type="password",
        placeholder="sk-ant-...",
        help="Get your key at console.anthropic.com"
    )
    if api_key:
        st.session_state.api_key = api_key

    st.divider()
    st.markdown("### Navigate")
    page = st.radio(
        "Go to",
        ["🏠 Home", "👤 Profile", "👗 Wardrobe", "✨ Outfit Generator",
         "💬 AI Chat", "🎨 Colour Analysis"],
        label_visibility="collapsed"
    )
    st.divider()
    wardrobe_count = len(st.session_state.wardrobe)
    st.metric("Wardrobe Items", wardrobe_count)
    if st.session_state.colour_season:
        st.success(f"🎨 {st.session_state.colour_season}")
    if not st.session_state.api_key:
        st.warning("Add your API key to unlock AI features.")

# ── Page routing ────────────────────────────────────────────────────────────
if page == "🏠 Home":
    from utils import home
    home.render()
elif page == "👤 Profile":
    from utils import profile
    profile.render()
elif page == "👗 Wardrobe":
    from utils import wardrobe
    wardrobe.render()
elif page == "✨ Outfit Generator":
    from utils import outfit_generator
    outfit_generator.render()
elif page == "💬 AI Chat":
    from utils import chat
    chat.render()
elif page == "🎨 Colour Analysis":
    from utils import colour_analysis
    colour_analysis.render()