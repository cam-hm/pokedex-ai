"""
Minimal Pokedex - Streamlit App
Main entry point
"""
import streamlit as st
from src.ui.home import show_home_view
from src.ui.detail import show_detail_view

# Set page config
st.set_page_config(page_title="Minimal Pokedex", page_icon="🔴", layout="wide")

# --- Session State Management ---
if 'view' not in st.session_state:
    st.session_state.view = 'home'
if 'selected_pokemon' not in st.session_state:
    st.session_state.selected_pokemon = None

# --- Main App Logic ---
if st.session_state.view == 'home':
    show_home_view()
elif st.session_state.view == 'detail':
    show_detail_view()
