"""
Detail View
Pokemon detail page with stats, description, varieties, and evolution chain
"""
import streamlit as st
from src.config.constants import STAT_CONFIG
from src.api.pokeapi_client import get_pokemon_data, get_species_data
from src.services.pokemon_service import (
    get_pokemon_description, 
    get_pokemon_varieties, 
    get_evolution_chain,
    get_abilities_info,
    get_gender_ratio,
    get_capture_rate,
    get_base_happiness
)
from src.services.type_service import get_type_icon_url
from src.ui.components.modals import show_effectiveness_modal


def navigate_to_home():
    """Navigate back to home view"""
    st.session_state.view = 'home'
    st.session_state.selected_pokemon = None


def navigate_to_detail(pokemon_name):
    """Navigate to detail view"""
    st.session_state.view = 'detail'
    st.session_state.selected_pokemon = pokemon_name


def show_detail_view():
    """Render the Pokemon detail page"""
    if st.button("← Back to Home"):
        navigate_to_home()
        st.rerun()
        
    name = st.session_state.selected_pokemon
    data = get_pokemon_data(name)
    
    if data:
        st.title(f"#{data['id']} {data['name'].title()}")
        
        # Layout: 2 Columns
        col1, col2 = st.columns([1, 2])
        
        with col1:
            # Shiny Toggle
            is_shiny = st.toggle("✨ Shiny Version")
            
            # Display Image (Static High Quality)
            if is_shiny:
                sprite_url = data['sprites']['other']['official-artwork']['front_shiny']
                if not sprite_url:
                    sprite_url = data['sprites']['front_shiny']
            else:
                sprite_url = data['sprites']['other']['official-artwork']['front_default']
                if not sprite_url:
                    sprite_url = data['sprites']['front_default']
                
            st.image(sprite_url, use_container_width=True)
            
            # Audio (Cries)
            cries = data.get('cries', {})
            latest_cry = cries.get('latest')
            if latest_cry:
                st.audio(latest_cry)
            
        with col2:
            # Basic Info
            st.subheader("General Info")
            
            # Description (Flavor Text)
            species_url = data['species']['url']
            species_data = get_species_data(species_url)
            
            if species_data:
                description = get_pokemon_description(species_data)
                st.info(description)

            # Type Icons
            st.write("**Type:**")
            type_cols = st.columns(len(data['types']) + 2)  # Extra columns for spacing
            for i, t in enumerate(data['types']):
                type_name = t['type']['name']
                icon_url = get_type_icon_url(type_name)
                with type_cols[i]:
                    st.image(icon_url, width=100)
            
            st.write(f"**Height:** {data['height']/10} m")
            st.write(f"**Weight:** {data['weight']/10} kg")
            
            # Abilities
            abilities_info = get_abilities_info(data)
            abilities_text = ", ".join(abilities_info['normal'])
            if abilities_info['hidden']:
                abilities_text += f" | {abilities_info['hidden']} (Hidden)"
            st.write(f"**Abilities:** {abilities_text}")
            
            # Gender Ratio (from species data)
            if species_data:
                gender_ratio = get_gender_ratio(species_data)
                if gender_ratio.get('genderless'):
                    st.write("**Gender:** Genderless")
                else:
                    st.write(f"**Gender:** ♂ {gender_ratio['male']:.1f}% / ♀ {gender_ratio['female']:.1f}%")
            
            # Type Effectiveness Button
            st.write("")  # Spacer
            if st.button("🛡️ View Type Effectiveness"):
                types = [t['type']['name'] for t in data['types']]
                show_effectiveness_modal(types)

            # Stats
            st.subheader("Base Stats")
            for stat in data['stats']:
                stat_key = stat['stat']['name']
                config = STAT_CONFIG.get(stat_key, {"color": "#888888", "name": stat_key})
                
                stat_name = config['name']
                color = config['color']
                base_stat = stat['base_stat']
                percentage = min(base_stat / 255 * 100, 100)
                
                st.markdown(f"""
                <div style="display: flex; align-items: center; margin-bottom: 5px;">
                    <div style="width: 80px; font-weight: bold; color: #555;">{stat_name}</div>
                    <div style="width: 40px; text-align: right; margin-right: 10px; font-weight: bold;">{base_stat}</div>
                    <div style="flex-grow: 1; background-color: #f0f0f0; border-radius: 10px; height: 10px;">
                        <div style="width: {percentage}%; background-color: {color}; height: 100%; border-radius: 10px;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        # Evolution Chain & Varieties
        st.divider()
        
        if species_data:
            # --- Varieties (Mega, Gmax, etc.) ---
            varieties = get_pokemon_varieties(species_data, data['name'])
            
            if varieties:
                st.subheader("Varieties & Forms")
                v_cols = st.columns(min(len(varieties), 5))  # Limit columns to avoid crowding
                for i, variety in enumerate(varieties):
                    v_name = variety['pokemon']['name'].replace('-', ' ').title()
                    v_url_name = variety['pokemon']['name']
                    # Get ID for image
                    v_id = variety['pokemon']['url'].split('/')[-2]
                    v_img = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{v_id}.png"
                    
                    with v_cols[i % 5]:
                        st.image(v_img, width=80)
                        if st.button(v_name, key=f"var_{v_id}"):
                            navigate_to_detail(v_url_name)
                            st.rerun()
                st.divider()

            # --- Evolution Chain ---
            st.subheader("Evolution Chain")
            evo_list = get_evolution_chain(species_url)
            
            if evo_list:
                evo_cols = st.columns(len(evo_list))
                for i, evo in enumerate(evo_list):
                    with evo_cols[i]:
                        evo_id = evo['id']
                        evo_name = evo['name'].title()
                        evo_img = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{evo_id}.png"
                        
                        st.image(evo_img, width=100)
                        if st.button(evo_name, key=f"evo_{evo_id}"):
                            navigate_to_detail(evo['name'])
                            st.rerun()
    else:
        st.error("Pokemon not found!")
        if st.button("Go Back"):
            navigate_to_home()
            st.rerun()
