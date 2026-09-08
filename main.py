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
    """Loads the main webpage and passes the movie list to the HTML."""
    movies = load_movies()
    return render_template('index.html', movies=movies)

@app.route('/add', methods=['POST'])
def add_movie():
    """Receives the form submission from HTML and saves the new movie."""
    title = request.form.get('title').strip()
    watched_status = request.form.get('watched')
    
    if title:
        movies = load_movies()
        movies.append({"title": title, "watched": watched_status})
        save_movies(movies)
        
    # Refresh the page to show the updated list
    return redirect(url_for('index'))

if __name__ == "__main__":
    # Runs the local web server
    app.run(debug=True)