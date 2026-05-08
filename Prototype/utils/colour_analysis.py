import streamlit as st
import anthropic


SEASON_INFO = {
    "Spring": {
        "emoji": "🌸",
        "description": "Warm, light, and clear tones. You glow in fresh, bright colours.",
        "best": ["Coral", "Peach", "Warm Yellow", "Ivory", "Camel", "Light Warm Brown"],
        "avoid": ["Black", "Cool Grey", "Icy Blue", "Stark White"],
        "neutrals": ["Ivory", "Camel", "Warm Beige", "Light Brown"],
    },
    "Summer": {
        "emoji": "☀️",
        "description": "Cool, muted, and soft tones. You shine in dusty, powdery shades.",
        "best": ["Dusty Rose", "Lavender", "Powder Blue", "Soft Teal", "Mauve", "Cool Grey"],
        "avoid": ["Orange", "Warm Yellow", "Camel", "Earthy Brown"],
        "neutrals": ["Soft White", "Cool Grey", "Rose Brown", "Blue Grey"],
    },
    "Autumn": {
        "emoji": "🍂",
        "description": "Warm, rich, and muted tones. You look stunning in earthy, golden shades.",
        "best": ["Burnt Orange", "Olive", "Rust", "Mustard", "Warm Brown", "Forest Green"],
        "avoid": ["Hot Pink", "Icy Blue", "Pure White", "Black"],
        "neutrals": ["Camel", "Warm Brown", "Olive", "Chocolate"],
    },
    "Winter": {
        "emoji": "❄️",
        "description": "Cool, deep, and clear tones. You are made for bold contrast and vivid colours.",
        "best": ["True Red", "Royal Blue", "Emerald", "Hot Pink", "Pure White", "Black"],
        "avoid": ["Orange", "Warm Beige", "Camel", "Muted Earth Tones"],
        "neutrals": ["Pure White", "Black", "Cool Grey", "Navy"],
    },
}


