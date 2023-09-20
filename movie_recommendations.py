import pandas as pd
import requests
from bs4 import BeautifulSoup
import numpy as np

url = 'https://www.imdb.com/search/title/?count=100&groups=top_1000&sort=user_rating'
response = requests.get(url)
response
soup = BeautifulSoup(response.content,'html.parser')
# print(soup)
movie_name = []
genre = []
year = []
time = []
rating = []
metascore = []
votes = []
gross = []

movie_data = soup.findAll('div', attrs={'class' : 'lister-item mode-advanced'})

# print(movie_data)

for store in movie_data:
    name = store.h3.a.text
    movie_name.append(name)
    genre_list = store.p.find('span',class_ = 'genre').text.replace('\n','')
    genre.append(genre_list)
    year_of_release = store.h3.find ('span',class_ = 'lister-item-year text-muted unbold').text.replace('(','').replace(')','')
    year.append(year_of_release)
    runtime = store.p.find('span',class_ = 'runtime').text.replace(' min','')
    time.append(runtime)
    rate = store.find('div', class_ = 'inline-block ratings-imdb-rating').text.replace('\n','')    
    rating.append(rate)

# print(year_of_release)
# count=np.count_nonzero(movie_name)
# print(count)
movie_DF = pd.DataFrame({'genre_list' : genre , 'Title' : movie_name,'Year of release' : year, 'Watch time' : time, 'Movie rating' : rating})

movie_DF.to_csv('movies_list.csv')

import pandas as pd

# Read scraped data into a Pandas DataFrame
try:
    df = pd.read_csv('movies_list.csv')  # Adjust the filename and format as needed
except FileNotFoundError:
    print("Error: Scraped data file not found.")
    exit(1)
except pd.errors.EmptyDataError:
    print("Error: Scraped data file is empty.")
    exit(1)
except pd.errors.ParserError:
    print("Error: Unable to parse scraped data.")
    exit(1)
    
# Prompt user for genre input
user_genre = input("Enter a film genre: ")

# Filter movies by user's input genre
filtered_movies = df[df['genre_list'].str.contains(user_genre, case=False)]

# Display the movie suggestions
if not filtered_movies.empty:
    print("Here are some movie suggestions based on your genre:")
    print(filtered_movies[['genre_list','Title','Year of release']])
else:
    print(f"No movies found for the genre '{user_genre}'.")
