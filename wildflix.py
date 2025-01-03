import streamlit as st
st.set_page_config(layout="wide")
import pandas as pd
from pages import accueil, top, nouveautes, genre, langue, projet
from streamlit_option_menu import option_menu

# Menu horizontal 
page = option_menu(
    None,  # Pas de titre pour le menu
    ["Accueil", "Top 10 aujourd'hui", "Nouveautés", "Genre", "Langue", "Notre projet"],  # Options du menu
    icons=['house', 'item_icon', 'item_icon', 'list', 'list', 'info-circle'],  # Icônes correspondantes
    menu_icon="cast",  # Icône du menu global
    default_index=0,  # Page par défaut
    orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#007bff", "color": "white"}}
    )
      
if page=="Accueil":
    accueil()
elif page=="Top 10 aujourd'hui": 
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