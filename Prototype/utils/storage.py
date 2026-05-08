import json
import os

STORAGE_FILE = "drip_data.json"


def load_data():
    """Load saved data from JSON file."""
    if os.path.exists(STORAGE_FILE):
        try:
            with open(STORAGE_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def save_data(data: dict):
    """Save data to JSON file."""
    try:
        with open(STORAGE_FILE, "w") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Error saving data: {e}")


def load_wardrobe():
    data = load_data()
    return data.get("wardrobe", [])


def save_wardrobe(wardrobe: list):
    data = load_data()
    data["wardrobe"] = wardrobe
    save_data(data)


def load_profile():
    data = load_data()
    return data.get("profile", {
        "name": "",
        "style_persona": "Classic",
        "body_type": "Not specified",
        "height": "",
        "gender": "Not specified",
        "photo": None,
    })


def save_profile(profile: dict):
    data = load_data()
    # Don't save binary photo data to JSON
    profile_to_save = {k: v for k, v in profile.items() if k != "photo"}
    data["profile"] = profile_to_save
    save_data(data)


def load_colour_season():
    data = load_data()
    return data.get("colour_season", "")


def save_colour_season(season: str):
    data = load_data()
    data["colour_season"] = season
    save_data(data)