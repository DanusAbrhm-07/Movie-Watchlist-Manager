from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DB_NAME = "movies.db"

# --- Database Setup ---
def init_db():
    """Creates the database and table if they don't exist."""
    conn = sqlite3.connect(DB_NAME)
    # Added COLLATE NOCASE to prevent case-sensitive duplicates (e.g., "batman" vs "Batman")
    conn.execute('''
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL UNIQUE COLLATE NOCASE,
            watched TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def get_db_connection():
    """Opens a database connection."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row # Allows us to treat rows like dictionaries for the HTML
    return conn

# --- Web Routes ---
@app.route('/')
def index():
    """Loads the main webpage and handles search and filter via SQL."""
    search_query = request.args.get('search', '').strip().lower()
    filter_status = request.args.get('filter', 'All')
    
    conn = get_db_connection()
    
    # Base query
    query = "SELECT * FROM movies WHERE 1=1"
    params = []
    
    # Dynamically append SQL conditions based on user input
    if search_query:
        query += " AND LOWER(title) LIKE ?"
        params.append(f"%{search_query}%")
        
    if filter_status != 'All':
        query += " AND watched = ?"
        params.append(filter_status)
        
    # Fetch results and convert to standard dictionaries for Jinja HTML rendering
    rows = conn.execute(query, params).fetchall()
    filtered_movies = [dict(row) for row in rows]
    
    conn.close()
    return render_template('index.html', movies=filtered_movies, search_query=search_query, filter_status=filter_status)

@app.route('/add', methods=['POST'])
def add_movie():
    """Inserts a new movie into the database."""
    title = request.form.get('title', '').strip()
    watched_status = request.form.get('watched', 'No')
    
    if title:
        conn = get_db_connection()
        try:
            conn.execute("INSERT INTO movies (title, watched) VALUES (?, ?)", (title, watched_status))
            conn.commit()
        except sqlite3.IntegrityError:
            # This triggers automatically if the title already exists (due to the UNIQUE constraint)
            pass 
        conn.close()
        
    return redirect(url_for('index'))

@app.route('/delete/<int:movie_id>', methods=['POST'])
def delete_movie(movie_id):
    """Deletes a movie by its unique database ID."""
    conn = get_db_connection()
    conn.execute("DELETE FROM movies WHERE id = ?", (movie_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/toggle/<int:movie_id>', methods=['POST'])
def toggle_movie(movie_id):
    """Updates the watched status in the database."""
    conn = get_db_connection()
    movie = conn.execute("SELECT watched FROM movies WHERE id = ?", (movie_id,)).fetchone()
    
    if movie:
        new_status = "No" if movie["watched"] == "Yes" else "Yes"
        conn.execute("UPDATE movies SET watched = ? WHERE id = ?", (new_status, movie_id))
        conn.commit()
        
    conn.close()
    return redirect(url_for('index'))

if __name__ == "__main__":
    init_db() # Ensure the database and tables are created before the server starts
    app.run(debug=True, use_reloader=False)