import pandas as pd
import streamlit as st
import base64
import streamlit as st
import ast


df = pd.read_csv("last_df.csv")
df_genre = pd.read_csv("df_for_genre.csv")

fr = df[df["original_language"] == "fr"].sort_values(by="popularity", ascending=False)
en = df[df["original_language"] == "en"].sort_values(by="popularity", ascending=False)
it = df[df["original_language"] == "it"].sort_values(by="popularity", ascending=False)
ja = df[df["original_language"] == "ja"].sort_values(by="popularity", ascending=False)
ko = df[df["original_language"] == "ko"].sort_values(by="popularity", ascending=False)

nouveautes_fr = df[df["original_language"] == "fr"].sort_values(by="release_date", ascending=False).head(10)
nouveautes_en = df[df["original_language"] == "en"].sort_values(by="release_date", ascending=False).head(10)
nouveautes_it = df[df["original_language"] == "it"].sort_values(by="release_date", ascending=False).head(10)
nouveautes_ja = df[df["original_language"] == "ja"].sort_values(by="release_date", ascending=False).head(10)
nouveautes_ko = df[df["original_language"] == "ko"].sort_values(by="release_date", ascending=False).head(10)

drame = df[df["genre_ids"] == "Drame"].sort_values(by="popularity", ascending=False)
comedie = df[df["genre_ids"] == "Comédie"].sort_values(by="popularity", ascending=False)
romance = df[df["genre_ids"] == "Romance"].sort_values(by="popularity", ascending=False)
thriller = df[df["genre_ids"] == "Thriller"].sort_values(by="popularity", ascending=False)
action = df[df["genre_ids"] == "Action"].sort_values(by="popularity", ascending=False)
crime = df[df["genre_ids"] == "Crime"].sort_values(by="popularity", ascending=False)
documentaire = df[df["genre_ids"] == "Documentaire"].sort_values(by="popularity", ascending=False)
horreur = df[df["genre_ids"] == "Horreur"].sort_values(by="popularity", ascending=False)
aventure = df[df["genre_ids"] == "Aventure"].sort_values(by="popularity", ascending=False)
mystere = df[df["genre_ids"] == "Mystère"].sort_values(by="popularity", ascending=False)
fantastique = df[df["genre_ids"] == "Fantastique"].sort_values(by="popularity", ascending=False)
musique = df[df["genre_ids"] == "Musique"].sort_values(by="popularity", ascending=False)
animation = df[df["genre_ids"] == "Animation"].sort_values(by="popularity", ascending=False)
familial = df[df["genre_ids"] == "Familial"].sort_values(by="popularity", ascending=False)
histoire = df[df["genre_ids"] == "Histoire"].sort_values(by="popularity", ascending=False)
science_fiction = df[df["genre_ids"] == "Science-fiction"].sort_values(by="popularity", ascending=False)
telefilm = df[df["genre_ids"] == "Téléfilm"].sort_values(by="popularity", ascending=False)
guerre = df[df["genre_ids"] == "Guerre"].sort_values(by="popularity", ascending=False)
western = df[df["genre_ids"] == "Western"].sort_values(by="popularity", ascending=False)


