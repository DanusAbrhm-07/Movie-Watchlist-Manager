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
            
    movies.append({"title": title, "watched": is_watched})
    save_movies(movies)
    print(f"'{title}' added successfully!")

def view_movies(movies):
    if not movies:
        print("Your watchlist is empty.")
        return
    print("\n--- All Movies ---")
    print(json.dumps(movies, indent=4))

def search_movies(movies):
    search_term = input("Enter title to search: ").strip().lower()
    results = [m for m in movies if search_term in m["title"].lower()]
    if results:
        print(json.dumps(results, indent=4))
    else:
        print("No matching movies found.")

def mark_watched(movies):
    if not movies:
        print("Your watchlist is empty.")
        return
    print("\nSelect a movie:")
    for i, m in enumerate(movies):
        print(f"{i + 1}. {m['title']}")
        
    try:
        index = int(input("\nEnter the number to mark as watched: ")) - 1
        if 0 <= index < len(movies):
            if movies[index]["watched"] == "Yes":
                print("Movie is already marked as watched.")
            else:
                movies[index]["watched"] = "Yes"
                save_movies(movies)
                print("Marked as watched!")
        else:
            print("Error: Invalid movie number.")
    except ValueError:
        print("Error: Please enter a valid number.")

def remove_movie(movies):
    if not movies:
        print("Your watchlist is empty.")
        return
    print("\nSelect a movie:")
    for i, m in enumerate(movies):
        print(f"{i + 1}. {m['title']}")
        
    try:
        index = int(input("\nEnter the number to remove: ")) - 1
        if 0 <= index < len(movies):
            removed = movies.pop(index)
            save_movies(movies)
            print(f"Removed '{removed['title']}'.")
        else:
            print("Error: Invalid movie number.")
    except ValueError:
        print("Error: Please enter a valid number.")

def filter_movies(movies):
    filter_choice = input("Show (1) Watched or (2) Unwatched? ").strip()
    if filter_choice not in ['1', '2']:
        print("Error: Invalid choice.")
        return
        
    target_status = "Yes" if filter_choice == '1' else "No"
    filtered = [m for m in movies if m["watched"] == target_status]
    
    if not filtered:
        print("No movies found for this category.")
    else:
        print(json.dumps(filtered, indent=4))

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
        elif choice == '3':
            search_movies(movies)
        elif choice == '4':
            mark_watched(movies)
        elif choice == '5':
            remove_movie(movies)
        elif choice == '6':
            filter_movies(movies)
        elif choice == '7':
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please choose a number from 1 to 7.")

if __name__ == "__main__":
    main()