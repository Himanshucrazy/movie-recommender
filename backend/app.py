from flask import Flask, request, jsonify
from flask_cors import CORS
from model import recommend

app = Flask(__name__)
CORS(app)   # allow frontend to connect

@app.route('/')
def home():
    return "Movie Recommender API Running"

@app.route('/recommend', methods=['POST'])
def recommend_movies():
    data = request.get_json()
    movie = data.get('movie')

    result = recommend(movie)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)