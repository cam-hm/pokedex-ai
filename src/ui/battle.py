import streamlit as st
from src.api.pokeapi_client import get_all_pokemon_names, get_pokemon_data
from src.services.ai_service import PokemonChatbot
from src.config.items import COMPETITIVE_ITEMS
from src.config.natures import NATURES
from src.services.stats_service import calculate_all_stats

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
                # 2. Stats & Info
                base_stats = {s['stat']['name']: s['base_stat'] for s in p_data['stats']}
                types = [t['type']['name'].title() for t in p_data['types']]
                
                # Type Badges
                st.markdown(f"**Types:** {', '.join(types)}")
                
                # --- Advanced Stats (Nature & EVs) ---
                with st.expander("📊 Stats, Nature & EVs", expanded=False):
                    nature_name = st.selectbox("Nature", list(NATURES.keys()), index=list(NATURES.keys()).index("Hardy"), key=f"nature_{key_suffix}")
                    
                    # Dynamic EV Sliders (Prevent > 510 Total)
                    # Map full stat names to session state keys
                    stat_map = {
                        'hp': 'hp', 'attack': 'atk', 'defense': 'def',
                        'special-attack': 'spa', 'special-defense': 'spd', 'speed': 'spe'
                    }
                    
                    # 1. Get current values from session state to calculate budget
                    current_evs = {}
                    for stat, short_key in stat_map.items():
                        key = f"ev_{short_key}_{key_suffix}"
                        current_evs[stat] = st.session_state.get(key, 0)
                    
                    total_used = sum(current_evs.values())
                    remaining_global = 510 - total_used
                    
                    st.caption(f"Total EVs: {total_used}/510")
                    
                    cols = st.columns(3)
                    
                    # Helper to render slider with dynamic max
                    def render_ev_slider(col_idx, label, stat_name):
                        short_key = stat_map[stat_name]
                        key = f"ev_{short_key}_{key_suffix}"
                        current_val = current_evs[stat_name]
                        
                        # Max allowed is current value + whatever is left globally
                        # But never more than 252
                        dynamic_max = min(252, current_val + remaining_global)
                        
                        # Ensure current value doesn't exceed new max (sanity check)
                        safe_val = min(current_val, dynamic_max)
                        
                        if dynamic_max == 0:
                            # Avoid Streamlit error: min_value must be < max_value
                            # If budget is full, lock this slider at 0
                            return cols[col_idx].slider(label, 0, 252, 0, key=key, disabled=True)
                        else:
                            return cols[col_idx].slider(label, 0, dynamic_max, safe_val, key=key)

                    evs = {}
                    evs['hp'] = render_ev_slider(0, "HP", 'hp')
                    evs['attack'] = render_ev_slider(1, "Atk", 'attack')
                    evs['defense'] = render_ev_slider(2, "Def", 'defense')
                    evs['special-attack'] = render_ev_slider(0, "SpA", 'special-attack')
                    evs['special-defense'] = render_ev_slider(1, "SpD", 'special-defense')
                    evs['speed'] = render_ev_slider(2, "Spd", 'speed')
                
                # Calculate Real Stats (Level 50)
                real_stats = calculate_all_stats(base_stats, evs, NATURES[nature_name])
                
                # Stats Grid (Show Real Stats)
                st.markdown("##### Real Stats (Lv. 50)")
                s_col1, s_col2 = st.columns(2)
                with s_col1:
                    st.write(f"❤️ **HP:** {real_stats['hp']} (Base: {base_stats['hp']})")
                    st.write(f"⚔️ **Atk:** {real_stats['attack']} (Base: {base_stats['attack']})")
                    st.write(f"🛡️ **Def:** {real_stats['defense']} (Base: {base_stats['defense']})")
                with s_col2:
                    st.write(f"✨ **SpA:** {real_stats['special-attack']} (Base: {base_stats['special-attack']})")
                    st.write(f"🔰 **SpD:** {real_stats['special-defense']} (Base: {base_stats['special-defense']})")
                    st.write(f"💨 **Spd:** {real_stats['speed']} (Base: {base_stats['speed']})")

                # 3. Moves & Items

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
                real_stats = {}
                nature_name = "Hardy"
                evs = {}
                
            return p_name, p_data, selected_moves, selected_item, real_stats, nature_name, evs

    # Render both cards
    p1_name, p1_data, p1_moves, p1_item, p1_stats, p1_nature, p1_evs = render_battle_card(col1, "My Pokemon", "1", all_pokemon.index("charizard") if "charizard" in all_pokemon else 0)
    p2_name, p2_data, p2_moves, p2_item, p2_stats, p2_nature, p2_evs = render_battle_card(col2, "Opponent", "2", all_pokemon.index("blastoise") if "blastoise" in all_pokemon else 1)

    st.markdown("---")

    if st.button("🚀 Analyze Matchup", type="primary", use_container_width=True):
        if p1_data and p2_data:
            with st.spinner("🤖 AI is analyzing the battle..."):
                analysis = st.session_state.chatbot.analyze_matchup(
                    p1_name, p1_data, p1_moves, p1_item, p1_stats, p1_nature,
                    p2_name, p2_data, p2_moves, p2_item, p2_stats, p2_nature
                )
                st.markdown("### 📊 Battle Analysis")
                st.markdown(analysis)
        else:
            st.error("Please select both Pokemon to analyze.")
