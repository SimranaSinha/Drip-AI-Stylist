import streamlit as st
from utils.storage import save_wardrobe

CATEGORIES = [
    "Tops", "Bottoms", "Dresses & Jumpsuits", "Outerwear",
    "Shoes", "Bags & Accessories", "Activewear", "Formal / Occasionwear"
]


def render():
    st.title("👗 My Wardrobe")
    st.markdown("Add your clothing items. DRIP builds real outfits from what you actually own.")
    st.divider()

    with st.expander("➕ Add New Item", expanded=len(st.session_state.wardrobe) == 0):
        col1, col2, col3 = st.columns(3)
        with col1:
            category = st.selectbox("Category", CATEGORIES)
        with col2:
            name = st.text_input("Item Name", placeholder="e.g. White linen shirt")
        with col3:
            colour = st.text_input("Colour(s)", placeholder="e.g. White")

        col4, col5 = st.columns(2)
        with col4:
            brand = st.text_input("Brand (optional)", placeholder="e.g. Zara")
        with col5:
            notes = st.text_input("Notes (optional)", placeholder="e.g. slightly cropped")

        if st.button("Add to Wardrobe", type="primary"):
            if name.strip():
                st.session_state.wardrobe.append({
                    "id": len(st.session_state.wardrobe) + 1,
                    "category": category,
                    "name": name.strip(),
                    "colour": colour.strip(),
                    "brand": brand.strip(),
                    "notes": notes.strip(),
                })
                save_wardrobe(st.session_state.wardrobe)
                st.success(f"Added: {name} ✓")
                st.rerun()
            else:
                st.error("Item name is required.")

    st.divider()

    wardrobe = st.session_state.wardrobe
    if not wardrobe:
        st.info("Your wardrobe is empty. Add some items above to get started!")
        return

    st.markdown(f"### {len(wardrobe)} Items in Your Wardrobe")

    for cat in CATEGORIES:
        items = [w for w in wardrobe if w["category"] == cat]
        if not items:
            continue
        st.markdown(f"**{cat}** ({len(items)})")
        cols = st.columns(4)
        for i, item in enumerate(items):
            with cols[i % 4]:
                with st.container(border=True):
                    st.markdown(f"**{item['name']}**")
                    if item["colour"]:
                        st.caption(f"🎨 {item['colour']}")
                    if item["brand"]:
                        st.caption(f"🏷 {item['brand']}")
                    if item["notes"]:
                        st.caption(f"📝 {item['notes']}")
                    if st.button("🗑 Remove", key=f"del_{item['id']}"):
                        st.session_state.wardrobe = [
                            w for w in wardrobe if w["id"] != item["id"]
                        ]
                        save_wardrobe(st.session_state.wardrobe)
                        st.rerun()

    st.divider()
    if st.button("🗑 Clear Entire Wardrobe", type="secondary"):
        st.session_state.wardrobe = []
        save_wardrobe([])
        st.rerun()