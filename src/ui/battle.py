import streamlit as st
from src.api.pokeapi_client import get_all_pokemon_names, get_pokemon_data
from src.services.ai_service import PokemonChatbot
from src.config.items import COMPETITIVE_ITEMS

def show_battle_view():
    st.title("⚔️ AI Battle Analyzer")
    st.markdown("Select two Pokemon to analyze their matchup using AI.")

    # Initialize AI Service
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = PokemonChatbot()

    # Fetch all Pokemon names for autocomplete
    all_pokemon = get_all_pokemon_names()

    # Fetch all Pokemon names for autocomplete
    all_pokemon = get_all_pokemon_names()

    col1, col2 = st.columns(2)

    def render_battle_card(col, title, key_suffix, default_index):
        with col:
            st.subheader(title)
            # Select Pokemon
            p_name = st.selectbox(
                "Select Pokemon", 
                all_pokemon, 
                index=default_index, 
                key=f"p_select_{key_suffix}",
                label_visibility="collapsed"
            )
            
            p_data = get_pokemon_data(p_name)
            
            if p_data:
                # 1. Fixed Height Image Container (200px)
                # Try Showdown GIF first, fallback to static
                sprite = p_data['sprites']['other']['showdown']['front_default']
                if not sprite:
                    sprite = p_data['sprites']['other']['official-artwork']['front_default']
                
                st.markdown(f"""
                <div style="height: 220px; display: flex; align-items: center; justify-content: center; border-radius: 10px; margin-bottom: 10px;">
                    <img src="{sprite}" style="max-height: 200px; max-width: 100%; object-fit: contain;">
                </div>
                """, unsafe_allow_html=True)
                
                # 2. Stats & Info
                stats = {s['stat']['name']: s['base_stat'] for s in p_data['stats']}
                types = [t['type']['name'].title() for t in p_data['types']]
                
                # Type Badges (Simple text for now, but aligned)
                st.markdown(f"**Types:** {', '.join(types)}")
                
                # Stats Grid
                s_col1, s_col2 = st.columns(2)
                with s_col1:
                    st.write(f"❤️ **HP:** {stats.get('hp')}")
                    st.write(f"⚔️ **Atk:** {stats.get('attack')}")
                    st.write(f"🛡️ **Def:** {stats.get('defense')}")
                with s_col2:
                    st.write(f"✨ **SpA:** {stats.get('special-attack')}")
                    st.write(f"🔰 **SpD:** {stats.get('special-defense')}")
                    st.write(f"💨 **Spd:** {stats.get('speed')}")

                # 3. Moves & Items
                st.markdown("---")
                all_moves = [m['move']['name'] for m in p_data['moves']]
                selected_moves = st.multiselect(
                    "Select Moves (Max 4)", 
                    all_moves, 
                    max_selections=4,
                    key=f"moves_{key_suffix}"
                )
                
                selected_item = st.selectbox(
                    "Held Item",
                    COMPETITIVE_ITEMS,
                    key=f"item_{key_suffix}"
                )
                
            else:
                selected_moves = []
                selected_item = "None"
                
            return p_name, p_data, selected_moves, selected_item

    # Render both cards
    # Render both cards
    p1_name, p1_data, p1_moves, p1_item = render_battle_card(col1, "My Pokemon", "1", all_pokemon.index("charizard") if "charizard" in all_pokemon else 0)
    p2_name, p2_data, p2_moves, p2_item = render_battle_card(col2, "Opponent", "2", all_pokemon.index("blastoise") if "blastoise" in all_pokemon else 1)

    st.markdown("---")

    if st.button("🚀 Analyze Matchup", type="primary", use_container_width=True):
        if p1_data and p2_data:
            with st.spinner("🤖 AI is analyzing the battle..."):
                analysis = st.session_state.chatbot.analyze_matchup(
                    p1_name, p1_data, p1_moves, p1_item,
                    p2_name, p2_data, p2_moves, p2_item
                )
                st.markdown("### 📊 Battle Analysis")
                st.markdown(analysis)
        else:
            st.error("Please select both Pokemon to analyze.")
