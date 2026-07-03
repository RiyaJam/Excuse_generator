# excuse_engine.py — Core excuse generation logic and excuse bank

import random


# ─────────────────────────────────────────────
# Excuse Bank
# ─────────────────────────────────────────────

EXCUSES = {
    "Work": [
        # Internet/Tech issues
        "My internet connection has been unstable all morning.",
        "My computer crashed and I lost all my work.",
        "I'm having issues with my VPN and can't access the company systems.",
        "My work laptop won't turn on and I'm troubleshooting it.",
        # Health issues
        "I have an urgent doctor's appointment I couldn't reschedule.",
        "I've developed a severe migraine that makes it impossible to work.",
        "I'm having an allergic reaction and need to see a doctor.",
        "I suddenly feel very dizzy and can't safely commute.",
        # Transportation
        "My car won't start and I'm waiting for roadside assistance.",
        "There's been a major accident on the highway causing severe delays.",
        "The public transport in my area is on strike today.",
        "I got a flat tire on the way to work.",
        # Home emergencies
        "There's been a water leak in my apartment that needs immediate attention.",
        "My building's power went out and I'm unable to work from home.",
        "There's a gas leak in my building and we've been evacuated.",
        "A contractor is here for an emergency repair I couldn't reschedule.",
        # Personal
        "I have a family emergency that requires my immediate attention.",
        "I've been called for an unexpected jury duty today.",
        "I need to deal with an urgent legal matter.",
        "I have to attend an emergency meeting with my child's school."
    ],
    "School": [
        # Health
        "I have a severe headache and can't concentrate.",
        "I'm feeling nauseous and don't want to spread illness to classmates.",
        "I have a doctor's appointment that couldn't be rescheduled.",
        "I had an allergic reaction and need to take medication that makes me drowsy.",
        # Transportation
        "My bus didn't show up this morning.",
        "There's construction blocking the road to school.",
        "My parents' car broke down and they can't drive me.",
        "I missed the school bus due to an alarm malfunction.",
        # Academic
        "I need more time to complete my research for the assignment.",
        "The library resources I needed were unavailable.",
        "My computer crashed while I was finishing my assignment.",
        "I've been struggling with the material and need extra time.",
        # Family
        "I had to help care for a sick family member.",
        "There was a family emergency I had to attend to.",
        "We had unexpected visitors that I couldn't avoid.",
        "I had to accompany a family member to an important appointment."
    ],
    "Social": [
        # Transportation
        "My car is making a strange noise and I don't want to risk driving it.",
        "The trains are running on a holiday schedule and I can't get there.",
        # Health issues
        "I developed a sudden rash and need to figure out what's causing it.",
        "I threw out my back while getting ready.",
        "I have a terrible toothache and need to see a dentist.",
        "I'm experiencing vertigo and shouldn't be out in public.",
        # Household emergencies
        "My kitchen sink started leaking and I need to fix it.",
        "My smoke detector won't stop beeping and I need to replace the battery.",
        "I accidentally locked myself out of my apartment.",
        "My refrigerator stopped working and I need to save my food.",
        # Unusual circumstances
        "A stray cat had kittens in my garage and I need to help them.",
        "My neighbor locked their keys in their car with the engine running.",
        "There's a suspicious package in my building and we're evacuated.",
        "I just found out I'm allergic to the venue (pet dander/peanuts/etc)."
    ],
    "Family": [
        # Childcare
        "The daycare called - my child has a fever and needs to be picked up.",
        "Our regular babysitter is sick and we can't find coverage.",
        "My child has a school project due tomorrow we forgot about.",
        "There's an unexpected early dismissal at school today.",
        # Elder care
        "My mother's home health aide didn't show up today.",
        "My father's medication needs to be refilled urgently.",
        "We need to take my grandmother to an unexpected doctor's appointment.",
        "The assisted living facility is on lockdown due to a health inspection.",
        # Emergencies
        "Our basement flooded after last night's heavy rain.",
        "Our carbon monoxide detector went off and we're waiting for the fire department.",
        "A family member was in a minor car accident and needs support.",
        "We're dealing with a sudden pest infestation in our home.",
        # Logistics
        "Our flight home got canceled and we're stuck at the airport.",
        "The hotel lost our reservation and we need to find new accommodations.",
        "Our luggage got lost and we're waiting for it to be delivered.",
        "Our rental car broke down in an unfamiliar area.",
        # Special
        "Today is the anniversary of a family member's passing and we're not up for socializing.",
        "We're fostering a rescue dog who's having separation anxiety.",
        "We're hosting unexpected out-of-town relatives.",
        "Our home security system triggered a false alarm and police are investigating."
    ],
    "Personal": [
        # Mental health
        "I'm experiencing severe anxiety today and need to take care of myself.",
        "My therapist recommended I take a mental health day.",
        "I'm feeling completely overwhelmed and need to reset.",
        "I haven't been sleeping well and can't function properly today.",
        # Physical health
        "I twisted my ankle while exercising and need to rest it.",
        "I have a migraine coming on and need to lie down.",
        "I got a bad sunburn and can't wear proper clothes.",
        "I'm recovering from a minor medical procedure.",
        # Home issues
        "My water heater broke and I need to get it fixed.",
        "There's a gas leak in my building and we had to evacuate.",
        "My apartment is being treated for bed bugs today.",
        "My air conditioning stopped working in this heat wave.",
        # Technology problems
        "My phone fell in water and I'm waiting for it to dry out.",
        "I got locked out of all my accounts due to a security breach.",
        "My smart home devices all malfunctioned at once.",
        "My internet provider is having an outage in my area.",
        # Unusual
        "I'm waiting for an important delivery that requires my signature.",
        "I'm being audited and need to gather tax documents.",
        "My wallet was stolen and I'm dealing with canceling cards.",
        "I'm being called for jury duty today."
    ]
}


