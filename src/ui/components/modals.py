"""
UI Components - Modals
Reusable modal components
"""
import streamlit as st
from src.services.type_service import get_type_effectiveness, get_type_icon_url


@st.dialog("Type Effectiveness")
def show_effectiveness_modal(types):
    """
    Display Type Effectiveness modal with weaknesses, resistances, and immunities
    
    Args:
        types (list): List of Pokemon types
    """
    effectiveness = get_type_effectiveness(types)
    
    weaknesses = []
    resistances = []
    immunities = []
    
    for t, multiplier in effectiveness.items():
        if multiplier > 1.0:
            weaknesses.append((t, multiplier))
        elif multiplier == 0.0:
            immunities.append(t)
        elif multiplier < 1.0:
            resistances.append((t, multiplier))
            
    # Helper to render type badge
    def render_type_badge(type_name, multiplier=None):
        icon_url = get_type_icon_url(type_name)
        
        suffix = ""
        if multiplier is not None:
            suffix = f" (x{int(multiplier) if multiplier.is_integer() else multiplier})"
            
        st.markdown(f"""
            <div style="display: flex; align-items: center; margin-bottom: 5px;">
                <img src="{icon_url}" height="20" style="margin-right: 8px;" />
                <span>{type_name.title()}{suffix}</span>
            </div>
        """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Weaknesses ❌")
        if weaknesses:
            for t, mult in weaknesses:
                render_type_badge(t, mult)
        else:
            st.write("None")
            
    with col2:
        st.subheader("Resistances 🛡️")
        if resistances:
            for t, mult in resistances:
                render_type_badge(t, mult)
        else:
            st.write("None")
            
    if immunities:
        st.subheader("Immunities 🚫")
        for t in immunities:
            render_type_badge(t)
