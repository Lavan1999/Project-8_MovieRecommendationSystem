import pickle
import streamlit as st 
import requests 

st.set_page_config(layout="wide")
# Center the title with blue color
st.markdown(
    "<h1 style='text-align: center; color: pink;'>Movie Recommendation System</h1>",
    unsafe_allow_html=True
)
# Load the movies data from the pickle file
movies = pickle.load(open('movies.pkl','rb'))
# Extract the titles
titles = movies['title'].values
# Convert to a set to get unique values and then sort the list
movies_list = set(titles)
col1, col2 ,col3= st.columns([0.4,0.5,0.1])

with col1:
    st.header(" :blue[Select Movie]")
    selected_movie = st.selectbox('', movies_list)

similarity = pickle.load(open('similarity.pkl','rb'))

def fetch_poster(movie_id):
    response = requests.get("https://api.themoviedb.org/3/movie/{}?api_key=ec2bac11f1fbc157f3df0aedb6445b66&language=en-US".format(movie_id))
    data = response.json()
    print(data)
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


import streamlit.components.v1 as components
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse = True, key=lambda x : x[1])[1:6]

    recommended_movies = []
    recommended_poster = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch poster fromcAPI
        recommended_poster.append(fetch_poster(movie_id))
        
    return recommended_movies, recommended_poster

  
if st.button('Show Recommended Movies'):
    movie_name, movie_poster = recommend(selected_movie)
    
    # Create a new row of five equally spaced columns for the movie recommendations
    cols = st.columns(5)
    for i, col in enumerate(cols):
        with col:
            st.text(movie_name[i])
            st.image(movie_poster[i])