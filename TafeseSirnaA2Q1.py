"""
TafeseSirnaA2Q1

COMP 1012 A02

INSTRUCTOR: Dr. Shaiful Chowdhury
ASSIGNMENT: A2 Q1
AUTHOR:     Sirna Tafese
VERSION:    Oct-30th-2024

PURPOSE:   This program analyzes extensive data on Netflix
           movies, users, and ratings to extract insights,
           such as identifying the movie with the highest 
           average rating. Additionally, a simple filtering 
           algorithm generates top movie recommendations based
           on a chosen movie.
"""
# ----- Imports -----
import os  # Import the os library for file operations

# ----- Constants -----
MOVIE_DIRECTORY = "all_movies"    # Directory containing movie data files
MOVIE_TITLES_FILE = "movie_titles.txt"  # Filename for movie title information

MOVIE_PROCESS_STEP = 1000   # Interval to display progress when processing many files

# ----- Variables -----

# Dictionary to store movie data including viewer info and ratings
movie_data = {}

# Dictionary to store viewer data, including the movies and ratings per viewer
viewer_data = {}

# Dictionary to map movie IDs to movie titles
movie_titles = {}

# Counters for movie statistics
total_movie_count = 0                  # Total number of movies
high_rating_movies_count = 0            # Count of movies with average rating >= 4.0
high_rating_high_viewership_count = 0    # Count of movies with high ratings and viewership > 1000

print("Processing started...")

# Loop through each file in the movie directory
for movie_file_name in os.listdir(MOVIE_DIRECTORY):
    movie_file = open(os.path.join(MOVIE_DIRECTORY, movie_file_name))

    # Read the movie ID from the first line, converting it to an integer
    movie_id = movie_file.readline()
    movie_id = int(movie_id.strip().strip(":"))

    # Initialize movie data if the movie ID isn't already in the dictionary
    if movie_id not in movie_data:
        movie_data[movie_id] = {}
        movie_data[movie_id]["ratings"] = {}
        movie_data[movie_id]["average_rating"] = 0
        movie_data[movie_id]["unique_viewers_count"] = 0
        total_movie_count += 1

    # Loop through each viewer's rating in the file
    for rating_entry in movie_file:
        data = rating_entry.split(",")
        
        user_id = int(data[0].strip())  # Get the viewer ID
        user_rating = int(data[1].strip())  # Get the viewer's rating
        user_watch_date = data[2].strip()  # Get the date of the viewing

        # Check if the viewer is unique for this movie and update count if needed
        if user_id not in movie_data[movie_id]["ratings"]:
            movie_data[movie_id]["unique_viewers_count"] += 1

        # Store viewer's rating in the movie data and add to total rating
        movie_data[movie_id]["ratings"][user_id] = user_rating
        movie_data[movie_id]["average_rating"] += user_rating

        # Add movie rating to the viewer's profile if the viewer isn't already in the viewer dictionary
        if user_id not in viewer_data:
            viewer_data[user_id] = {}
        viewer_data[user_id][movie_id] = user_rating

    movie_file.close()  # Close the file after reading

    # Calculate the average rating for the movie
    if movie_data[movie_id]["unique_viewers_count"] != 0:
        movie_data[movie_id]["average_rating"] = movie_data[movie_id]["average_rating"] / movie_data[movie_id]["unique_viewers_count"]

    # Update high rating and viewership statistics if conditions are met
    if movie_data[movie_id]["average_rating"] >= 4:
        high_rating_movies_count += 1
        if movie_data[movie_id]["unique_viewers_count"] > 1000:
            high_rating_high_viewership_count += 1
    
    # Append movie details to an output file
    with open('output.txt', 'a') as f:
        f.write("ID: {:5.0f}\tR:{:.2f}\tV:{}\n".format(movie_id, movie_data[movie_id]["average_rating"], movie_data[movie_id]["unique_viewers_count"]))

    # Print progress for every interval of MOVIE_PROCESS_STEP
    if total_movie_count % MOVIE_PROCESS_STEP == 0:
        print("{} movies processed.".format(total_movie_count))


