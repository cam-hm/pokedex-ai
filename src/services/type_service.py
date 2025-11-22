"""
Type Service
Handles type effectiveness calculations and type-related operations
"""
import streamlit as st
import requests
from src.config.constants import TYPE_ID_MAP


@st.cache_data
def get_type_effectiveness(types):
    """
    Calculate type effectiveness (weaknesses, resistances, immunities)
    
    Args:
        types (list): List of type names (e.g., ['fire', 'flying'])
        
    Returns:
        dict: Dictionary mapping type names to damage multipliers
    """
    damage_relations = {}
    
    for t in types:
        url = f"https://pokeapi.co/api/v2/type/{t}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()['damage_relations']
            
            # Double Damage From (Weakness)
            for type_node in data['double_damage_from']:
                name = type_node['name']
                damage_relations[name] = damage_relations.get(name, 1.0) * 2.0
                
            # Half Damage From (Resistance)
            for type_node in data['half_damage_from']:
                name = type_node['name']
                damage_relations[name] = damage_relations.get(name, 1.0) * 0.5
                
            # No Damage From (Immunity)
            for type_node in data['no_damage_from']:
                name = type_node['name']
                damage_relations[name] = damage_relations.get(name, 1.0) * 0.0
                
    return damage_relations


def get_type_icon_url(type_name):
    """
    Get icon URL for a given Pokemon type
    
    Args:
        type_name (str): Type name (e.g., 'fire')
        
    Returns:
        str: URL to type icon image
    """
    type_id = TYPE_ID_MAP.get(type_name, 1)
    return f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/types/generation-viii/sword-shield/{type_id}.png"
