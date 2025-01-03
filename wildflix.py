import streamlit as st
st.set_page_config(layout="wide")
import pandas as pd
from pages import accueil, match, top, nouveautes, genre, langue, projet
from streamlit_option_menu import option_menu

# Menu horizontal 
page = option_menu(
    None,  # Pas de titre pour le menu
    ["Accueil", "Match", "Top 10", "Nouveautés", "Genre", "Langue", "Notre projet"],  # Options du menu
    icons=['house', 'people', 'star', '', 'search', 'list', 'info-circle'],  # Icônes correspondantes
    menu_icon="cast",  # Icône du menu global
    default_index=0,  # Page par défaut
    orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#007bff", "color": "white"}}
    )
      
if page=="Accueil":
    accueil()
elif page=="Match":
    match()
elif page=="Top 10": 
    top()
elif page=="Nouveautés":
    nouveautes()
elif page=="Genre":
    genre()
elif page=="Langue":
    langue()
elif page=="Notre projet":
    projet()
else :
    accueil()