import streamlit as st
import pickle
import pandas as pd
import requests

st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")

# Tumhari TMDB API key
API_KEY = "472aa3303ee3f71d079f6f09c9a20910"

def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
        response = requests.get(url, timeout=5)
        data = response.json()
        if 'poster_path' in data and data['poster_path']:
            return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
        else:
            return "https://via.placeholder.com/200x300?text=No+Poster"
    except:
        return "https://via.placeholder.com/200x300?text=No+Internet"


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])

    names = []
    posters = []

    for i in movies_list[1:6]:   # top 5 recommendations
        movie_id = movies.iloc[i[0]]['id']   # tumhara column: id
        names.append(movies.iloc[i[0]]['title'])
        posters.append(fetch_poster(movie_id))

    return names, posters

# Load files
movies_dict = pickle.load(open(r"C:\Users\shwet\movie_dict.pkl", "rb"))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open(r"C:\Users\shwet\similarity.pkl", "rb"))

# UI
st.markdown("<h1 style='text-align:center;'>🎬 Movie Recommender System</h1>", unsafe_allow_html=True)


option = st.selectbox("Select a movie", movies['title'].values)

if st.button("Recommend"):
    names, posters = recommend(option)
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.image(posters[i])
            st.markdown(f"<p style='text-align:center'>{names[i]}</p>", unsafe_allow_html=True)
