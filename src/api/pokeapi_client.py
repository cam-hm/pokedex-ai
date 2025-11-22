"""
PokeAPI Client
Handles all HTTP requests to PokeAPI with caching
"""
import streamlit as st
import requests


@st.cache_data
def get_pokemon_list(limit=50, offset=0):
    """
    Fetch a list of Pokemon from PokeAPI
    
    Args:
        limit (int): Number of Pokemon to fetch
        offset (int): Starting index
        
    Returns:
        list: List of Pokemon with name and URL
    """
    url = f"https://pokeapi.co/api/v2/pokemon?limit={limit}&offset={offset}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['results']
    return []


def get_pokemon_data(name):
    """
    Fetch detailed data for a specific Pokemon
    
    Args:
        name (str): Pokemon name or ID
        
    Returns:
        dict: Pokemon data or None if not found
    """
    url = f"https://pokeapi.co/api/v2/pokemon/{name}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None


@st.cache_data
def get_all_pokemon_names():
    """
    Fetch all Pokemon names for autocomplete
    
    Returns:
        list: List of all Pokemon names
    """
    url = "https://pokeapi.co/api/v2/pokemon?limit=10000"
    response = requests.get(url)
    if response.status_code == 200:
        results = response.json()['results']
        return [p['name'] for p in results]
    return []


def get_species_data(species_url):
    """
    Fetch Pokemon species data
    
    Args:
        species_url (str): URL to species endpoint
        
    Returns:
        dict: Species data or None if failed
    """
    response = requests.get(species_url)
    if response.status_code == 200:
        return response.json()
    return None


def get_evolution_chain_data(evolution_chain_url):
    """
    Fetch evolution chain data
    
    Args:
        evolution_chain_url (str): URL to evolution chain endpoint
        
    Returns:
        dict: Evolution chain data or None if failed
    """
    response = requests.get(evolution_chain_url)
    if response.status_code == 200:
        return response.json()
    return None
