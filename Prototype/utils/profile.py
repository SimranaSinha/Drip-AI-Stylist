import streamlit as st
from utils.storage import save_profile


def render():
    st.title("👤 Your Style Profile")
    st.markdown("Help DRIP understand you so it can style you perfectly.")
    st.divider()

    p = st.session_state.profile

    col1, col2 = st.columns(2)

    with col1:
        p["name"] = st.text_input("Your Name", value=p["name"], placeholder="e.g. Alex")

        p["style_persona"] = st.selectbox(
            "Style Persona",
            ["Classic", "Streetwear", "Minimalist", "Maximalist", "Bohemian",
             "Preppy", "Athleisure", "Romantic", "Edgy / Alternative", "Business Casual"],
            index=["Classic", "Streetwear", "Minimalist", "Maximalist", "Bohemian",
                   "Preppy", "Athleisure", "Romantic", "Edgy / Alternative",
                   "Business Casual"].index(p.get("style_persona", "Classic"))
            if p.get("style_persona") in ["Classic", "Streetwear", "Minimalist", "Maximalist",
                                           "Bohemian", "Preppy", "Athleisure", "Romantic",
                                           "Edgy / Alternative", "Business Casual"] else 0,
        )

        p["gender"] = st.selectbox(
            "Gender Expression",
            ["Not specified", "Feminine", "Masculine", "Androgynous / Non-binary", "Fluid / Mix"],
            index=["Not specified", "Feminine", "Masculine",
                   "Androgynous / Non-binary", "Fluid / Mix"].index(p.get("gender", "Not specified"))
            if p.get("gender") in ["Not specified", "Feminine", "Masculine",
                                    "Androgynous / Non-binary", "Fluid / Mix"] else 0,
        )

    with col2:
        p["body_type"] = st.selectbox(
            "Body Type",
            ["Not specified", "Petite", "Tall", "Athletic", "Curvy",
             "Plus size", "Straight / Rectangle", "Pear", "Apple", "Hourglass"],
            index=["Not specified", "Petite", "Tall", "Athletic", "Curvy",
                   "Plus size", "Straight / Rectangle", "Pear", "Apple",
                   "Hourglass"].index(p.get("body_type", "Not specified"))
            if p.get("body_type") in ["Not specified", "Petite", "Tall", "Athletic", "Curvy",
                                       "Plus size", "Straight / Rectangle", "Pear", "Apple",
                                       "Hourglass"] else 0,
        )

        p["height"] = st.text_input(
            "Height (optional)", value=p.get("height", ""), placeholder="e.g. 5'6\" or 168cm"
        )

        uploaded_photo = st.file_uploader(
            "Profile Photo (optional)", type=["jpg", "jpeg", "png"],
            help="Used to show outfits styled on your photo"
        )
        if uploaded_photo:
            p["photo"] = uploaded_photo.read()

    if st.button("💾 Save Profile", type="primary"):
        st.session_state.profile = p
        save_profile(p)
        st.success(f"Profile saved! Welcome, {p['name'] or 'Stylee'} 👋")

    if any([p.get("name"), p.get("style_persona", "Classic") != "Classic"]):
        st.divider()
        st.markdown("### Your Style Card")
        c1, c2, c3 = st.columns(3)
        c1.metric("Style", p.get("style_persona", "—"))
        c2.metric("Body Type", p.get("body_type", "—"))
        c3.metric("Expression", p.get("gender", "—"))