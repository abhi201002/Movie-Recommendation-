import pickle
import streamlit as st
import requests
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?language=en-US".format(movie_id)
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI4MzE4MDA0ZTI0OGY2MjAwMzdjYTFjZDZiMDAxODgzMSIsIm5iZiI6MTcyMzk2ODY0MC42NTM2OTUsInN1YiI6IjY2YzE4MjQ2YTA2MjA3NTJhMTkyMzMyZiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.tL59EZTuL1kq4BoyhxRR8j0PvKEAvrB27SDYAvSpfv0"
    }
    data = requests.get(url, headers=headers)
    data = data.json()
    path = data['poster_path']
    st.text(path)
    # poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + path
    # full_path = ""
    return full_path

movies = pickle.load(open('./movies.pkl','rb'))
final_vector = pickle.load(open('./TMDB_BOW.pkl','rb'))
final_vector_bow = pickle.load(open('./TMDB_BOW_vector.pkl','rb'))
final_vector_bow_title = pickle.load(open('./TMDB_BOW_vector_title.pkl','rb'))
final_vector_title = pickle.load(open('./TMDB_BOW_title.pkl','rb'))

def recommend(sent):
    sent = sent.lower()
    sent = [sent]
    query = final_vector.transform(sent).toarray()
    query_ = final_vector_title.transform(sent).toarray()
    # query = np.expand_dims(query, axis = 0)

    dic = {i:cosine_similarity(query, np.expand_dims(vec, axis = 0))[0][0] for i, vec in enumerate(final_vector_bow) }
    dic_ = {i:cosine_similarity(query_, np.expand_dims(vec, axis = 0))[0][0] for i, vec in enumerate(final_vector_bow_title) }
    # dic = {**dic, **dic_}
    distances = sorted(dic.items(), reverse = True, key = lambda x:x[1])
    distances_ = sorted(dic_.items(), reverse = True, key = lambda x:x[1])

    movie_ind = []

    for item in distances_:
        if item[1] == 0.0:
            continue
        movie_ind.append(item[0])
        
    for item in distances:
        if item[0] not in movie_ind:
            movie_ind.append(item[0]) 

    recommended_movie_posters = []
    recommended_movie_names = []

    for item in movie_ind[0:5]:
        movie_name = movies['title'][item]
        movie_id =  movies['id'][item]
        recommended_movie_posters.append(fetch_poster(int(movie_id)))
        recommended_movie_names.append(movie_name)

    return recommended_movie_names,recommended_movie_posters

st.header('Movie Recommender Syste')

movie_list = movies['title'].values
selected_movie = st.text_input(
    "Type your movie",
)

if st.button('Show Recommendation'):
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])