# Load movie titles from the specified file
movie_titles_file = open(MOVIE_TITLES_FILE, encoding="ISO-8859-1")
for movie_entry in movie_titles_file:
    data = movie_entry.split(",", 2)

    # Get movie ID, year, and title
    movie_id = int(data[0].strip())
    movie_year = data[1].strip()
    movie_name = data[2].strip()

    # Convert year to an integer if it's numeric
    if movie_year.isnumeric():
        movie_year = int(movie_year)

    # Store movie title in movie_titles dictionary
    if movie_id not in movie_titles:
        movie_titles[movie_id] = ""
    
    movie_titles[movie_id] = movie_name


# Initialize variables for exploration of unique viewers, highest rating, and most viewed by a user
most_unique_viewers_movie = 0
highest_rated_movie = 0
most_movies_viewer = 0

most_unique_viewers_count = 0
highest_rating_count = 0

# Find movie with the most unique viewers and highest average rating
for movie in movie_data:
    
    # Update movie with the most unique viewers if current movie's count is higher
    if movie_data[movie]["unique_viewers_count"] > most_unique_viewers_count:
        most_unique_viewers_count = movie_data[movie]["unique_viewers_count"]
        most_unique_viewers_movie = movie
    
    # Update movie with the highest rating if current movie's rating is higher
    if movie_data[movie]["average_rating"] > highest_rating_count:
        highest_rating_count = movie_data[movie]["average_rating"]
        highest_rated_movie = movie

most_movies_viewed_count = 0

# Find viewer who has watched the most movies
for viewer in viewer_data:

    # Update if the current viewer has watched more movies
    if len(viewer_data[viewer]) > most_movies_viewed_count:
        most_movies_viewed_count = len(viewer_data[viewer])
        most_movies_viewer = viewer

# ----- Data Exploration OUTPUT  -----
# Print summary statistics based on the data
print("The total number of movies with high ratings: " + str(high_rating_movies_count))
print("The total number of movies with high ratings and viewers: " + str(high_rating_high_viewership_count))
print("The movie with the most {} unique viewers is: {}".format(most_unique_viewers_count, movie_titles[most_unique_viewers_movie]))
print("The movie with the highest {:.2f} average rating is: {}".format(highest_rating_count, movie_titles[highest_rated_movie]))
print("The viewer with the most watched {} movies is: {}".format(most_movies_viewed_count, most_movies_viewer))


# ----- Recommendation System -----

# Initialize variables for movie recommendation
suggested_movie = 0
user_input_movie = 0
highest_similarity_score = 0

# Continuously prompt user for movie ID and recommend similar movies
user_input = input("Enter a movie id: ")
while user_input.upper() != "ESC":

    user_input_movie = int(user_input)

    # Get a set of viewers who watched the input movie
    input_movie_viewers = set(movie_data[user_input_movie]["ratings"].keys())
    
    # Reset highest similarity score and suggested movie
    highest_similarity_score = 0
    suggested_movie = 0

    # Calculate similarity with each movie based on shared viewers
    for movie in movie_data:
        suggested_movie_viewers = set(movie_data[movie]["ratings"].keys())

        sim_score = len(input_movie_viewers.intersection(suggested_movie_viewers))
        sim_score = sim_score / len(input_movie_viewers.union(suggested_movie_viewers))

        # Update suggested movie if a higher similarity score is found
        if sim_score > highest_similarity_score and movie != user_input_movie:
            highest_similarity_score = sim_score
            suggested_movie = movie

    # Display the suggested movie
    print(str(suggested_movie) + " " + movie_titles[suggested_movie])
    user_input = input("Enter a movie id: ")

# End of program execution message
print()     # Print blank line for spacing
print("End of processing")