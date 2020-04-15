import pandas as pd
from genre_functions import *
from spotify_functions import get_artist_id, get_artist_name
import requests

filename_to_open = 'C:\TomTests\daniel_project\singers_gender.csv'
filename_to_write = 'C:\TomTests\daniel_project\kaggle_genres.csv'

# latin_1 encoding to get accents, diacritics, whatever
df1 = pd.read_csv(filename_to_open, encoding='latin_1')

artist_list = df1['artist'].tolist()
genre_list = []
artist_result_list = []
for x in artist_list:
    print(x)
    temp_uri = get_artist_id(x)
    if temp_uri == "No URI":
        genre_list.append('none')
        artist_result_list.append('none')
    else:
        genre_list.append(get_spotify_genres(temp_uri))
        artist_result_list.append(get_artist_name(temp_uri))

df1['retrieved'] = artist_result_list
df1['genre'] = genre_list

df1.to_csv(filename_to_write)
