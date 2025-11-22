"""
Pokemon Service
Business logic for Pokemon operations
"""
from src.api.pokeapi_client import get_species_data, get_evolution_chain_data


def get_pokemon_description(species_data):
    """
    Extract English description from species data
    
    Args:
        species_data (dict): Pokemon species data
        
    Returns:
        str: Description text
    """
    if not species_data:
        return "No description available."
    
    flavor_texts = species_data.get('flavor_text_entries', [])
    description = next(
        (entry['flavor_text'] for entry in flavor_texts if entry['language']['name'] == 'en'),
        "No description available."
    )
    return description.replace('\n', ' ').replace('\f', ' ')


def get_pokemon_varieties(species_data, current_name):
    """
    Get alternate forms/varieties of a Pokemon
    
    Args:
        species_data (dict): Pokemon species data
        current_name (str): Current Pokemon name to exclude
        
    Returns:
        list: List of variety dictionaries
    """
    if not species_data:
        return []
    
    varieties = species_data.get('varieties', [])
    return [v for v in varieties if v['pokemon']['name'] != current_name]


def get_evolution_chain(species_url):
    """
    Fetch and parse evolution chain
    
    Args:
        species_url (str): URL to species endpoint
        
    Returns:
        list: List of evolution stages with name and id
    """
    species_data = get_species_data(species_url)
    if not species_data:
        return []
    
    evo_chain_url = species_data.get('evolution_chain', {}).get('url')
    if not evo_chain_url:
        return []
    
    evo_data = get_evolution_chain_data(evo_chain_url)
    if not evo_data:
        return []
    
    chain = evo_data.get('chain', {})
    evo_list = []
    
    def parse_evolution(chain_node):
        species_name = chain_node['species']['name']
        species_id = chain_node['species']['url'].split('/')[-2]
        evo_list.append({'name': species_name, 'id': species_id})
        for next_node in chain_node.get('evolves_to', []):
            parse_evolution(next_node)
    
    parse_evolution(chain)
    return evo_list