def add_background(image_path):
    """
    Ajoute une image de fond en utilisant un encodage base64.
    """
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded_string}");
            background-size: cover;
            background-repeat: no-repeat;
            background-position: center;  
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def accueil():
    # Ajouter l'image de fond
    add_background("fond.png")
    
    # Contenu de l'application
    #st.title("Bienvenue")
    st.markdown("""
        <style>
        .stSelectbox {
            color: rgb(255, 255, 255);
            background-color: gray;
            border-radius: 5px;
            border: 2px solid #007BFF;
            box-shadow: 0px 0px 10px #007BFF;
        }
        .stSelectbox > div[data-baseweb="select"] > div {
            font-family: inherit;
            font-size: 16px;
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)

    # Charger les fichiers CSV
    last_df = pd.read_csv("last_df.csv")
    df_recommendations = pd.read_csv("df_20_000_recomandation.csv")

    # URL de base pour les affiches des films
    base_url = 'https://image.tmdb.org/t/p/original'

    # Afficher l'image avec alignement centré
    col1, col2, col3, col4, col5 = st.columns([1.2, 1.2, 2.6, 0.8, 0.7])  # Colonnes pour aligner au centre
    with col3:
        st.image("logo.png", width=330)
    st.markdown(
        f"<h1 style='color:#FFFFFF; text-align: center;'>Bienvenue sur notre Système de Recommandation</h1>",
        unsafe_allow_html=True
    )

    st.write('')

    # Trier les titres par popularité
    sorted_titles_by_popularity = df_recommendations.sort_values(by="popularity", ascending=False)["title"].dropna().unique()

    # Barre de recherche de film
    col_empty1, col_search, col_empty2 = st.columns([1, 4, 1])
    with col_search:
        search_query = st.selectbox(
            "Sélectionnez ou écrivez un titre de film :",
            options=[""] + list(sorted_titles_by_popularity)
        )

    if search_query:
        selected_movie = last_df[last_df['title'] == search_query]

        if not selected_movie.empty:
            movie_title = selected_movie.iloc[0]['title']
            st.subheader(f"🎬 Film sélectionné : {movie_title}")
            if pd.notna(selected_movie.iloc[0]['poster_path']):
                st.image(base_url + selected_movie.iloc[0]['poster_path'], width=300)
            st.write(f"**Description** : {selected_movie.iloc[0]['overview']}")

            # Rechercher les recommandations dans df_recommendations
            recommendations = df_recommendations[df_recommendations['title'] == movie_title]

            if not recommendations.empty:
                # Extraire dynamiquement les recommandations valides
                recommended_titles = [
                    recommendations.iloc[0][col]
                    for col in recommendations.columns if "Recommendation_" in col and pd.notna(recommendations.iloc[0][col])
                ]

                # Assurer qu'on trouve les recommandations dans last_df
                recommended_movies = last_df[last_df['title'].isin(recommended_titles)]

                # Afficher les recommandations
                st.write("### 🍿 Films recommandés :")
                col1, col2, col3, col4, col5 = st.columns(5)

                # Créer une liste complète avec des "places vides" pour éviter les bugs d'affichage
                while len(recommended_movies) < 5:
                    empty_row = {'poster_path': None, 'title': "Aucune recommandation", 'overview': ""}
                    recommended_movies = pd.concat([recommended_movies, pd.DataFrame([empty_row])])

                # Convertir en liste pour l'affichage
                recommended_movies_list = recommended_movies.to_dict(orient="records")

                # Ajouter les films recommandés dans chaque colonne
                for col, movie in zip([col1, col2, col3, col4, col5], recommended_movies_list):
                    with col:
                        if pd.notna(movie['poster_path']):
                            st.image(f"{base_url}{movie['poster_path']}", use_container_width=True)
                        else:
                            st.image("https://via.placeholder.com/300x450?text=Pas+d'affiche", use_container_width=True)
                        st.write(f"**{movie['title']}**")
                        st.write(movie['overview'])




def top():
    st.markdown(
        "<h1 style='color: #FFD700; text-align: center;'>Découvrez le Top 10</h1>", 
        unsafe_allow_html=True
    )
    st.write('')
    st.write('')
    selected_top = st.selectbox('Sélectionnez une langue',
['choisir','Français', 'Anglais', 'Italien', 'Japonais', 'Coréen'], index=0)
    
    if selected_top == "Français":
        st.subheader("🍿 Top 10 Français")
        st.write('')
        base_url = 'https://image.tmdb.org/t/p/original'
       
        # Parcourir les 10 premiers films français
        for i in (range(min(len(fr), 10))):
            row = fr.iloc[i]
            st.markdown("""
            <style>
                hr {
                    margin: 2rem auto; /* Centrage automatique et espacement */
                    border: 0;
                    border-top: 2px solid #ADD8E6; /* Bleu pâle */
                    width: 90%; /* Réduction de la largeur */
                }
            </style>
            <hr>
            """, unsafe_allow_html=True)#ligne horizontale
    
            # Diviser en colonnes : une pour l'image et une pour le synopsis
            
            empty1, col1, empty2, col2, empty3, col3, empty4 = st.columns([0.6, 1.4, 0.2, 2.5, 0.2, 2, 0.6])# La colonne 2 est deux fois plus large
            
            # Colonne 1 : Affiche du film
            with col1:
                if pd.notna(row['poster_path']):
                    st.write('')
                    st.write('')
                    st.write('')
                    st.write('')
                    st.write('')
                    st.write('')
                    st.write('')
                    st.image(base_url + row['poster_path'], width=500)
            
            # Colonne 2 : Titre et synopsis
            with col2:
                st.markdown(
                f"<h2 style='color:rgb(152, 227, 252); text-align: center;'>{row['title']}</h2>",
                unsafe_allow_html=True
                )
                #st.header(row['title'])  # Afficher le titre du film
                st.write("")
                st.write("")
                if pd.notna(row['overview']):
                    st.write(f"**Synopsis :** *{row['overview']}*")  # Afficher le synopsis
                    st.write("")
                    st.write("")
                st.write(f"**Acteurs :** *{row['actors']}*")
                st.write("")
                st.write(f"**Réalisateurs :** *{row['director']}*")

            # Affiche les informations du film        
            with col3:
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.write(f"|**Genre :** *{row['genre_ids']}*")
                st.write("")
                st.write(f"| *Date de Sortie : {row['release_date']}*")
                st.write(f"| *Durée : {row['runtime_min']} minutes*")
                st.write(f"| *Popularité : {row['popularity']}*")
                st.write("")
                st.write(f"| *Note du Public sur 10 : {row['vote_average']}*")
                st.write(f"| *Nombre de votes : {row['vote_count']}*")
                

    elif selected_top == "Anglais":
        st.subheader("🍿 Top 10 Anglais")
        st.write('')
        base_url = 'https://image.tmdb.org/t/p/original'
        
        # Parcourir les 10 premiers films Anglais
        for i in (range(min(len(en), 10))):
            row = en.iloc[i]
            st.markdown("""
            <style>
                hr {
                    margin: 2rem auto; /* Centrage automatique et espacement */
                    border: 0;
                    border-top: 2px solid #ADD8E6; /* Bleu pâle */
                    width: 90%; /* Réduction de la largeur */
                }
            </style>
            <hr>
            """, unsafe_allow_html=True)#ligne horizontale
        
            # Diviser en colonnes : une pour l'image et une pour le synopsis
            
            empty1, col1, empty2, col2, empty3, col3, empty4 = st.columns([0.6, 1.4, 0.2, 2.5, 0.2, 2, 0.6])# La colonne 2 est deux fois plus large
            
            # Colonne 1 : Affiche du film
            with col1:
                if pd.notna(row['poster_path']):
                    st.write('')
                    st.write('')
                    st.write('')
                    st.write('')
                    st.write('')
                    st.write('')
                    st.write('')
                    st.image(base_url + row['poster_path'], width=500)
            
            # Colonne 2 : Titre et synopsis
            with col2:
                st.markdown(
                f"<h2 style='color:rgb(152, 227, 252); text-align: center;'>{row['title']}</h2>",
                unsafe_allow_html=True
                )
                #st.header(row['title'])  # Afficher le titre du film
                st.write("")
                st.write("")
                if pd.notna(row['overview']):
                    st.write(f"**Synopsis :** *{row['overview']}*")  # Afficher le synopsis
                    st.write("")
                    st.write("")
                st.write(f"**Acteurs :** *{row['actors']}*")
                st.write("")
                st.write(f"**Réalisateurs :** *{row['director']}*")

            # Affiche les informations du film        
            with col3:
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.write(f"|**Genre :** *{row['genre_ids']}*")
                st.write("")
                st.write(f"| *Date de Sortie : {row['release_date']}*")
                st.write(f"| *Durée : {row['runtime_min']} minutes*")
                st.write(f"| *Popularité : {row['popularity']}*")
                st.write("")
                st.write(f"| *Note du Public sur 10 : {row['vote_average']}*")
                st.write(f"| *Nombre de votes : {row['vote_count']}*")


    elif selected_top == "Italien":
        st.subheader("🍿 Top 10 Italien")
        st.write('')
        base_url = 'https://image.tmdb.org/t/p/original'

        # Parcourir les 10 premiers films Italien
        for i in (range(min(len(it), 10))):
            row = it.iloc[i]
            st.markdown("""
            <style>
                hr {
                    margin: 2rem auto; /* Centrage automatique et espacement */
                    border: 0;
                    border-top: 2px solid #ADD8E6; /* Bleu pâle */
                    width: 90%; /* Réduction de la largeur */
                }
            </style>
            <hr>
            """, unsafe_allow_html=True)#ligne horizontale
        
            # Diviser en colonnes : une pour l'image et une pour le synopsis
            
            empty1, col1, empty2, col2, empty3, col3, empty4 = st.columns([0.6, 1.4, 0.2, 2.5, 0.2, 2, 0.6])# La colonne 2 est deux fois plus large
            
            # Colonne 1 : Affiche du film
            with col1:
                if pd.notna(row['poster_path']):
                    st.write('')
                    st.write('')
                    st.write('')
                    st.write('')
                    st.write('')
                    st.write('')
                    st.write('')
                    st.image(base_url + row['poster_path'], width=500)
            
            # Colonne 2 : Titre et synopsis
            with col2:
                st.markdown(
                f"<h2 style='color:rgb(152, 227, 252); text-align: center;'>{row['title']}</h2>",
                unsafe_allow_html=True
                )
                #st.header(row['title'])  # Afficher le titre du film
                st.write("")
                st.write("")
                if pd.notna(row['overview']):
                    st.write(f"**Synopsis :** *{row['overview']}*")  # Afficher le synopsis
                    st.write("")
                    st.write("")
                st.write(f"**Acteurs :** *{row['actors']}*")
                st.write("")
                st.write(f"**Réalisateurs :** *{row['director']}*")

            # Affiche les informations du film        
            with col3:
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.write(f"|**Genre :** *{row['genre_ids']}*")
                st.write("")
                st.write(f"| *Date de Sortie : {row['release_date']}*")
                st.write(f"| *Durée : {row['runtime_min']} minutes*")
                st.write(f"| *Popularité : {row['popularity']}*")
                st.write("")
                st.write(f"| *Note du Public sur 10 : {row['vote_average']}*")
                st.write(f"| *Nombre de votes : {row['vote_count']}*")


    elif selected_top == "Japonais":
        st.subheader("🍿 Top 10 Japonais")
        st.write('')
        base_url = 'https://image.tmdb.org/t/p/original'

        # Parcourir les 10 premiers films Japonais
        for i in (range(min(len(ja), 10))):
            row = ja.iloc[i]
            st.markdown("""
            <style>
                hr {
                    margin: 2rem auto; /* Centrage automatique et espacement */
                    border: 0;
                    border-top: 2px solid #ADD8E6; /* Bleu pâle */
                    width: 90%; /* Réduction de la largeur */
                }
            </style>
            <hr>
            """, unsafe_allow_html=True)#ligne horizontale
        
            # Diviser en colonnes : une pour l'image et une pour le synopsis
            
            empty1, col1, empty2, col2, empty3, col3, empty4 = st.columns([0.6, 1.4, 0.2, 2.5, 0.2, 2, 0.6])# La colonne 2 est deux fois plus large
            
            # Colonne 1 : Affiche du film
            with col1:
                if pd.notna(row['poster_path']):
                    st.write('')
                    st.write('')
                    st.write('')
                    st.write('')
                    st.write('')
                    st.write('')
                    st.write('')
                    st.image(base_url + row['poster_path'], width=500)
            
            # Colonne 2 : Titre et synopsis
            with col2:
                st.markdown(
                f"<h2 style='color:rgb(152, 227, 252); text-align: center;'>{row['title']}</h2>",
                unsafe_allow_html=True
                )
                #st.header(row['title'])  # Afficher le titre du film
                st.write("")
                st.write("")
                if pd.notna(row['overview']):
                    st.write(f"**Synopsis :** *{row['overview']}*")  # Afficher le synopsis
                    st.write("")
                    st.write("")
                st.write(f"**Acteurs :** *{row['actors']}*")
                st.write("")
                st.write(f"**Réalisateurs :** *{row['director']}*")

            # Affiche les informations du film        
            with col3:
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.write(f"|**Genre :** *{row['genre_ids']}*")
                st.write("")
                st.write(f"| *Date de Sortie : {row['release_date']}*")
                st.write(f"| *Durée : {row['runtime_min']} minutes*")
                st.write(f"| *Popularité : {row['popularity']}*")
                st.write("")
                st.write(f"| *Note du Public sur 10 : {row['vote_average']}*")
                st.write(f"| *Nombre de votes : {row['vote_count']}*")


    elif selected_top == "Coréen":
        st.subheader("🍿 Top 10 Coréen")
        st.write('')
        base_url = 'https://image.tmdb.org/t/p/original'

        # Parcourir les 10 premiers films Coréen
        for i in (range(min(len(ko), 10))):
            row = ko.iloc[i]
            st.markdown("""
            <style>
                hr {
                    margin: 2rem auto; /* Centrage automatique et espacement */
                    border: 0;
                    border-top: 2px solid #ADD8E6; /* Bleu pâle */
                    width: 90%; /* Réduction de la largeur */
                }
            </style>
            <hr>
            """, unsafe_allow_html=True)#ligne horizontale
        
            # Diviser en colonnes : une pour l'image et une pour le synopsis
            
            empty1, col1, empty2, col2, empty3, col3, empty4 = st.columns([0.6, 1.4, 0.2, 2.5, 0.2, 2, 0.6])# La colonne 2 est deux fois plus large
            
            # Colonne 1 : Affiche du film
            with col1:
                if pd.notna(row['poster_path']):
                    st.write('')
                    st.write('')
                    st.write('')
                    st.write('')
                    st.write('')
                    st.write('')
                    st.write('')
                    st.image(base_url + row['poster_path'], width=500)
            
            # Colonne 2 : Titre et synopsis
            with col2:
                st.markdown(
                f"<h2 style='color:rgb(152, 227, 252); text-align: center;'>{row['title']}</h2>",
                unsafe_allow_html=True
                )
                #st.header(row['title'])  # Afficher le titre du film
                st.write("")
                st.write("")
                if pd.notna(row['overview']):
                    st.write(f"**Synopsis :** *{row['overview']}*")  # Afficher le synopsis
                    st.write("")
                    st.write("")
                st.write(f"**Acteurs :** *{row['actors']}*")
                st.write("")
                st.write(f"**Réalisateurs :** *{row['director']}*")

            # Affiche les informations du film        
            with col3:
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.write(f"|**Genre :** *{row['genre_ids']}*")
                st.write("")
                st.write(f"| *Date de Sortie : {row['release_date']}*")
                st.write(f"| *Durée : {row['runtime_min']} minutes*")
                st.write(f"| *Popularité : {row['popularity']}*")
                st.write("")
                st.write(f"| *Note du Public sur 10 : {row['vote_average']}*")
                st.write(f"| *Nombre de votes : {row['vote_count']}*")



def nouveautes():
    st.markdown(
        "<h1 style='color: #FFD700; text-align: center;'>Explorez les nouveautés</h1>", 
        unsafe_allow_html=True
    )
    st.write('')
    st.write('')
    selected_top = st.selectbox('Sélectionnez une langue',
['choisir','Français', 'Anglais', 'Italien', 'Japonais', 'Coréen'], index=0)
    
    if selected_top == "Français":
        st.subheader("🍿 Nouveautés en Français")
        st.write('')
        base_url = 'https://image.tmdb.org/t/p/original'
       
        # Parcourir les 10 dernières sorties de films français
        for i in (range(min(len(nouveautes_fr), 10))):
            row = nouveautes_fr.iloc[i]
            st.markdown("""
            <style>
                hr {
                    margin: 2rem auto; /* Centrage automatique et espacement */
                    border: 0;
                    border-top: 2px solid #ADD8E6; /* Bleu pâle */
                    width: 90%; /* Réduction de la largeur */
                }
            </style>
            <hr>
            """, unsafe_allow_html=True)#ligne horizontale
    
            # Diviser en colonnes : une pour l'image et une pour le synopsis
            
            empty1, col1, empty2, col2, empty3, col3, empty4 = st.columns([0.6, 1.4, 0.2, 2.5, 0.2, 2, 0.6])# La colonne 2 est deux fois plus large
            
            # Colonne 1 : Affiche du film
            with col1:
                if pd.notna(row['poster_path']):
                    st.write('')
                    st.write('')
                    st.write('')
                    st.write('')
                    st.write('')
                    st.write('')
                    st.write('')
                    st.image(base_url + row['poster_path'], width=500)
            
            # Colonne 2 : Titre et synopsis
            with col2:
                st.markdown(
                f"<h2 style='color:rgb(152, 227, 252); text-align: center;'>{row['title']}</h2>",
                unsafe_allow_html=True
                )
                #st.header(row['title'])  # Afficher le titre du film
                st.write("")
                st.write("")
                if pd.notna(row['overview']):
                    st.write(f"**Synopsis :** *{row['overview']}*")  # Afficher le synopsis
                    st.write("")
                    st.write("")
                st.write(f"**Acteurs :** *{row['actors']}*")
                st.write("")
                st.write(f"**Réalisateurs :** *{row['director']}*")

            # Affiche les informations du film        
            with col3:
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.write(f"|**Genre :** *{row['genre_ids']}*")
                st.write("")
                st.write(f"| *Date de Sortie : {row['release_date']}*")
                st.write(f"| *Durée : {row['runtime_min']} minutes*")
                st.write(f"| *Popularité : {row['popularity']}*")
                st.write("")
                st.write(f"| *Note du Public sur 10 : {row['vote_average']}*")
                st.write(f"| *Nombre de votes : {row['vote_count']}*")
                

    elif selected_top == "Anglais":
        st.subheader("🍿 Nouveautés en Anglais")
        st.write('')
        base_url = 'https://image.tmdb.org/t/p/original'
        
        # Parcourir les 10 dernières sorties de films Anglais
        for i in (range(min(len(nouveautes_en), 10))):
            row = nouveautes_en.iloc[i]
            st.markdown("""
            <style>
                hr {
                    margin: 2rem auto; /* Centrage automatique et espacement */
                    border: 0;
                    border-top: 2px solid #ADD8E6; /* Bleu pâle */
                    width: 90%; /* Réduction de la largeur */
                }
            </style>
            <hr>
            """, unsafe_allow_html=True)#ligne horizontale
        
            # Diviser en colonnes : une pour l'image et une pour le synopsis
            
            empty1, col1, empty2, col2, empty3, col3, empty4 = st.columns([0.6, 1.4, 0.2, 2.5, 0.2, 2, 0.6])# La colonne 2 est deux fois plus large
            
            # Colonne 1 : Affiche du film
            with col1:
                if pd.notna(row['poster_path']):
                    st.write('')
                    st.write('')
                    st.write('')
                    st.write('')
                    st.write('')
                    st.write('')
                    st.write('')
                    st.image(base_url + row['poster_path'], width=500)
            
            # Colonne 2 : Titre et synopsis
            with col2:
                st.markdown(
                f"<h2 style='color:rgb(152, 227, 252); text-align: center;'>{row['title']}</h2>",
                unsafe_allow_html=True
                )
                #st.header(row['title'])  # Afficher le titre du film
                st.write("")
                st.write("")
                if pd.notna(row['overview']):
                    st.write(f"**Synopsis :** *{row['overview']}*")  # Afficher le synopsis
                    st.write("")
                    st.write("")
                st.write(f"**Acteurs :** *{row['actors']}*")
                st.write("")
                st.write(f"**Réalisateurs :** *{row['director']}*")

            # Affiche les informations du film        
            with col3:
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.write(f"|**Genre :** *{row['genre_ids']}*")
                st.write("")
                st.write(f"| *Date de Sortie : {row['release_date']}*")
                st.write(f"| *Durée : {row['runtime_min']} minutes*")
                st.write(f"| *Popularité : {row['popularity']}*")
                st.write("")
                st.write(f"| *Note du Public sur 10 : {row['vote_average']}*")
                st.write(f"| *Nombre de votes : {row['vote_count']}*")


    elif selected_top == "Italien":
        st.subheader("🍿 Nouveautés en Italien")
        st.write('')
        base_url = 'https://image.tmdb.org/t/p/original'

        # Parcourir les 10 dernières sorties de films Italien
        for i in (range(min(len(nouveautes_it), 10))):
            row = nouveautes_it.iloc[i]
            st.markdown("""
            <style>
                hr {
                    margin: 2rem auto; /* Centrage automatique et espacement */
                    border: 0;
                    border-top: 2px solid #ADD8E6; /* Bleu pâle */
                    width: 90%; /* Réduction de la largeur */
                }
            </style>
            <hr>
            """, unsafe_allow_html=True)#ligne horizontale
        
            # Diviser en colonnes : une pour l'image et une pour le synopsis
            
            empty1, col1, empty2, col2, empty3, col3, empty4 = st.columns([0.6, 1.4, 0.2, 2.5, 0.2, 2, 0.6])# La colonne 2 est deux fois plus large
            
            # Colonne 1 : Affiche du film
            with col1:
                if pd.notna(row['poster_path']):
                    st.write('')
                    st.write('')
                    st.write('')
                    st.write('')
                    st.write('')
                    st.write('')
                    st.write('')
                    st.image(base_url + row['poster_path'], width=500)
            
            # Colonne 2 : Titre et synopsis
            with col2:
                st.markdown(
                f"<h2 style='color:rgb(152, 227, 252); text-align: center;'>{row['title']}</h2>",
                unsafe_allow_html=True
                )
                #st.header(row['title'])  # Afficher le titre du film
                st.write("")
                st.write("")
                if pd.notna(row['overview']):
                    st.write(f"**Synopsis :** *{row['overview']}*")  # Afficher le synopsis
                    st.write("")
                    st.write("")
                st.write(f"**Acteurs :** *{row['actors']}*")
                st.write("")
                st.write(f"**Réalisateurs :** *{row['director']}*")

            # Affiche les informations du film        
            with col3:
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.write(f"|**Genre :** *{row['genre_ids']}*")
                st.write("")
                st.write(f"| *Date de Sortie : {row['release_date']}*")
                st.write(f"| *Durée : {row['runtime_min']} minutes*")
                st.write(f"| *Popularité : {row['popularity']}*")
                st.write("")
                st.write(f"| *Note du Public sur 10 : {row['vote_average']}*")
                st.write(f"| *Nombre de votes : {row['vote_count']}*")


    elif selected_top == "Japonais":
        st.subheader("🍿 Nouveautés en Japonais")
        st.write('')
        base_url = 'https://image.tmdb.org/t/p/original'

        # Parcourir les 10 dernières sorties de films Japonais
        for i in (range(min(len(nouveautes_ja), 10))):
            row = nouveautes_ja.iloc[i]
            st.markdown("""
            <style>
                hr {
                    margin: 2rem auto; /* Centrage automatique et espacement */
                    border: 0;
                    border-top: 2px solid #ADD8E6; /* Bleu pâle */
                    width: 90%; /* Réduction de la largeur */
                }
            </style>
            <hr>
            """, unsafe_allow_html=True)#ligne horizontale
        
            # Diviser en colonnes : une pour l'image et une pour le synopsis
            
            empty1, col1, empty2, col2, empty3, col3, empty4 = st.columns([0.6, 1.4, 0.2, 2.5, 0.2, 2, 0.6])# La colonne 2 est deux fois plus large
            
            # Colonne 1 : Affiche du film
            with col1:
                if pd.notna(row['poster_path']):
                    st.write('')
                    st.write('')
                    st.write('')
                    st.write('')
                    st.write('')
                    st.write('')
                    st.write('')
                    st.image(base_url + row['poster_path'], width=500)
            
            # Colonne 2 : Titre et synopsis
            with col2:
                st.markdown(
                f"<h2 style='color:rgb(152, 227, 252); text-align: center;'>{row['title']}</h2>",
                unsafe_allow_html=True
                )
                #st.header(row['title'])  # Afficher le titre du film
                st.write("")
                st.write("")
                if pd.notna(row['overview']):
                    st.write(f"**Synopsis :** *{row['overview']}*")  # Afficher le synopsis
                    st.write("")
                    st.write("")
                st.write(f"**Acteurs :** *{row['actors']}*")
                st.write("")
                st.write(f"**Réalisateurs :** *{row['director']}*")

            # Affiche les informations du film        
            with col3:
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.write(f"|**Genre :** *{row['genre_ids']}*")
                st.write("")
                st.write(f"| *Date de Sortie : {row['release_date']}*")
                st.write(f"| *Durée : {row['runtime_min']} minutes*")
                st.write(f"| *Popularité : {row['popularity']}*")
                st.write("")
                st.write(f"| *Note du Public sur 10 : {row['vote_average']}*")
                st.write(f"| *Nombre de votes : {row['vote_count']}*")


    elif selected_top == "Coréen":
        st.subheader("🍿 Nouveautés en Coréen")
        st.write('')
        base_url = 'https://image.tmdb.org/t/p/original'

        # Parcourir les 10 dernières sorties de films Coréen
        for i in (range(min(len(nouveautes_ko), 10))):
            row = nouveautes_ko.iloc[i]
            st.markdown("""
            <style>
                hr {
                    margin: 2rem auto; /* Centrage automatique et espacement */
                    border: 0;
                    border-top: 2px solid #ADD8E6; /* Bleu pâle */
                    width: 90%; /* Réduction de la largeur */
                }
            </style>
            <hr>
            """, unsafe_allow_html=True)#ligne horizontale
        
            # Diviser en colonnes : une pour l'image et une pour le synopsis
            
            empty1, col1, empty2, col2, empty3, col3, empty4 = st.columns([0.6, 1.4, 0.2, 2.5, 0.2, 2, 0.6])# La colonne 2 est deux fois plus large
            
            # Colonne 1 : Affiche du film
            with col1:
                if pd.notna(row['poster_path']):
                    st.write('')
                    st.write('')
                    st.write('')
                    st.write('')
                    st.write('')
                    st.write('')
                    st.write('')
                    st.image(base_url + row['poster_path'], width=500)
            
            # Colonne 2 : Titre et synopsis
            with col2:
                st.markdown(
                f"<h2 style='color:rgb(152, 227, 252); text-align: center;'>{row['title']}</h2>",
                unsafe_allow_html=True
                )
                #st.header(row['title'])  # Afficher le titre du film
                st.write("")
                st.write("")
                if pd.notna(row['overview']):
                    st.write(f"**Synopsis :** *{row['overview']}*")  # Afficher le synopsis
                    st.write("")
                    st.write("")
                st.write(f"**Acteurs :** *{row['actors']}*")
                st.write("")
                st.write(f"**Réalisateurs :** *{row['director']}*")

            # Affiche les informations du film        
            with col3:
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.write(f"|**Genre :** *{row['genre_ids']}*")
                st.write("")
                st.write(f"| *Date de Sortie : {row['release_date']}*")
                st.write(f"| *Durée : {row['runtime_min']} minutes*")
                st.write(f"| *Popularité : {row['popularity']}*")
                st.write("")
                st.write(f"| *Note du Public sur 10 : {row['vote_average']}*")
                st.write(f"| *Nombre de votes : {row['vote_count']}*")



def genre():
    st.markdown(
        "<h1 style='color: #FFD700; text-align: center;'>Explorez par genre</h1>", 
        unsafe_allow_html=True
    )
    st.write('')
    st.write('')

    # Dropdown pour sélectionner un genre
    genres = ['choisir', 'Drame', 'Comédie', 'Romance', 'Thriller', 'Action', 
              'Crime', 'Documentaire', 'Horreur', 'Aventure', 'Mystère', 
              'Fantastique', 'Musique', 'Animation', 'Familial', 'Histoire', 
              'Science-fiction', 'Téléfilm', 'Guerre', 'Western']
    selected_genre = st.selectbox('Sélectionnez un genre', genres, index=0)

    if selected_genre == 'choisir':
        return

    # Filtrer les films par genre sélectionné et garder uniquement ceux avec une affiche valide
    filtered_df = df_genre[
        (df_genre["genre_ids"] == selected_genre) & 
        df_genre['poster_path'].notnull() & 
        df_genre['poster_path'].str.strip().ne('')
    ].sort_values(by="popularity", ascending=False).head(50)

    # Vérifier s'il y a des films à afficher
    if filtered_df.empty:
        st.write(f"Aucun film disponible avec une affiche pour le genre {selected_genre}.")
        return

    # Afficher les films
    base_url = 'https://image.tmdb.org/t/p/original'
    st.subheader(f"🍿 {selected_genre}")
    st.write('')

    # Créer une liste des affiches valides
    posters = filtered_df['poster_path'].tolist()
    titles = filtered_df['title'].tolist()

    # Afficher les posters dans une grille
    cols = st.columns(5)  # Nombre de colonnes
    for index, (poster_path, title) in enumerate(zip(posters, titles)):
        with cols[index % 5]:  # Assigner à une colonne sans espace vide
            st.image(base_url + poster_path, width=200)



def langue():
    st.markdown(
        "<h1 style='color: #FFD700; text-align: center;'>Explorez par langue</h1>", 
        unsafe_allow_html=True
    )
    st.write('')
    st.write('')

    # Dropdown pour sélectionner une langue
    genres = ['choisir', 'Français', 'Anglais', 'Italien', 'Japonais', 'Coréen']
    lang_code_map = {
        'Français': 'fr',
        'Anglais': 'en',
        'Italien': 'it',
        'Japonais': 'ja',
        'Coréen': 'ko'
    }
    selected_langue = st.selectbox('Sélectionnez une langue', genres, index=0)

    if selected_langue == 'choisir':
        return

    # Récupérer le code de la langue
    selected_lang_code = lang_code_map[selected_langue]

    # Filtrer les films par langue sélectionnée et garder uniquement ceux avec une affiche valide
    filtered_df = df[
        (df["original_language"] == selected_lang_code) & 
        df['poster_path'].notnull() & 
        df['poster_path'].str.strip().ne('')
    ].sort_values(by="popularity", ascending=False).head(50)

    # Vérifier s'il y a des films à afficher
    if filtered_df.empty:
        st.write(f"Aucun film disponible avec une affiche pour la langue {selected_langue}.")
        return

    # Afficher les films
    base_url = 'https://image.tmdb.org/t/p/original'
    st.subheader(f"🍿 {selected_langue}")
    st.write('')

    # Créer une liste des affiches valides et des titres
    posters = filtered_df['poster_path'].tolist()
    titles = filtered_df['title'].tolist()

    # Afficher les posters dans une grille
    cols = st.columns(5)  # Nombre de colonnes
    for index, (poster_path, title) in enumerate(zip(posters, titles)):
        with cols[index % 5]:  # Assigner à une colonne sans espace vide
            st.image(base_url + poster_path, width=200)



def projet():
    st.markdown(
        "<h1 style='color: #FFFFFF; text-align: center;'>Notre projet</h1>", 
        unsafe_allow_html=True
    )
    st.write('')

        # Afficher l'image avec alignement centré
    col1, col2 = st.columns([3, 5])  # Colonnes pour aligner au centre
    with col1:
        st.image("ordi_logo.png", width=400)
    with col2 : 
        st.write('')
        st.write('')
        st.write("Bienvenue sur Wildflix – Votre plateforme ultime pour découvrir des films exceptionnels !")
        st.write("Chez Wildflix, nous transformons votre expérience cinématographique grâce à un service de recommandation intelligent et intuitif. Explorez un catalogue riche et varié comprenant des milliers de films soigneusement sélectionnés pour satisfaire toutes vos envies et vos curiosités.")
    st.write("Pourquoi choisir Wildflix ?")
    st.write('')
    st.write("🔍 Recommandations personnalisées : Grâce à notre technologie avancée, Wildflix analyse vos préférences et vous propose des films que vous êtes presque sûr d’aimer. Nos algorithmes prennent en compte de nombreux critères, tels que la popularité des films, le casting, la date de sortie, le genre, et bien plus encore.")
    st.write('')
    st.write("🔥 Top du moment et nouveautés : Restez à la pointe des tendances avec notre onglet 'Top du moment', constamment mis à jour, et découvrez les derniers films fraîchement ajoutés dans la section 'Nouveautés'.")
    st.write('')
    st.write("🎭 Filtres intuitifs : Vous cherchez un film d'un genre spécifique ou dans une langue particulière ? Nos filtres ergonomiques vous permettent de naviguer facilement dans notre vaste catalogue.")
    st.write('')
    st.write("🌟 Une expérience sur-mesure : Chez Wildflix, tout est conçu pour vous offrir une interface fluide et agréable, où chaque clic vous rapproche de votre prochaine découverte cinématographique.")
    st.write('')
    st.write("Wildflix : Une plateforme data-driven au service du 7ᵉ art")
    st.write("Nous mettons la puissance des données au service de votre passion pour le cinéma. Grâce à des algorithmes intelligents et des mises à jour régulières, nous sommes déterminés à vous offrir une expérience qui évolue et s’adapte à vos goûts.")
    st.write("Plongez dans l'univers du cinéma avec Wildflix et laissez-vous surprendre par des recommandations qui vous ressemblent.")
    st.write('')
    st.write("👉 Rejoignez-nous dès aujourd'hui et découvrez votre prochain film coup de cœur !")
    st.markdown("""
        <style>
            hr {
                margin: 2rem auto; /* Centrage automatique et espacement */
                border: 0;
                border-top: 2px solid #ADD8E6; /* Bleu pâle */
                width: 90%; /* Réduction de la largeur */
            }
        </style>
        <hr>
        """, unsafe_allow_html=True)#ligne horizontale