import spotipy
import pandas as pd

# start API session
from spotipy.oauth2 import SpotifyClientCredentials

client_credentials_manager = SpotifyClientCredentials(client_id='',
                                                      client_secret='')

sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
sp.trace = False


# Get artist name/ID -->>> AHH not sure how to deal with errors, I'm using Tank and The Bangas as a placeholder 6275989
def get_artist_id(input_name):
    if '+' in input_name:  # remove all the "+" characters. this was breaking the search
        input_name = input_name.replace('+', '')
    else:
        input_name = input_name
    result0 = sp.search(q='artist:' + input_name, type='artist')
    try:
        uri = result0['artists']['items'][0]['uri']
    except IndexError:
        uri = 'No URI'
    return uri


# Gets spotify artist URI from input name to search, and allows you to select the one you want
def get_artist_id_selection(input_name):
    if '+' in input_name:  # remove all the "+" characters. this was breaking the search
        input_name = input_name.replace('+', '')
    else:
        input_name = input_name
    result0 = sp.search(q='artist:' + input_name, type='artist')
    artist_items_list = result0['artists']['items']

    try:
        selection_dict = {}
        i = 0

        while i < len(artist_items_list):
            print(i,':',artist_items_list[i]['name'],'|')
            selection_dict[i] = artist_items_list[i]['uri']

            i += 1

        print('selection_dict', selection_dict)

        # ask for selection
        selection_number = int(input("Select a number: "))
        uri = selection_dict[selection_number]

    except IndexError:
        uri = 'No URI'
    return uri


# from URI
def get_artist_name(input_uri):
    result0 = sp.artist(input_uri)['name']
    return result0


# takes ID as input
# Gets list of related artist URIs given a URI, puts into tidy-data
def find_spotify_related_artist_uris(uri):
    related_artist_list = []
    related_artist_search = sp.artist_related_artists(uri)
    for x in related_artist_search['artists']:
        related_artist_list.append([uri,x['uri']])

    return related_artist_list


## Gets list of related artist names given a URI, puts into tidy-data
def find_spotify_related_artist_names(uri):
    related_artist_list = []
    related_artist_search = sp.artist_related_artists(uri)
    for x in related_artist_search['artists']:
        related_artist_list.append([sp.artist(uri)['name'],x['name']])

    return related_artist_list


# Gets list of both names and uris for related artists
def related_artist_names_uris(uri):
    related_artists_list = []
    related_artist_search = sp.artist_related_artists(uri)
    for x in related_artist_search['artists']:
        related_artists_list.append([sp.artist(uri)['name'],uri,x['name'],x['uri']])

    return related_artists_list

# Gets list of genres and followers for a given URI
def get_genre_URI(uri):
    genre_list = []
    try:
        artist_followers = sp.artist(uri)['followers']
    except IndexError:
        artist_1_followers = 0
    return artist_followers
    return genre_list

def get_followers(uri):
    try:
        artist_followers = sp.artist(uri)['followers']
    except IndexError:
        artist_1_followers = 0
    return artist_followers


