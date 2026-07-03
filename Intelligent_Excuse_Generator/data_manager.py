# data_manager.py — Handles loading and saving excuse history, favorites, and usage patterns

import os
import json


EXCUSE_DATA_FILE = "excuse_data.json"


def load_excuse_data():
    """
    Load excuse data from JSON file.
    Returns a dict with history, favorites, effectiveness, and usage_patterns.
    """
    if os.path.exists(EXCUSE_DATA_FILE):
        with open(EXCUSE_DATA_FILE, 'r') as f:
            return json.load(f)
    else:
        return {
            "history": [],
            "favorites": [],
            "effectiveness": {},
            "usage_patterns": []
        }


def save_excuse_data(excuse_data: dict):
    """
    Save excuse data to JSON file.

    Args:
        excuse_data (dict): The data to persist.
    """
    with open(EXCUSE_DATA_FILE, 'w') as f:
        json.dump(excuse_data, f, indent=4)


def add_to_history(excuse_data: dict, excuse: str, scenario: str, save: bool = True):
    """
    Add an excuse to the history log.

    Args:
        excuse_data (dict): The loaded data dict.
        excuse (str): The excuse text.
        scenario (str): The scenario category.
        save (bool): Whether to persist immediately.
    """
    from datetime import datetime
    entry = {
        "excuse": excuse,
        "scenario": scenario,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    excuse_data["history"].append(entry)
    if save:
        save_excuse_data(excuse_data)


def add_to_favorites(excuse_data: dict, excuse: str, save: bool = True):
    """
    Add an excuse to favorites if not already present.

    Args:
        excuse_data (dict): The loaded data dict.
        excuse (str): The excuse text.
        save (bool): Whether to persist immediately.
    """
    if excuse not in excuse_data["favorites"]:
        excuse_data["favorites"].append(excuse)
        if save:
            save_excuse_data(excuse_data)


def update_effectiveness(excuse_data: dict, excuse: str, score: int, save: bool = True):
    """
    Update the effectiveness score for a given excuse.

    Args:
        excuse_data (dict): The loaded data dict.
        excuse (str): The excuse text (used as key).
        score (int): Effectiveness score (e.g. 1-10).
        save (bool): Whether to persist immediately.
    """
    excuse_data["effectiveness"][excuse] = score
    if save:
        save_excuse_data(excuse_data)


def get_ranked_excuses(excuse_data: dict):
    """
    Return excuses sorted by effectiveness score (descending).

    Returns:
        list: List of (excuse, score) tuples.
    """
    ranked = sorted(
        excuse_data["effectiveness"].items(),
        key=lambda x: x[1],
        reverse=True
    )
    return ranked
