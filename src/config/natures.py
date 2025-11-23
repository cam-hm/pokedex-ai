"""
Pokemon Natures and their stat modifiers.
Key: Nature Name
Value: {"plus": stat_to_increase, "minus": stat_to_decrease}
"""

NATURES = {
    "Hardy": {"plus": None, "minus": None},
    "Lonely": {"plus": "attack", "minus": "defense"},
    "Brave": {"plus": "attack", "minus": "speed"},
    "Adamant": {"plus": "attack", "minus": "special-attack"},
    "Naughty": {"plus": "attack", "minus": "special-defense"},
    "Bold": {"plus": "defense", "minus": "attack"},
    "Docile": {"plus": None, "minus": None},
    "Relaxed": {"plus": "defense", "minus": "speed"},
    "Impish": {"plus": "defense", "minus": "special-attack"},
    "Lax": {"plus": "defense", "minus": "special-defense"},
    "Timid": {"plus": "speed", "minus": "attack"},
    "Hasty": {"plus": "speed", "minus": "defense"},
    "Serious": {"plus": None, "minus": None},
    "Jolly": {"plus": "speed", "minus": "special-attack"},
    "Naive": {"plus": "speed", "minus": "special-defense"},
    "Modest": {"plus": "special-attack", "minus": "attack"},
    "Mild": {"plus": "special-attack", "minus": "defense"},
    "Quiet": {"plus": "special-attack", "minus": "speed"},
    "Bashful": {"plus": None, "minus": None},
    "Rash": {"plus": "special-attack", "minus": "special-defense"},
    "Calm": {"plus": "special-defense", "minus": "attack"},
    "Gentle": {"plus": "special-defense", "minus": "defense"},
    "Sassy": {"plus": "special-defense", "minus": "speed"},
    "Careful": {"plus": "special-defense", "minus": "special-attack"},
    "Quirky": {"plus": None, "minus": None},
}
