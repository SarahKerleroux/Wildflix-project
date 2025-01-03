import streamlit as st
import pandas as pd
from pages_leo import *
from streamlit_option_menu import option_menu

df = pd.read_csv('last_df.csv')

# Enlever les marges sur streamlit
st.set_page_config(layout="wide")

# Menu horizontal 
pages = option_menupages = option_menu(
    None,  # Pas de titre pour le menu
    ["Accueil", "Top 10 aujourd'hui", "Nouveautés", "Genre", "Langue", "Notre projet"],  # Options du menu
    icons=['house', 'item_icon', 'item_icon', 'list', 'list', 'info-circle'],  # Icônes correspondantes
    menu_icon="cast",  # Icône du menu global
    default_index=0,  # Page par défaut
    orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#007bff", "color": "white"}}
    )
      
if pages=="Accueil":
    accueil()
elif pages=="Top 10 aujourd'hui": 
    top()
elif pages=="Nouveautés":
    nouveautes()
elif pages=="Genre":
    genre()
elif pages=="Langue":
    langue()
elif pages=="Notre projet":
    projet()
else :
    accueil()