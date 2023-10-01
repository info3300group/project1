# do NOT submit this file on cmsx as part of the project - I am only uploading
# this script to github as reference.

import csv
import requests
import json 
import secret_api_key # this file will not be tracked in git - to run this script locally, create your own api key at omdbapi.com

api_endpoint_url = f"http://www.omdbapi.com/?apikey={secret_api_key.OMDB_API_KEY}"
movies_already_stored = set()

with open('ratings.csv', 'w', newline='') as file:
    moviesRatingsWriter = csv.writer(file)
    moviesRatingsWriter.writerow(["Movie Title", "Imdb Rating"])

    with open('movies.csv', mode ='r')as moviesDataFile:
        moviesDataReader = csv.reader(moviesDataFile)
        # skip column title line
        next(moviesDataReader)

        # fetch rating for each movie
        for lines in moviesDataReader:
                movie_title = lines[0]
                if movie_title not in movies_already_stored:
                    movies_already_stored.add(movie_title)

                    # get movie info from api 
                    movie_year = lines[1]
                    api_endpoint_url_for_movie = f"{api_endpoint_url}&t={movie_title}&y={movie_year}"
                    res = requests.get(api_endpoint_url_for_movie)
                    response = json.loads(res.text)

                    # put movie title and associated imdb rating into file (if it exists)
                    try:
                        imdb_rating = response['Ratings'][0]['Value'][0:3]
                        moviesRatingsWriter.writerow([movie_title, imdb_rating])
                        print("found movie ", movie_title)
                    except:
                        try:
                            api_endpoint_url_for_movie = f"{api_endpoint_url}&t={movie_title}"
                            res = requests.get(api_endpoint_url_for_movie)
                            response = json.loads(res.text)
                            imdb_rating = response['Ratings'][0]['Value'][0:3]
                            moviesRatingsWriter.writerow([movie_title, imdb_rating])
                            print("found movie ", movie_title)
                        except:
                            moviesRatingsWriter.writerow([movie_title, "None"])
                            print("movie not found", movie_title, api_endpoint_url_for_movie)

print("all done")
                         
