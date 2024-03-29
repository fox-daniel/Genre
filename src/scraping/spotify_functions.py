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


# so, now i need to make a function that, given an artist, spits out a 1, 2, or 3 level cluster PD
def artist_network_function(x):
    # first_cluster_list = related_artist_names_uris(x)
    # col_names = ['artist_name','artist_uri','related_name','related_uri']

    # with URIS only
    first_cluster_list = find_spotify_related_artist_uris(x)
    col_names = ['artist_uri','related_uri']
    df1 = pd.DataFrame(first_cluster_list, columns=col_names)
    # add column for cluster "level"
    df1['cluster'] = 1
    #print('df',df1)
    print('# of 1st related:', len(first_cluster_list))

    # CLUSTER LEVEL 2
    # now try to get each related artist's cluster
    second_cluster_list = []
    for x in df1['related_uri'].tolist():

        #print('checking1', x, time.time())

        # this would be for name, uri, related_name, related_uri
        # second_cluster_list.append(related_artist_names_uris(x))

        # try with just uris
        second_cluster_list.append(find_spotify_related_artist_uris(x))

        # print('checking2',x,time.time())

    # flatten
    second_cluster_list = [item for sublist in second_cluster_list for item in sublist]
    print('# of 2nd related:', len(second_cluster_list))
    df2 = pd.DataFrame(second_cluster_list, columns=col_names)
    # add column for cluster "level"
    df2['cluster'] = 2

    # CLUSTER LEVEL 3
    # now try to get each 2nd-related artist's cluster
    third_cluster_list = []
    for x in df2['related_uri'].tolist():

        # this would be for name, uri, related_name, related_uri
        # third_cluster_list.append(related_artist_names_uris(x))

        # just uris
        third_cluster_list.append(find_spotify_related_artist_uris(x))

        # print('last3rdCluster:', third_cluster_list[-1])
        # print('checking', x, time.time())

    # flatten
    third_cluster_list = [item for sublist in third_cluster_list for item in sublist]
    print('# of 3rd related:', len(third_cluster_list))

    df3 = pd.DataFrame(third_cluster_list, columns=col_names)
    # add column for cluster "level"
    df3['cluster'] = 3

    # concatentate
    frames = [df1, df2, df3]
    result = pd.concat(frames)
    return result