def render():
    st.title("🎨 Colour Analysis")
    st.markdown("Discover your colour season and the shades that make you shine.")
    st.divider()

    if not st.session_state.api_key:
        st.warning("🔑 Add your Anthropic API key in the sidebar to use this feature.")
        return

    tab1, tab2 = st.tabs(["🔍 Find My Season", "📚 Season Guide"])

    # ── Tab 1: AI Analysis ───────────────────────────────────────────────────
    with tab1:
        st.markdown("Answer a few quick questions and DRIP's AI will identify your colour season.")
        st.divider()

        col1, col2 = st.columns(2)

        with col1:
            skin_tone = st.selectbox(
                "Skin Tone",
                ["Fair / Porcelain", "Light", "Light Medium", "Medium", "Medium Deep",
                 "Deep / Dark"]
            )
            undertone = st.selectbox(
                "Skin Undertone",
                ["Warm (yellow / golden / peachy)",
                 "Cool (pink / red / bluish)",
                 "Neutral (mix of both)",
                 "Not sure"]
            )
            eye_colour = st.selectbox(
                "Eye Colour",
                ["Blue", "Green", "Hazel", "Light Brown", "Dark Brown",
                 "Grey", "Amber / Golden Brown", "Black"]
            )

        with col2:
            hair_colour = st.selectbox(
                "Natural Hair Colour",
                ["Platinum Blonde", "Golden Blonde", "Ash Blonde", "Light Brown",
                 "Medium Brown", "Dark Brown", "Auburn / Red", "Black",
                 "Salt & Pepper / Grey", "White"]
            )
            vein_colour = st.selectbox(
                "Wrist Vein Colour",
                ["Blue / Purple (cool)",
                 "Green (warm)",
                 "Blue-Green (neutral)",
                 "Hard to tell"]
            )
            metals = st.selectbox(
                "Which metal looks better on you?",
                ["Gold (warm)", "Silver (cool)", "Both look equally good"]
            )

        st.divider()
        analyse = st.button("🎨 Analyse My Colours", type="primary", use_container_width=True)

        if analyse:
            prompt = f"""You are an expert colour analyst specialising in seasonal colour theory.
Analyse this person's features and determine their colour season.

FEATURES:
- Skin tone: {skin_tone}
- Undertone: {undertone}
- Eye colour: {eye_colour}
- Natural hair colour: {hair_colour}
- Wrist vein colour: {vein_colour}
- Better metal: {metals}

The four seasons are: Spring (warm + light/clear), Summer (cool + soft/muted),
Autumn (warm + deep/muted), Winter (cool + deep/clear).

Respond ONLY with valid JSON (no markdown):
{{
  "season": "Spring|Summer|Autumn|Winter",
  "confidence": "High|Medium",
  "reasoning": "2-3 sentences explaining why based on their features",
  "signature_colours": ["colour1", "colour2", "colour3", "colour4", "colour5"],
  "colours_to_avoid": ["colour1", "colour2", "colour3"],
  "wardrobe_tip": "one specific tip for building their wardrobe around their season",
  "celebrity_examples": ["name1", "name2"]
}}"""

            with st.spinner("Analysing your colour profile..."):
                try:
                    client = anthropic.Anthropic(api_key=st.session_state.api_key)
                    resp = client.messages.create(
                        model="claude-opus-4-5",
                        max_tokens=800,
                        messages=[{"role": "user", "content": prompt}]
                    )
                    import json
                    raw = resp.content[0].text.strip().replace("```json", "").replace("```", "")
                    data = json.loads(raw)
                except Exception as e:
                    st.error(f"Something went wrong: {e}")
                    return

            season = data.get("season", "")
            info = SEASON_INFO.get(season, {})

            st.divider()

            # Season result header
            st.markdown(f"## {info.get('emoji', '')} You are a **{season}**!")
            st.markdown(f"*{info.get('description', '')}*")
            st.markdown(f"**Confidence:** {data.get('confidence', '')}")
            st.divider()

            # Reasoning
            with st.container(border=True):
                st.markdown("### 🔍 Why You're a " + season)
                st.markdown(data.get("reasoning", ""))

            st.divider()

            col_a, col_b = st.columns(2)

            with col_a:
                with st.container(border=True):
                    st.markdown("### ✅ Your Best Colours")
                    for colour in data.get("signature_colours", []):
                        st.markdown(f"- {colour}")
                    st.markdown(f"\n**💡 Wardrobe Tip**  \n{data.get('wardrobe_tip', '')}")

            with col_b:
                with st.container(border=True):
                    st.markdown("### ❌ Colours to Avoid")
                    for colour in data.get("colours_to_avoid", []):
                        st.markdown(f"- {colour}")

                    celebrities = data.get("celebrity_examples", [])
                    if celebrities:
                        st.divider()
                        st.markdown("### 🌟 Celebrity Examples")
                        for celeb in celebrities:
                            st.markdown(f"- {celeb}")

            # Save to session state
            st.session_state.colour_season = season
            st.success(f"✨ Saved! Your season ({season}) will now be used in outfit generation.")

    # ── Tab 2: Season Guide ──────────────────────────────────────────────────
    with tab2:
        st.markdown("### The Four Colour Seasons")
        st.markdown("Find out what each season means and what works best.")
        st.divider()

        for season_name, info in SEASON_INFO.items():
            with st.expander(f"{info['emoji']} {season_name} — {info['description']}"):
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.markdown("**✅ Best Colours**")
                    for c in info["best"]:
                        st.markdown(f"- {c}")
                with c2:
                    st.markdown("**🎨 Neutrals**")
                    for c in info["neutrals"]:
                        st.markdown(f"- {c}")
                with c3:
                    st.markdown("**❌ Avoid**")
                    for c in info["avoid"]:
                        st.markdown(f"- {c}")