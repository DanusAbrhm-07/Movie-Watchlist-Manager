import json
import os

FILE_NAME = "movies.json"

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

def main():
    movies = load_movies()
    while True:
        print("\n--- Movie Watchlist Manager ---")
        print("1. Add a movie\n2. View all movies\n3. Search for a movie")
        print("4. Mark movie as watched\n5. Remove a movie\n6. Display watched/unwatched\n7. Exit")
        
        choice = input("Choose an option: ").strip()
        
        if choice == '7':
            print("Goodbye!")
            break
        else:
            print("Feature under development.")

if __name__ == "__main__":
    main()