"""
Home View
Pokemon grid and generation filter
"""
import streamlit as st
from src.config.constants import GENERATIONS
from src.api.pokeapi_client import get_pokemon_list, get_all_pokemon_names


def navigate_to_detail(pokemon_name):
    """Navigate to detail view"""
    st.session_state.view = 'detail'
    st.session_state.selected_pokemon = pokemon_name


def show_home_view():
    """Render the home page with Pokemon grid"""
    st.title("🔴 Minimal Pokedex")
    st.markdown("Select a Pokemon to view details!")
    
    # Search Bar (Autocomplete)
    all_names = get_all_pokemon_names()
    search_query = st.selectbox("Search Pokemon:", [""] + all_names, index=0, placeholder="Type to search...")
    
    if search_query:
        navigate_to_detail(search_query)
        st.rerun()

    # Generation Selector
    selected_gen = st.selectbox("Select Generation:", list(GENERATIONS.keys()))
    gen_params = GENERATIONS[selected_gen]
    # Pokemon Grid
    with st.spinner(f"Loading {selected_gen}..."):
        pokemon_list = get_pokemon_list(limit=gen_params['limit'], offset=gen_params['offset'])
        
        cols = st.columns(5)  # 5 columns grid
        for i, pokemon in enumerate(pokemon_list):
            # Extract ID from URL for image
            p_id = pokemon['url'].split('/')[-2]
            p_name = pokemon['name'].title()
            
            # URLs
            gif_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/showdown/{p_id}.gif"
            png_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{p_id}.png"
            
            with cols[i % 5]:
                # Use HTML object tag for fallback (avoids React onerror issues)
                # Fixed height container for grid consistency
                st.markdown(f"""
                    <div style="display: flex; justify-content: center; align-items: center; height: 120px; margin-bottom: 10px;">
                        <object data="{gif_url}" type="image/gif" style="max-width: 100px; max-height: 100px;">
                            <img src="{png_url}" style="max-width: 100px; max-height: 100px;" />
                        </object>
                    </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"#{p_id} {p_name}", key=f"btn_{p_id}"):
                    navigate_to_detail(pokemon['name'])
                    st.rerun()
