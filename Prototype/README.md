# 💧 Drip — Your AI Fashion Stylist (Prototype)

A personal AI stylist built with Streamlit that helps you discover your style, manage your wardrobe, and dress with confidence.

## Features

### 🎨 Colour Analysis
Discover your colour season and the shades that make you shine.

- **Find My Season** — Answer a few quick questions (skin tone, undertone, eye colour, hair colour, wrist vein colour, and metal preference) and DRIP's AI will identify your colour season
- **Season Results** — Get your season (Spring, Summer, Autumn, or Winter) with a confidence score, a detailed explanation of why you belong to that season, your best colours to wear, colours to avoid, wardrobe tips, and celebrity style examples
- **Season Guide** — Explore all four colour seasons with curated best colours, neutrals, and colours to avoid for each

### ✨ Other Features
- 🏠 **Home** — Dashboard overview
- 👤 **Profile** — Personal style profile
- 👗 **Wardrobe** — Manage and track your wardrobe items
- ✨ **Outfit Generator** — AI-generated outfit suggestions
- 💬 **AI Chat** — Chat with your personal AI stylist

## 📁 Structure of Repo
```
💧 Drip-AI-Stylist/
└── 📁 Prototype/
    ├── 🚀 app.py                  # Main Streamlit app entry point
    ├── 🗃️ drip_data.json          # Local data storage
    ├── 📦 requirements.txt        # Python dependencies
    ├── 📝 README.md
    └── 📁 utils/
        ├── 🔧 __init__.py
        ├── 💬 chat.py             # AI Chat feature
        ├── 🎨 colour_analysis.py  # Colour season analysis
        ├── 🏠 home.py             # Home dashboard
        ├── ✨ outfit_generator.py # AI outfit suggestions
        ├── 👤 profile.py          # User profile
        ├── 💾 storage.py          # Data persistence
        └── 👗 wardrobe.py         # Wardrobe management
```

## Getting Started
### Prerequisites

- Python 3.8+
- pip
- Anthropic API Key

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/SimranaSinha/Drip-.git
   cd Drip-
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:
   ```bash
   streamlit run app.py
   ```

4. Open your browser and go to `http://localhost:8501`

5. Enter your Anthropic API key in the sidebar to unlock AI features

## Built With

- [Streamlit](https://streamlit.io/) — Web framework
- [Anthropic Claude](https://www.anthropic.com/) — AI engine powering style recommendations and colour analysis

