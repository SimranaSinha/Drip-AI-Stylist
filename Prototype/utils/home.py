import streamlit as st


def render():
    st.title("💧 Welcome to DRIP")
    st.subheader("Your Personal AI Fashion Stylist")
    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 👤 Set Your Profile")
        st.markdown(
            "Tell DRIP your style persona, body type, and preferences. "
            "The more it knows, the better it styles."
        )
        profile_done = bool(st.session_state.profile.get("name"))
        st.success("Profile set ✓") if profile_done else st.info("Not set yet")

    with col2:
        st.markdown("### 👗 Build Your Wardrobe")
        st.markdown(
            "Add your clothing items by category. "
            "DRIP uses your actual wardrobe to build real outfits."
        )
        count = len(st.session_state.wardrobe)
        st.success(f"{count} items added ✓") if count > 0 else st.info("Wardrobe is empty")

    with col3:
        st.markdown("### ✨ Generate Outfits")
        st.markdown(
            "Pick an event, mood, and weather. "
            "DRIP's AI will curate 3 outfit combinations just for you."
        )
        api_ready = bool(st.session_state.api_key)
        st.success("API key ready ✓") if api_ready else st.warning("Add API key in sidebar")

    st.divider()

    st.markdown("### 🚀 How to get started")
    st.markdown(
        "1. **Add your Anthropic API key** in the sidebar  \n"
        "2. **Fill in your Profile** — style, body type, height  \n"
        "3. **Add items** to your Wardrobe  \n"
        "4. Go to **Outfit Generator** and let DRIP style you  \n"
        "5. Chat with your **AI Stylist** anytime for advice"
    )