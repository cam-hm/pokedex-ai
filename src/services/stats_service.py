"""
Stats Service
Calculates actual Pokemon stats based on Base Stats, IVs, EVs, Level, and Nature.
"""
import math

def calculate_stat(stat_name, base, iv, ev, level, nature_modifier):
    """
    Calculate the actual value of a stat.
    
    Formula (HP):
    ((2 * Base + IV + (EV/4)) * Level / 100) + Level + 10
    
    Formula (Others):
    (((2 * Base + IV + (EV/4)) * Level / 100) + 5) * Nature
    """
    if stat_name == "hp":
        return math.floor(((2 * base + iv + (ev / 4)) * level / 100) + level + 10)
    else:
        val = math.floor(((2 * base + iv + (ev / 4)) * level / 100) + 5)
        
        # Apply Nature
        if nature_modifier == 1.1:
            val = math.floor(val * 1.1)
        elif nature_modifier == 0.9:
            val = math.floor(val * 0.9)
            
        return val

def get_nature_modifier(nature_data, stat_name):
    """
    Get the multiplier (1.1, 0.9, or 1.0) for a stat based on nature.
    """
    if nature_data["plus"] == stat_name:
        return 1.1
    elif nature_data["minus"] == stat_name:
        return 0.9
    return 1.0

def calculate_all_stats(base_stats, evs, nature_data, level=50, ivs=31):
    """
    Calculate all 6 stats.
    
    Args:
        base_stats (dict): {'hp': 100, 'attack': 100, ...}
        evs (dict): {'hp': 0, 'attack': 252, ...}
        nature_data (dict): {'plus': 'attack', 'minus': 'speed'}
        level (int): Default 50
        ivs (int): Default 31 (Max)
        
    Returns:
        dict: {'hp': 175, 'attack': 150, ...}
    """
    final_stats = {}
    
    for stat_name, base_val in base_stats.items():
        # Handle different naming conventions if necessary (e.g. special-attack vs sp_atk)
        # PokeAPI uses 'special-attack', 'special-defense'
        
        ev = evs.get(stat_name, 0)
        modifier = get_nature_modifier(nature_data, stat_name)
        
        final_stats[stat_name] = calculate_stat(stat_name, base_val, ivs, ev, level, modifier)
        
    return final_stats
