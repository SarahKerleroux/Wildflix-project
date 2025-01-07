import pandas as pd
import streamlit as st
import base64
import html

@st.cache_data
def load_data():
    df = pd.read_csv("last_df_bon.csv")
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
    return df, df_genre, fr, en, it, ja, ko, nouveautes_fr, nouveautes_en, nouveautes_it, nouveautes_ja, nouveautes_ko

df, df_genre, fr, en, it, ja, ko, nouveautes_fr, nouveautes_en, nouveautes_it, nouveautes_ja, nouveautes_ko = load_data()

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
    
    df_movies = pd.read_csv("last_df_bon.csv").reset_index()
    df_recommendations = pd.read_csv("df_20_000_recomandation.csv")
    add_background("fond.png")
    base_url = 'https://image.tmdb.org/t/p/original'


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
            border: 1px solid #007BFF;
        }
        </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns([1.2, 1.2, 2.6, 0.8, 0.7])  # Colonnes pour aligner au centre


    with col3:
        st.image("logo.png", width=350)
    st.markdown(
        f"<h1 style='color:#FFFFFF; text-align: center;'>Bienvenue sur notre Système de Recommandation</h1>",
        unsafe_allow_html=True
    )


    st.write("")


    # titles = [df_recommendations].sort_values(by="popularity", ascending=False)["title"].dropna().unique()
    titles = df_movies['title']
    if 'index_movie' not in st.session_state:
        st.session_state['index_movie'] = None
    # Barre de recherche
    col_empty1, col_search, col_empty2 = st.columns([1, 4, 1])
    print('xxx')
    print(st.session_state["index_movie"])
    with col_search:
        search_query = st.selectbox("Sélectionnez ou écrivez un titre de film :", options= list(titles), index = st.session_state["index_movie"])
        st.write('')
        st.write('')
    empty1, col1,empty2, col2,empty3,col3,empty4 = st.columns([0.1,3,0.1,5,0.1,2,0.1])
    
    
    if search_query:
        # Film sélectionné
        selected_movie = df_movies[df_movies['title'] == search_query].iloc[0]
        
        
        with col1:
            st.write('---')
            if pd.notna(selected_movie['poster_path']):
                st.image(base_url + selected_movie['poster_path'], width=350)


        with col2 :
            st.markdown(f"<h1 style='color:#FFFFFF; text-align: center;'>🎬 Film: {selected_movie['title']}</h1>", unsafe_allow_html=True)
            st.markdown(f"<h5 style='color:#FFFFFF; text-align: center;'>Sortie le {selected_movie['release_date']}</h5>", unsafe_allow_html=True)
            st.write('')
            st.markdown(
    f"""
    <style>
    .custom-synopsis {{
        background-color: rgba(0, 0, 0, 0.80); /* Fond noir avec 80% d'opacité */
        padding: 10px;
        border-radius: 10px; /* Bords arrondis */
        color: white; /* Texte blanc */
        text-align: left;
        box-shadow: 0 0 15px rgba(0, 123, 255, 0.8); /* Éclairage bleu stylisé */
        border: 2px solid rgba(0, 123, 255, 0.8); /* Bord bleu lumineux */
    }}
    .custom-synopsis h5 {{
        font-size: 24px; /* Taille du titre "Synopsis" */
        font-weight: bold; /* Mettre en gras */
        margin-bottom: 0; /* Pas d'espacement avec le texte */
        margin-top: 0; /* Pas d'espacement supérieur */
    }}
    .custom-synopsis em {{
        font-size: 16px; /* Taille du texte du synopsis */
    }}
    </style>
    <div class="custom-synopsis">
        <h5>Synopsis :</h5>
        <em>{selected_movie['overview']}</em>
    </div>
    """,
    unsafe_allow_html=True
)
            
            st.write('')
            
            st.markdown(f"""
    <style>
    .custom-info {{
        background-color: rgba(0, 0, 0, 0.80); /* Fond noir avec 80% d'opacité */
        padding: 10px;
        border-radius: 10px; /* Bords arrondis */
        color: white; /* Texte blanc */
        text-align: left;
        box-shadow: 0 0 15px rgba(0, 123, 255, 0.8); /* Éclairage bleu stylisé */
        border: 2px solid rgba(0, 123, 255, 0.8); /* Bord bleu lumineux */
        margin-bottom: 20px; /* Espacement entre les sections */
    }}
    .custom-info h5 {{
        font-size: 24px; /* Taille du titre */
        font-weight: bold; /* Titre en gras */
        margin-bottom: 0; /* Pas d'espacement sous le titre */
        margin-top: 0; /* Pas d'espacement au-dessus */
    }}
    .custom-info em {{
        font-size: 16px; /* Taille du texte */
    }}
    /* Supprime les crochets et les guillemets */
    .custom-info em::before {{
        content: ""; /* Supprime les crochets ouverts */
    }}
    .custom-info em::after {{
        content: ""; /* Supprime les crochets fermés */
    }}
    .custom-info em {{
        display: inline-block;
        white-space: pre-wrap;
    }}
    </style>
    <div class="custom-info">
        <h5>Acteurs :</h5>
        <em>{str(selected_movie['actors']).strip("[]").replace("'", "").replace(",", ", ")}</em>
    </div>
    <div class="custom-info">
        <h5>Réalisateur :</h5>
        <em>{selected_movie['director']}</em>
    </div>  
    """, unsafe_allow_html=True)
        with col3:        
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write(f"|**Genre :** *{selected_movie['genre_ids']}*")
            st.write(f"|**Durée :** *{selected_movie['runtime_min']} minutes*")
            st.write(f"|**Popularité :** *{selected_movie['popularity']}*")
            st.write(f"|**Note du Public sur 10 :** *{selected_movie['vote_average']}*")
            st.write(f"|**Nombre de votes :** *{selected_movie['vote_count']}*")



        # Recommandations
        recommendations = df_recommendations[df_recommendations['title'] == search_query].iloc[0]
        recommended_titles = []
        for col in recommendations.index:
            if "Recommendation" in col and pd.notna(recommendations[col]):
                recommended_titles.append(recommendations[col])

        # Obtenir les détails des films recommandés
        recommended_movies = df_movies[df_movies['title'].isin(recommended_titles)]
        print(recommended_movies['title'])

        # Affiche les recommandations
        st.markdown("<h1 style='color:#FFFFFF; text-align: center;'> 🍿 Films recommandés :</h1>", unsafe_allow_html=True)
        st.markdown(
    """
    <style>
    div.stButton > button {
        background-color: rgba(0, 0, 0, 0.80); /* Fond noir avec 80% d'opacité */
        color: white; /* Texte blanc */
        border: 2px solid rgba(0, 123, 255, 0.8); /* Bord bleu lumineux */
        box-shadow: 0 0 15px rgba(0, 123, 255, 0.8); /* Éclairage bleu stylisé */
        font-size: 16px; /* Taille du texte */
        padding: 10px 20px; /* Espacement interne */
        border-radius: 5px; /* Coins arrondis */
        cursor: pointer; /* Curseur pointeur */
        margin: 0 auto; /* Centrer horizontalement */
        display: block; /* Occuper tout l'espace disponible */
    }

    /* Survol */
    div.stButton > button:hover {
        box-shadow: 0 0 20px rgba(0, 123, 255, 1); /* Éclairage bleu plus intense au survol */
        background: rgba(0, 123, 255, 0.5); /* Fond bleu clair */
        color: white; /* Texte blanc */
        border: 2px solid rgba(0, 123, 255, 0.8); /* Bord bleu lumineux */
    }

    /* État actif (clic) */
    div.stButton > button:active {
        box-shadow: inset 0 0 10px rgba(0, 123, 255, 0.8); /* Éclairage intérieur bleu */
        background: rgba(0, 123, 255, 0.8); /* Fond bleu foncé */
        color: white; /* Texte blanc */
        border: 2px solid rgba(0, 123, 255, 1); /* Bord bleu intense */
    }

    /* État focus (après clic ou navigation clavier) */
    div.stButton > button:focus {
        outline: none !important; /* Supprime le contour rouge par défaut */
        box-shadow: 0 0 10px rgba(0, 123, 255, 0.8); /* Éclairage bleu */
        border: 2px solid rgba(0, 123, 255, 1) !important; /* Bord bleu intense */
        background: rgba(0, 123, 255, 0.8); /* Fond bleu */
        color: white !important; /* Texte blanc */
    }

    /* Suppression des bordures internes sur Firefox */
    div.stButton > button::-moz-focus-inner {
        border: 0; /* Supprime les bordures internes par défaut sur Firefox */
    }
    </style>
    """,
    unsafe_allow_html=True
)
        cols = st.columns(5)  
        for idx, (col, (i, movie)) in enumerate(zip(cols, recommended_movies.iterrows())):
            with col:
                st.image(base_url + movie['poster_path'])
                st.button(f"Voir {movie['title']}", key=f"recommendation_{idx}", on_click= clik_film, args=[int(recommended_movies.iloc[[idx]].index[0])])
                    
