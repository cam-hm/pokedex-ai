"""
Application Constants and Configuration
"""

# Pokemon Generation Data
GENERATIONS = {
    "Generation 1 (Kanto)": {"limit": 151, "offset": 0},
    "Generation 2 (Johto)": {"limit": 100, "offset": 151},
    "Generation 3 (Hoenn)": {"limit": 135, "offset": 251},
    "Generation 4 (Sinnoh)": {"limit": 107, "offset": 386},
    "Generation 5 (Unova)": {"limit": 156, "offset": 493},
    "Generation 6 (Kalos)": {"limit": 72, "offset": 649},
    "Generation 7 (Alola)": {"limit": 88, "offset": 721},
    "Generation 8 (Galar)": {"limit": 96, "offset": 809},
    "Generation 9 (Paldea)": {"limit": 120, "offset": 905}
}

# Stat Configuration for colored bars
STAT_CONFIG = {
    "hp": {"color": "#4CAF50", "name": "HP"},
    "attack": {"color": "#FDD835", "name": "Attack"},
    "defense": {"color": "#FF9800", "name": "Defense"},
    "special-attack": {"color": "#2196F3", "name": "Sp. Atk"},
    "special-defense": {"color": "#9C27B0", "name": "Sp. Def"},
    "speed": {"color": "#E91E63", "name": "Speed"}
}

# Type ID Mapping for icon URLs
TYPE_ID_MAP = {
    "normal": 1, "fighting": 2, "flying": 3, "poison": 4, "ground": 5, "rock": 6, "bug": 7,
    "ghost": 8, "steel": 9, "fire": 10, "water": 11, "grass": 12, "electric": 13, "psychic": 14,
    "ice": 15, "dragon": 16, "dark": 17, "fairy": 18
}
