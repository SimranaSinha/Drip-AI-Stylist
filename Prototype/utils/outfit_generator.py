import json
import streamlit as st
import anthropic


def render():
    st.title("✨ Outfit Generator")
    st.markdown("Tell DRIP the occasion and let AI build the perfect looks from your wardrobe.")
    st.divider()

    if not st.session_state.api_key:
        st.warning("🔑 Add your Anthropic API key in the sidebar to use this feature.")
        return

    if len(st.session_state.wardrobe) < 3:
        st.info("👗 Add at least 3 items to your wardrobe before generating outfits.")
        return

    col1, col2 = st.columns(2)
    with col1:
        event = st.selectbox(
            "Occasion",
            ["Casual Day Out", "Work / Office", "Date Night", "Brunch",
             "Party / Night Out", "Gym / Active", "Formal Event", "Weekend Errands",
             "Custom..."],
        )
        if event == "Custom...":
            event = st.text_input("Describe the occasion", placeholder="e.g. Beach wedding")

        mood = st.selectbox(
            "Mood",
            ["Confident", "Relaxed", "Playful", "Sophisticated", "Edgy", "Romantic"]
        )

    with col2:
        weather = st.selectbox(
            "Weather",
            ["Warm & Sunny", "Hot", "Mild / Spring", "Cool / Autumn", "Cold", "Rainy"]
        )
        num_outfits = st.slider("Number of outfits", 1, 4, 3)

    generate = st.button("✨ Generate Outfits", type="primary", use_container_width=True)

    if generate and event:
        p = st.session_state.profile
        wardrobe_list = "\n".join(
            f"Item {i+1}: [{w['category']}] {w['name']}"
            + (f" — {w['colour']}" if w["colour"] else "")
            + (f" ({w['brand']})" if w["brand"] else "")
            for i, w in enumerate(st.session_state.wardrobe)
        )

        prompt = f"""You are an expert fashion stylist. Create {num_outfits} outfit combinations.

USER PROFILE:
- Name: {p['name'] or 'User'}
- Style: {p['style_persona']}
- Body type: {p['body_type']}
- Height: {p['height'] or 'not specified'}
- Gender expression: {p['gender']}

WARDROBE:
{wardrobe_list}

OCCASION: {event}
WEATHER: {weather}
MOOD: {mood}

Rules:
- Only use items from the wardrobe list above
- Reference items by their exact name
- Each outfit must use 2-5 items
- Make each outfit distinct

Respond ONLY with valid JSON (no markdown):
{{
  "outfits": [
    {{
      "name": "outfit name",
      "vibe": "3-5 word vibe",
      "items": ["exact item name", "exact item name"],
      "reasoning": "why this works for the occasion and person",
      "styling_tips": "specific tips to wear this well",
      "styling_on_person": "how it complements their body type and style"
    }}
  ]
}}"""

        with st.spinner("Your AI stylist is curating outfits..."):
            try:
                client = anthropic.Anthropic(api_key=st.session_state.api_key)
                resp = client.messages.create(
                    model="claude-opus-4-5",
                    max_tokens=1500,
                    messages=[{"role": "user", "content": prompt}]
                )
                raw = resp.content[0].text.strip().replace("```json", "").replace("```", "")
                data = json.loads(raw)
            except json.JSONDecodeError:
                st.error("AI returned unexpected format. Try again.")
                return
            except anthropic.AuthenticationError:
                st.error("Invalid API key. Check your key in the sidebar.")
                return
            except Exception as e:
                st.error(f"Something went wrong: {e}")
                return

        st.divider()
        st.markdown(f"### Your Outfits for *{event}*")

        for i, outfit in enumerate(data.get("outfits", [])):
            with st.container(border=True):
                col_title, col_vibe = st.columns([3, 1])
                with col_title:
                    st.markdown(f"#### Look {i+1} — {outfit['name']}")
                with col_vibe:
                    st.markdown(f"*{outfit.get('vibe', '')}*")

                c1, c2 = st.columns(2)
                with c1:
                    st.markdown("**The Pieces**")
                    for item in outfit.get("items", []):
                        st.markdown(f"- {item}")
                    st.markdown(f"\n**Why it works**  \n{outfit.get('reasoning', '')}")
                with c2:
                    st.info(f"💡 **Styling Tips**\n\n{outfit.get('styling_tips', '')}")
                    if outfit.get("styling_on_person"):
                        st.success(f"✨ {outfit['styling_on_person']}")