def clik_film(index_movie):
    print(index_movie)
    st.session_state["index_movie"] = index_movie
          

def match():
    # Charger les datasets
    df_movies = pd.read_csv("last_df_bon.csv").reset_index()
    df_recommendations = pd.read_csv("df_20_000_recomandation.csv")
    base_url = 'https://image.tmdb.org/t/p/original'

    st.markdown(
        f"<h1 style='color:#FFD700; text-align: center;'>En duo trouvez votre match !</h1>",
        unsafe_allow_html=True
    )
    st.write('')
    st.write('')

    # Styles personnalisés pour les selectbox et boutons
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
            border: 1px solid #007BFF;
        }
        div.stButton > button {
            background-color: rgba(0, 0, 0, 0.80);
            color: white;
            border: 2px solid rgba(0, 123, 255, 0.8);
            box-shadow: 0 0 15px rgba(0, 123, 255, 0.8);
            font-size: 16px;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            margin: 0 auto;
            display: block;
        }
        div.stButton > button:hover {
            box-shadow: 0 0 20px rgba(0, 123, 255, 1);
            background: rgba(0, 123, 255, 0.5);
            color: white;
            border: 2px solid rgba(0, 123, 255, 0.8);
        }
        div.stButton > button:active {
            box-shadow: inset 0 0 10px rgba(0, 123, 255, 0.8);
            background: rgba(0, 123, 255, 0.8);
            color: white;
            border: 2px solid rgba(0, 123, 255, 1);
        }
        </style>
    """, unsafe_allow_html=True)

    # Sélection des deux films
    titles = df_movies['title'].unique()
    col1, col2 = st.columns(2)

    st.write('')
    st.write('')
    
    with col1:
        selected_movie_1 = st.selectbox("Sélectionnez le premier film :", options=titles, key="movie_1")
    with col2:
        selected_movie_2 = st.selectbox("Sélectionnez le second film :", options=titles, key="movie_2")

    if selected_movie_1 and selected_movie_2:
        # Obtenir les recommandations pour chaque film
        recommendations_1 = df_recommendations[df_recommendations['title'] == selected_movie_1].iloc[0]
        recommendations_2 = df_recommendations[df_recommendations['title'] == selected_movie_2].iloc[0]

        # Extraire les titres recommandés
        recommended_titles_1 = [
            recommendations_1[col] for col in recommendations_1.index if "Recommendation" in col and pd.notna(recommendations_1[col])
        ]
        recommended_titles_2 = [
            recommendations_2[col] for col in recommendations_2.index if "Recommendation" in col and pd.notna(recommendations_2[col])
        ]

        # Trouver les films communs ou proches
        common_recommendations = set(recommended_titles_1).intersection(recommended_titles_2)
        all_recommendations = list(common_recommendations)

        if len(all_recommendations) < 5:
            # Ajouter des recommandations uniques si nécessaire
            unique_recommendations = set(recommended_titles_1).union(recommended_titles_2)
            all_recommendations += list(unique_recommendations - common_recommendations)[:5 - len(all_recommendations)]

        # Obtenir les détails des films recommandés
        recommended_movies = df_movies[df_movies['title'].isin(all_recommendations)]

        # Affiche les recommandations
        st.markdown("<h1 style='color:#FFFFFF; text-align: center;'> 🍿 Films recommandés :</h1>", unsafe_allow_html=True)
        st.markdown(
    """
    <style>
    div.stButton > button {
        background-color: rgba(0, 0, 0, 0.80); /* Fond noir avec 80% d'opacité */
        color: white; /* Texte blanc */
        border: 2px solid rgba(0, 123, 255, 0.8); /* Bord bleu lumineux */
        box-shadow: 0 0 15px rgba(0, 123, 255, 0.8); /* Éclairage bleu stylisé */
        font-size: 16px; /* Taille du texte */
        padding: 10px 20px; /* Espacement interne */
        border-radius: 5px; /* Coins arrondis */
        cursor: pointer; /* Curseur pointeur */
        margin: 0 auto; /* Centrer horizontalement */
        display: block; /* Occuper tout l'espace disponible */
    }

    /* Survol */
    div.stButton > button:hover {
        box-shadow: 0 0 20px rgba(0, 123, 255, 1); /* Éclairage bleu plus intense au survol */
        background: rgba(0, 123, 255, 0.5); /* Fond bleu clair */
        color: white; /* Texte blanc */
        border: 2px solid rgba(0, 123, 255, 0.8); /* Bord bleu lumineux */
    }

    /* État actif (clic) */
    div.stButton > button:active {
        box-shadow: inset 0 0 10px rgba(0, 123, 255, 0.8); /* Éclairage intérieur bleu */
        background: rgba(0, 123, 255, 0.8); /* Fond bleu foncé */
        color: white; /* Texte blanc */
        border: 2px solid rgba(0, 123, 255, 1); /* Bord bleu intense */
    }

    /* État focus (après clic ou navigation clavier) */
    div.stButton > button:focus {
        outline: none !important; /* Supprime le contour rouge par défaut */
        box-shadow: 0 0 10px rgba(0, 123, 255, 0.8); /* Éclairage bleu */
        border: 2px solid rgba(0, 123, 255, 1) !important; /* Bord bleu intense */
        background: rgba(0, 123, 255, 0.8); /* Fond bleu */
        color: white !important; /* Texte blanc */
    }

    /* Suppression des bordures internes sur Firefox */
    div.stButton > button::-moz-focus-inner {
        border: 0; /* Supprime les bordures internes par défaut sur Firefox */
    }
    </style>
    """,
    unsafe_allow_html=True
)

        cols = st.columns(5)
        for idx, (col, (_, movie)) in enumerate(zip(cols, recommended_movies.iterrows())):
            with col:
                st.image(base_url + movie['poster_path'], use_container_width=True)  # Utilisation de use_container_width
                st.button(
                    f"Voir {movie['title']}",
                    key=f"recommendation_{idx}",
                    on_click=clik_film,
                    args=[int(movie['index'])]
                )



def top():
    st.markdown(
        "<h1 style='color: #FFD700; text-align: center;'>Découvrez le Top 10</h1>", 
        unsafe_allow_html=True
    )
    st.write('')
    st.write('')
    st.markdown(
    """
    <style>
    /* Style par défaut pour le selectbox */
    div[data-baseweb="select"] {
        border-radius: 5px; /* Coins arrondis */
    }
    
    /* Survol du selectbox */
    div[data-baseweb="select"]:hover {
        border: 1px solid #0056b3; /* Bordure bleue plus foncée au survol */
    }

    /* État actif ou sélectionné */
    div[data-baseweb="select"] > div {
        border-color: #007BFF !important; /* Bordure bleue après sélection */
        background-color: rgba(0, 123, 255, 0.1); /* Fond bleu clair */
    }

    /* Texte sélectionné */
    div[data-baseweb="select"] span {
        color: black; /* Couleur du texte noir (ou ajuster selon le design) */
    }
    </style>
    """,
    unsafe_allow_html=True
)
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
    st.markdown(
    """
    <style>
    /* Style par défaut pour le selectbox */
    div[data-baseweb="select"] {
        border-radius: 5px; /* Coins arrondis */
    }
    
    /* Survol du selectbox */
    div[data-baseweb="select"]:hover {
        border: 1px solid #0056b3; /* Bordure bleue plus foncée au survol */
    }

    /* État actif ou sélectionné */
    div[data-baseweb="select"] > div {
        border-color: #007BFF !important; /* Bordure bleue après sélection */
        background-color: rgba(0, 123, 255, 0.1); /* Fond bleu clair */
    }

    /* Texte sélectionné */
    div[data-baseweb="select"] span {
        color: black; /* Couleur du texte noir (ou ajuster selon le design) */
    }
    </style>
    """,
    unsafe_allow_html=True
)
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
    st.markdown(
    """
    <style>
    /* Style par défaut pour le selectbox */
    div[data-baseweb="select"] {
        border-radius: 5px; /* Coins arrondis */
    }
    
    /* Survol du selectbox */
    div[data-baseweb="select"]:hover {
        border: 1px solid #0056b3; /* Bordure bleue plus foncée au survol */
    }

    /* État actif ou sélectionné */
    div[data-baseweb="select"] > div {
        border-color: #007BFF !important; /* Bordure bleue après sélection */
        background-color: rgba(0, 123, 255, 0.1); /* Fond bleu clair */
    }

    /* Texte sélectionné */
    div[data-baseweb="select"] span {
        color: black; /* Couleur du texte noir (ou ajuster selon le design) */
    }
    </style>
    """,
    unsafe_allow_html=True
)

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
    st.markdown(
    """
    <style>
    /* Style par défaut pour le selectbox */
    div[data-baseweb="select"] {
        border-radius: 5px; /* Coins arrondis */
    }
    
    /* Survol du selectbox */
    div[data-baseweb="select"]:hover {
        border: 1px solid #0056b3; /* Bordure bleue plus foncée au survol */
    }

    /* État actif ou sélectionné */
    div[data-baseweb="select"] > div {
        border-color: #007BFF !important; /* Bordure bleue après sélection */
        background-color: rgba(0, 123, 255, 0.1); /* Fond bleu clair */
    }

    /* Texte sélectionné */
    div[data-baseweb="select"] span {
        color: black; /* Couleur du texte noir (ou ajuster selon le design) */
    }
    </style>
    """,
    unsafe_allow_html=True
)

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
    col1, col2, col3, col4 = st.columns([0.5, 2.4, 5, 0.5])  # Colonnes pour aligner au centre
    st.markdown(
    """
    <style>
    .highlighted-text {
        font-size: 24px; /* Taille du texte */
        font-weight: bold; /* Texte en gras */
    }
    </style>
    """,
    unsafe_allow_html=True,
    )
    with col2:
        st.image("logo_ordi.png", width=350)

    with col3:
        st.write('')
        st.write('')
        st.markdown('<p class="highlighted-text">La plateforme ultime pour découvrir des films exceptionnels !</p>', unsafe_allow_html=True)
        st.write("Chez Wildflix, nous transformons votre expérience cinématographique grâce à un service de recommandation intelligent et intuitif. Explorez un catalogue riche et varié comprenant des milliers de films soigneusement sélectionnés pour satisfaire toutes vos envies et vos curiosités.")
    
    col1, col2, col3 = st.columns([0.6, 8, 0.6])
    with col2:
        st.markdown(
            """
            <style>
            .title {
                font-size: 24px; /* Taille du texte */
                font-weight: bold; /* Texte en gras */
            }
            </style>
            """,
            unsafe_allow_html=True,
        )
        
        st.markdown('<p class="title">Pourquoi choisir Wildflix ?</p>', unsafe_allow_html=True)
        st.write('')
        st.write("🔍 Recommandations personnalisées : Grâce à notre technologie avancée, Wildflix analyse vos préférences et vous propose des films que vous êtes presque sûr d’aimer. Nos algorithmes prennent en compte de nombreux critères, tels que la popularité des films, le casting, la date de sortie, le genre, et bien plus encore.")
        st.write('')
        st.write("🔥 Top du moment et nouveautés : Restez à la pointe des tendances avec notre onglet 'Top du moment', constamment mis à jour, et découvrez les derniers films fraîchement ajoutés dans la section 'Nouveautés'.")
        st.write('')
        st.write("🎭 Filtres intuitifs : Vous cherchez un film d'un genre spécifique ou dans une langue particulière ? Nos filtres ergonomiques vous permettent de naviguer facilement dans notre vaste catalogue.")
        st.write('')
        st.write("🌟 Une expérience sur-mesure : Chez Wildflix, tout est conçu pour vous offrir une interface fluide et agréable, où chaque clic vous rapproche de votre prochaine découverte cinématographique.")
        st.write('')
        st.markdown('<p class="title">Wildflix : Une plateforme data-driven au service du 7ᵉ art</p>', unsafe_allow_html=True)
        st.write("Nous mettons la puissance des données au service de votre passion pour le cinéma. Grâce à des algorithmes intelligents et des mises à jour régulières, nous sommes déterminés à vous offrir une expérience qui évolue et s’adapte à vos goûts.")
        st.write("Plongez dans l'univers du cinéma avec Wildflix et laissez-vous surprendre par des recommandations qui vous ressemblent.")
        st.write('')
        st.markdown(
        """
        <style>
        .centered-text {
            text-align: center; /* Centre le texte */
        }
        </style>
        """,
        unsafe_allow_html=True,
        )
        st.markdown('<p class="centered-text">👉 Rejoignez-nous dès aujourd\'hui et découvrez votre prochain film coup de cœur !</p>', unsafe_allow_html=True)
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