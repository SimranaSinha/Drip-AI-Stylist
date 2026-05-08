import streamlit as st
import anthropic


def build_system_prompt():
    p = st.session_state.profile
    wardrobe = st.session_state.wardrobe

    wardrobe_list = (
        "\n".join(
            f"{i+1}. [{w['category']}] {w['name']}"
            + (f" — {w['colour']}" if w["colour"] else "")
            for i, w in enumerate(wardrobe)
        )
        if wardrobe
        else "No items added yet."
    )

    return f"""You are DRIP's personal AI stylist — warm, knowledgeable, and fashion-forward.
You speak like a brilliant stylist friend: confident, encouraging, specific, never preachy.

USER PROFILE:
- Name: {p['name'] or 'the user'}
- Style persona: {p['style_persona']}
- Body type: {p['body_type']}
- Height: {p['height'] or 'not specified'}
- Gender expression: {p['gender']}

THEIR WARDROBE ({len(wardrobe)} items):
{wardrobe_list}

GUIDELINES:
- Reference actual wardrobe items when giving outfit advice
- Be specific and concise — 2-4 short paragraphs max
- Be conversational and warm, not formal
- You can answer general fashion questions (colour theory, trends, styling tips, garment care)
- Stay in character as the DRIP stylist at all times"""


def render():
    st.title("💬 AI Stylist Chat")
    st.markdown("Ask your personal DRIP stylist anything about fashion, outfits, or style.")
    st.divider()

    if not st.session_state.api_key:
        st.warning("🔑 Add your Anthropic API key in the sidebar to chat.")
        return

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for msg in st.session_state.chat_history:
        with st.chat_message("assistant" if msg["role"] == "assistant" else "user"):
            st.markdown(msg["content"])

    if not st.session_state.chat_history:
        name = st.session_state.profile.get("name") or ""
        greeting = (
            f"Hi{' ' + name if name else ''}! ✨ I'm your DRIP stylist. "
            f"I can see your wardrobe has {len(st.session_state.wardrobe)} item(s). "
            "Ask me anything — outfit ideas, what to wear for an event, colour tips, "
            "or what pieces are missing from your closet!"
        )
        with st.chat_message("assistant"):
            st.markdown(greeting)

        suggestions = [
            "What should I wear to a casual brunch?",
            "Can you suggest a date night outfit?",
            "What colours work best for me?",
            "What's missing from my wardrobe?",
        ]
        st.markdown("**Try asking:**")
        cols = st.columns(len(suggestions))
        for col, suggestion in zip(cols, suggestions):
            if col.button(suggestion, use_container_width=True):
                st.session_state._quick_prompt = suggestion
                st.rerun()

    quick = st.session_state.pop("_quick_prompt", None)
    user_input = st.chat_input("Ask your stylist...") or quick

    if user_input:
        with st.chat_message("user"):
            st.markdown(user_input)
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        with st.chat_message("assistant"):
            with st.spinner("Styling..."):
                try:
                    client = anthropic.Anthropic(api_key=st.session_state.api_key)
                    resp = client.messages.create(
                        model="claude-haiku-4-5-20251001",
                        max_tokens=700,
                        system=build_system_prompt(),
                        messages=st.session_state.chat_history[-14:],
                    )
                    reply = resp.content[0].text.strip()
                except anthropic.AuthenticationError:
                    reply = "⚠️ Invalid API key. Please check your key in the sidebar."
                except Exception as e:
                    reply = f"⚠️ Something went wrong: {e}"
            st.markdown(reply)

        st.session_state.chat_history.append({"role": "assistant", "content": reply})

    if st.session_state.chat_history:
        st.divider()
        if st.button("🗑 Clear Chat"):
            st.session_state.chat_history = []
            st.rerun()