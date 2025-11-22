import streamlit as st
import requests

# Set page config
st.set_page_config(page_title="Minimal Pokedex", page_icon="🔴", layout="wide")

# --- Session State Management ---
if 'view' not in st.session_state:
    st.session_state.view = 'home'
if 'selected_pokemon' not in st.session_state:
    st.session_state.selected_pokemon = None

def navigate_to_detail(pokemon_name):
    st.session_state.view = 'detail'
    st.session_state.selected_pokemon = pokemon_name

def navigate_to_home():
    st.session_state.view = 'home'
    st.session_state.selected_pokemon = None

# --- Helper Functions ---
@st.cache_data
def get_pokemon_list(limit=50, offset=0):
    url = f"https://pokeapi.co/api/v2/pokemon?limit={limit}&offset={offset}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['results']
    return []

def get_pokemon_data(name):
    url = f"https://pokeapi.co/api/v2/pokemon/{name}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# --- Constants ---
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

STAT_CONFIG = {
    "hp": {"color": "#4CAF50", "name": "HP"},
    "attack": {"color": "#FDD835", "name": "Attack"},
    "defense": {"color": "#FF9800", "name": "Defense"},
    "special-attack": {"color": "#2196F3", "name": "Sp. Atk"},
    "special-defense": {"color": "#9C27B0", "name": "Sp. Def"},
    "speed": {"color": "#E91E63", "name": "Speed"}
}

# --- Views ---

def show_home_view():
    st.title("🔴 Minimal Pokedex")
    st.markdown("Select a Pokemon to view details!")
    
    # Search Bar
    search_query = st.text_input("Search Pokemon:", "").lower()
    if search_query:
        if st.button("Search"):
            navigate_to_detail(search_query)
            st.rerun()

    # Generation Selector
    selected_gen = st.selectbox("Select Generation:", list(GENERATIONS.keys()))
    gen_params = GENERATIONS[selected_gen]

    # Pokemon Grid
    pokemon_list = get_pokemon_list(limit=gen_params['limit'], offset=gen_params['offset'])
    
    cols = st.columns(5) # 5 columns grid
    for i, pokemon in enumerate(pokemon_list):
        # Extract ID from URL for image
        p_id = pokemon['url'].split('/')[-2]
        p_name = pokemon['name'].title()
        p_img = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{p_id}.png"
        
        with cols[i % 5]:
            st.image(p_img, width=100)
            if st.button(f"#{p_id} {p_name}", key=f"btn_{p_id}"):
                navigate_to_detail(pokemon['name'])
                st.rerun()

def show_detail_view():
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
            # Display Image
            sprite_url = data['sprites']['other']['official-artwork']['front_default']
            if not sprite_url:
                sprite_url = data['sprites']['front_default']
            st.image(sprite_url, use_column_width=True)
            
            # Audio (Cries)
            cries = data.get('cries', {})
            latest_cry = cries.get('latest')
            if latest_cry:
                st.audio(latest_cry)
            
        with col2:
            # Basic Info
            st.subheader("General Info")
            types = [t['type']['name'].title() for t in data['types']]
            st.write(f"**Type:** {', '.join(types)}")
            st.write(f"**Height:** {data['height']/10} m")
            st.write(f"**Weight:** {data['weight']/10} kg")
            
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

        # Evolution Chain
        st.divider()
        st.subheader("Evolution Chain")
        
        species_url = data['species']['url']
        species_res = requests.get(species_url)
        
        if species_res.status_code == 200:
            species_data = species_res.json()
            evo_chain_url = species_data['evolution_chain']['url']
            evo_res = requests.get(evo_chain_url)
            
            if evo_res.status_code == 200:
                evo_data = evo_res.json()
                chain = evo_data['chain']
                
                evo_list = []
                def parse_evolution(chain_node):
                    species_name = chain_node['species']['name']
                    species_id = chain_node['species']['url'].split('/')[-2]
                    evo_list.append({'name': species_name, 'id': species_id})
                    for next_node in chain_node['evolves_to']:
                        parse_evolution(next_node)
                parse_evolution(chain)
                
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

# --- Main App Logic ---
if st.session_state.view == 'home':
    show_home_view()
elif st.session_state.view == 'detail':
    show_detail_view()
