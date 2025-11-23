"""
Minimal Pokedex - Streamlit App
Main entry point
"""
import streamlit as st
from src.ui.home import show_home_view
from src.ui.detail import show_detail_view
from src.ui.battle import show_battle_view

# Set page config
st.set_page_config(page_title="Minimal Pokedex", page_icon="🔴", layout="wide")

# --- Sidebar Navigation ---
with st.sidebar:
    st.title("🔴 Pokedex AI")
    app_mode = st.radio("Menu", ["Pokedex", "Battle Analyzer"], index=0)
    st.markdown("---")
    st.markdown("Powered by **Groq** & **PokeAPI**")

# --- Main App Logic ---
if app_mode == "Battle Analyzer":
    show_battle_view()
else:
    # Pokedex Mode (Home/Detail)
    if 'view' not in st.session_state:
        st.session_state.view = 'home'
    if 'selected_pokemon' not in st.session_state:
        st.session_state.selected_pokemon = None

    if st.session_state.view == 'home':
        show_home_view()
    elif st.session_state.view == 'detail':
        show_detail_view()
