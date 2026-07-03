# proof_generator.py — Generates simulated proof documents and apology messages

import random
from datetime import datetime


# ─────────────────────────────────────────────
# Proof Generation
# ─────────────────────────────────────────────

PROOF_TYPES = ["document", "chat_screenshot", "location_log"]

APOLOGIES = [
    "I sincerely apologize for the inconvenience.",
    "Please accept my deepest apologies for my absence.",
    "I regret that I was unable to fulfill my obligation.",
    "I am truly sorry for the trouble caused.",
    "I take full responsibility and apologize for the issue.",
    "I understand my actions have caused problems, and I apologize.",
    "I want to express my sincere remorse for what happened.",
    "I am deeply sorry for the disruption.",
    "I offer my sincerest apologies for the misunderstanding.",
    "I am extremely sorry for the error."
]


def generate_proof(proof_type: str = None) -> str:
    """
    Generate a simulated proof document string.

    Args:
        proof_type (str): One of 'document', 'chat_screenshot', 'location_log'.
                          If None, a random type is selected.

    Returns:
        str: The generated proof text.
    """
    if proof_type is None:
        proof_type = random.choice(PROOF_TYPES)

    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

    if proof_type == "document":
        return (
            f"📄 Document Proof ({timestamp}):\n"
            "This document certifies that the individual was unable to attend\n"
            "due to unforeseen and unavoidable circumstances.\n"
            "Verified by: [Authority Name] | Ref No: #EXC-" + str(random.randint(10000, 99999))
        )

    elif proof_type == "chat_screenshot":
        return (
            f"💬 Chat Screenshot ({timestamp}):\n"
            "[Contact]: Hey, are you coming?\n"
            "[User]: I'm so sorry, I can't make it — something urgent came up.\n"
            "[Contact]: Oh no, I hope everything is okay!\n"
            "[User]: Yeah, dealing with it now. Will explain later."
        )

    else:  # location_log
        lat = round(random.uniform(12.0, 28.0), 6)
        lon = round(random.uniform(72.0, 88.0), 6)
        return (
            f"📍 Location Log ({timestamp}):\n"
            f"Coordinates: {lat}° N, {lon}° E\n"
            f"Location: [Relevant Location — Hospital/Home/Office]\n"
            f"Duration: {random.randint(30, 180)} minutes\n"
            "Status: Verified via GPS tracking"
        )


def generate_apology(style: str = "professional") -> str:
    """
    Generate an apology message.

    Args:
        style (str): 'professional' or 'emotional'.

    Returns:
        str: Apology message string.
    """
    base = random.choice(APOLOGIES)

    if style == "emotional":
        emotional_additions = [
            " This situation has been incredibly difficult for me.",
            " I truly value our relationship and hope you can forgive me.",
            " I promise this won't happen again — you mean a lot to me.",
            " I feel terrible about this and wanted you to know immediately."
        ]
        return base + random.choice(emotional_additions)

    elif style == "professional":
        professional_additions = [
            " Please let me know how I can make this right.",
            " I will ensure measures are in place to prevent a recurrence.",
            " I am available to discuss this at your earliest convenience.",
            " I take full accountability and will address this promptly."
        ]
        return base + random.choice(professional_additions)

    return base


def get_proof_types() -> list:
    """Return all available proof types."""
    return PROOF_TYPES
