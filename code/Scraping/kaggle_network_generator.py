"""

This builds a "tidy-data", edge-list for a graph, for an artist.
It maps a network of every possible pathway if you were to click three times in a musician's "fans also like" list.

"""

import pandas as pd
import spotipy as sp

from spotify_functions import get_artist_id, get_artist_name,artist_network_function
import os
import glob

import time
# To give filenames a date!
timestr = time.strftime("%Y_%m_%d")

artist_list_csv_filename ='C:\TomTests\daniel_project\kaggle_genres-reduced.csv'

"""Specify the input list here"""
# automated --> 20_04_15: for daniel [kaggle import]
df = pd.read_csv(artist_list_csv_filename)
search_list = df['artist'].tolist()


# Skip duplicates
existing_networks_path = 'C:\TomTests\daniel_project\kaggle_networks\*.csv'
existing_networks_list = [os.path.basename(x) for x in glob.glob(existing_networks_path)]
existing_networks_artist_names = []
for x in existing_networks_list:
    existing_networks_artist_names.append(x.split('_')[0])
# Getting rid of anything already in kaggle_list
needed_sheets = list(set(search_list).difference(existing_networks_artist_names))
print(len(needed_sheets))

for x in needed_sheets:
    # Get input artist
    search_name = str(x)

    # get URI
    uri = get_artist_id(search_name)

    try:
        # get name
        name_searched = (get_artist_name(uri))
        print('name_searched:', name_searched)  # mostly a diagnostic! also used for saving

        # run the cluster function, which outputs df of all three levels
        cluster_df = artist_network_function(uri)

        # get rid of " and * and / in name for saving filename
        if '"' in name_searched:
            name_searched = name_searched.replace('"','')
        elif '*' in name_searched:
            name_searched = name_searched.replace('*','')
        elif '/' in name_searched:
            name_searched = name_searched.replace('/','')
        else:
            name_searched = name_searched


        # print(cluster_df)

        # save the file
        save_path = 'C:\TomTests\daniel_project\kaggle_networks\\'
        filename = str(name_searched+'_'+'spotify_'+str(timestr)+'.csv')


        cluster_df.to_csv(save_path+filename)

    # Skip when it can't find that artist, and output into artist_error_file_spotify.csv

    except sp.client.SpotifyException:

        import csv

        error_filename = 'artist_error_file_spotify.csv'
        error_path = 'C:/TomTests/Skidmore_Faculty_Dev_19/'
        error_row = [search_name, uri]
        with open(error_path + error_filename, 'a') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(error_row)
        csvFile.close()

        name_searched = 'None'
        print('HTTPError,' 'id=', id)