# ─────────────────────────────────────────────
# Core Generation Functions
# ─────────────────────────────────────────────

def generate_excuse(scenario: str, urgency: int = 5, believability: int = 5) -> str:
    """
    Generate an excuse based on scenario, urgency, and believability.

    Args:
        scenario (str): One of Work, School, Social, Family, Personal.
        urgency (int): 1–10 urgency level (affects prefix).
        believability (int): 1–10 score (affects which excuse is selected).

    Returns:
        str: The generated excuse string.
    """
    excuses_list = EXCUSES.get(scenario, EXCUSES["Personal"])

    # Select excuse based on believability index
    index = (believability * len(excuses_list) // 10) - 1
    index = max(0, min(index, len(excuses_list) - 1))
    excuse = excuses_list[index]

    # Add urgency prefix
    if urgency >= 8:
        excuse = f"[URGENT] {excuse}"
    elif urgency >= 5:
        excuse = f"[Important] {excuse}"

    return excuse


def get_random_excuse(scenario: str) -> str:
    """
    Return a completely random excuse for the given scenario.

    Args:
        scenario (str): Scenario key.

    Returns:
        str: A random excuse.
    """
    excuses_list = EXCUSES.get(scenario, EXCUSES["Personal"])
    return random.choice(excuses_list)


def get_all_scenarios() -> list:
    """Return all available scenario categories."""
    return list(EXCUSES.keys())


def rank_excuses(effectiveness_data: dict, scenario: str) -> list:
    """
    Rank excuses for a given scenario by their stored effectiveness scores.

    Args:
        effectiveness_data (dict): Dict mapping excuse text → score.
        scenario (str): The scenario to filter by.

    Returns:
        list: Sorted list of (excuse, score) tuples.
    """
    scenario_excuses = set(EXCUSES.get(scenario, []))
    ranked = [
        (excuse, score)
        for excuse, score in effectiveness_data.items()
        if excuse in scenario_excuses
    ]
    return sorted(ranked, key=lambda x: x[1], reverse=True)
