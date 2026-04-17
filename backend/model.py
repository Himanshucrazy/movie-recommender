import pandas as pd
import requests
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# 🔑 Add your TMDB API key here
API_KEY = "YOUR_API_KEY_HERE"

# Load dataset
movies = pd.read_csv('movies.csv')

# Keep required columns
movies = movies[['id', 'title', 'overview']]
movies.dropna(inplace=True)

# Convert text to vectors
cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(movies['overview']).toarray()

# Similarity matrix
similarity = cosine_similarity(vectors)


# 🎬 Fetch real poster from TMDB
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"
        data = requests.get(url).json()

        if 'poster_path' in data and data['poster_path']:
            return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
        else:
            return "https://dummyimage.com/200x300/000/fff&text=No+Image"
    except:
        return "https://dummyimage.com/200x300/000/fff&text=Error"


# 🎯 Recommendation function (with default fallback)
def recommend(movie):
    movie = movie.lower()

    # Check if movie exists
    if movie in movies['title'].str.lower().values:
        index = movies[movies['title'].str.lower() == movie].index[0]
    else:
        # Default fallback (first movie)
        index = 0

    distances = similarity[index]

    movies_list = sorted(list(enumerate(distances)),
                         reverse=True,
                         key=lambda x: x[1])[1:6]

    result = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].id
        title = movies.iloc[i[0]].title

        result.append({
            "title": title,
            "poster": fetch_poster(movie_id)
        })

    return result