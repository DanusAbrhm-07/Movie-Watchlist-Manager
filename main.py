from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)
FILE_NAME = "movies.json"

# --- Core Data Functions ---
def load_movies():
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, 'r') as file:
                return json.load(file)
        except (json.JSONDecodeError, IOError):
            return []
    return []

def save_movies(movies):
    try:
        with open(FILE_NAME, 'w') as file:
            json.dump(movies, file, indent=4)
    except IOError:
        print("Error: Could not save to disk.")

# --- Web Routes ---
@app.route('/')
def index():
    """Loads the main webpage and handles search and filter."""
    movies = load_movies()
    
    # Grab search and filter parameters from the web address (URL) if they exist
    search_query = request.args.get('search', '').strip().lower()
    filter_status = request.args.get('filter', 'All')
    
    # Create a list of movies that match the search and filter criteria
    filtered_movies = []
    for idx, movie in enumerate(movies):
        if search_query and search_query not in movie['title'].lower():
            continue
        if filter_status != 'All' and movie['watched'] != filter_status:
            continue
            
        # We attach the index ('id') so the HTML knows exactly which movie to delete or update
        filtered_movies.append({'id': idx, **movie})

    return render_template('index.html', movies=filtered_movies, search_query=search_query, filter_status=filter_status)

@app.route('/add', methods=['POST'])
def add_movie():
    """Receives the form submission to add a movie."""
    title = request.form.get('title').strip()
    watched_status = request.form.get('watched')
    
    if title:
        movies = load_movies()
        movies.append({"title": title, "watched": watched_status})
        save_movies(movies)
        
    return redirect(url_for('index'))

@app.route('/delete/<int:movie_id>', methods=['POST'])
def delete_movie(movie_id):
    """Deletes a movie based on its position in the list."""
    movies = load_movies()
    if 0 <= movie_id < len(movies):
        movies.pop(movie_id)
        save_movies(movies)
    return redirect(url_for('index'))

@app.route('/toggle/<int:movie_id>', methods=['POST'])
def toggle_movie(movie_id):
    """Switches the watched status between Yes and No."""
    movies = load_movies()
    if 0 <= movie_id < len(movies):
        current_status = movies[movie_id]["watched"]
        movies[movie_id]["watched"] = "No" if current_status == "Yes" else "Yes"
        save_movies(movies)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)