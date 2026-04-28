import json
import os

SETTINGS_FILE = "settings.json"
LEADERBOARD_FILE = "leaderboard.json"


def load_settings():
    # default settings
    default_settings = {
        "sound": True,
        "car_color": "pink",
        "difficulty": "normal"
    }

    if not os.path.exists(SETTINGS_FILE):
        save_settings(default_settings)
        return default_settings

    with open(SETTINGS_FILE, "r") as file:
        return json.load(file)


def save_settings(settings):
    # save settings to json
    with open(SETTINGS_FILE, "w") as file:
        json.dump(settings, file, indent=4)


def load_leaderboard():
    # load saved scores
    if not os.path.exists(LEADERBOARD_FILE):
        return []

    with open(LEADERBOARD_FILE, "r") as file:
        return json.load(file)


def save_score(name, score, distance):
    # add new score
    leaderboard = load_leaderboard()

    leaderboard.append({
        "name": name,
        "score": score,
        "distance": distance
    })

    # sort from best to worst
    leaderboard.sort(key=lambda x: x["score"], reverse=True)

    # keep only top 10
    leaderboard = leaderboard[:10]

    with open(LEADERBOARD_FILE, "w") as file:
        json.dump(leaderboard, file, indent=4)