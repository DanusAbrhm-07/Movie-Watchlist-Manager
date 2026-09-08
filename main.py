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

def add_movie(movies):
    title = input("Enter movie title: ").strip()
    if not title:
        print("Error: Title cannot be empty.")
        return
        
    while True:
        watched_input = input("Have you already watched this? (y/n): ").strip().lower()
        if watched_input in ['y', 'yes', 'true', 't']:
            is_watched = "Yes"
            break
        elif watched_input in ['n', 'no', 'false', 'f']:
            is_watched = "No"
            break
        else:
            print("Invalid input. Enter 'y' or 'n'.")
            
    movies.append({"Title": title, "Watched": is_watched})
    save_movies(movies)
    print(f"'{title}' added successfully!")

def view_movies(movies):
    if not movies:
        print("Your watchlist is empty.")
        return
    print("\n--- All Movies ---")
    # Converts the Python list back into a formatted JSON string for display
    print(json.dumps(movies, indent=4))

def main():
    movies = load_movies()
    while True:
        print("\n--- Movie Watchlist Manager ---")
        print("1. Add a movie\n2. View all movies\n3. Search for a movie")
        print("4. Mark movie as watched\n5. Remove a movie\n6. Display watched/unwatched\n7. Exit")
        
        choice = input("Choose an option: ").strip()
        
        if choice == '1':
            add_movie(movies)
        elif choice == '2':
            view_movies(movies)
        elif choice == '7':
            print("Goodbye!")
            break
        else:
            print("Feature under development.")

if __name__ == "__main__":
    main()

