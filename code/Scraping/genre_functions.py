import spotipy
import pandas as pd

# start API session
from spotipy.oauth2 import SpotifyClientCredentials

client_credentials_manager = SpotifyClientCredentials(client_id='',
                                                      client_secret='')

sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
sp.trace = False



def get_spotify_genres(x):
    result0 = sp.artist(x)

    try:
        artist_1_genre = result0['genres']
    except IndexError:
        artist_1_genre = ['Index Error None']

    return artist_1_genre


def get_wiki_genre(site_example):
    # OK, so first call wiki
    import requests
    import re
    from bs4 import BeautifulSoup as bs
    page = requests.get(site_example)

    # Then get the whole page content via BS lol
    soup = bs(page.content, 'html.parser')

    # Find the "Genres" header row thing of the side table thing ('table', class_="infobox biography vcard")
    genre_place = soup.find('th', scope="row", text="Genres")

    # Then get the cell next to the "Genres" cell
    genres_td = genre_place.find_next_siblings("td")

    # Then couldn't figure out how to get nested bits of HTML so just converted it to a string and started searching
    # The Genres are always(?) linked to other places on wiki, so they have a link, which is called by a title=""
    genre_match_list = []
    for m in re.finditer('title=".*?"', str(genres_td)):
        genre_titles = m.group()
        # print(genre_titles)
        genre_match_list.append(str(genre_titles))

    # basically get rid of excess string info stuff lol, make into neat list
    genre_list = []
    for x in genre_match_list:
        z = x[7:]
        y = z[:-1]
        genre_list.append(y)

    return genre_list


def get_wiki_url_from_name(name):
    wiki_url = 'https://en.wikipedia.org/wiki/'+str(name)
    return wiki_url
