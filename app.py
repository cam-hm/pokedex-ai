import streamlit as st
import requests

# Set page config
st.set_page_config(page_title="Minimal Pokedex", page_icon="🔴")

# Title and Description
st.title("🔴 Minimal Pokedex")
st.markdown("Search for a Pokemon by name or ID to see its details!")

# Input for Pokemon Name
pokemon_name = st.text_input("Enter Pokemon Name or ID:", "pikachu").lower()

# Function to fetch data
def get_pokemon_data(name):
    url = f"https://pokeapi.co/api/v2/pokemon/{name}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Fetch and Display Data
if pokemon_name:
    data = get_pokemon_data(pokemon_name)
    
    if data:
        # Layout: 2 Columns
        col1, col2 = st.columns(2)
        
        with col1:
            # Display Image
            # Try to get the official artwork, fallback to default sprite
            sprite_url = data['sprites']['other']['official-artwork']['front_default']
            if not sprite_url:
                sprite_url = data['sprites']['front_default']
            
            st.image(sprite_url, caption=f"#{data['id']} {data['name'].title()}", use_column_width=True)
            
        with col2:
            # Display Basic Info
            st.subheader("General Info")
            st.write(f"**Name:** {data['name'].title()}")
            st.write(f"**ID:** {data['id']}")
            
            # Types
            types = [t['type']['name'].title() for t in data['types']]
            st.write(f"**Type:** {', '.join(types)}")
            
            # Height & Weight
            st.write(f"**Height:** {data['height']/10} m")
            st.write(f"**Weight:** {data['weight']/10} kg")
            
    else:
        st.error("Pokemon not found! Please check the spelling.")
