"""
This script uses streamlit to run a web app for users to
explore the relationship between music genres and gender.
"""

import streamlit as st
from functools import partial 
import plotly.graph_objects as go
from difflib import get_close_matches
import sklearn

import numpy as np
import pandas as pd

#import matplotlib.pyplot as plt
#import seaborn as sns; sns.set()

import genre_data_loader
#from nested_subsets import NestedSubsets

now = '2020-07-07-09-58'

# import matplotlib.pyplot as plt
# import seaborn as sns; sns.set()

# choose app_dir_loc or app_dir_aws from which to import paths
from app_dir_aws import path_X_train, path_X_test, path_y_train, path_y_test


def load_data():
    # call data loader script
    genre_data = genre_data_loader.LoadGenreData(now, X_path_train = path_X_train, y_path_train = path_y_train,\
        X_path_test = path_X_test, y_path_test = path_y_test)

    # load data with genres as lists, sets, and strings
    data = genre_data.as_lists()
    data = genre_data.as_sets()
    data = genre_data.as_strings()
    X = genre_data.get_sparse_X_vector()

    # load dict from id to genre
    dictidg = genre_data.get_dict_id_to_genre()

    # create list of all genres
    list_of_genres = genre_data.get_list_of_genres()

    def lower_space(row):
        string = row.artist.lower()
        string = string.replace("_"," ")
        return string

    data.reset_index(inplace = True)
    data['artist'] = data.apply(lower_space, axis = 1)


    # import genre labels
    genrelist_df = pd.DataFrame({'genre':list_of_genres})

    return data, X, dictidg, list_of_genres, genrelist_df

data, X, dictidg, list_of_genres, genrelist_df = load_data()

def main():

    st.markdown("# Gender and Genre")
    
    page = st.sidebar.radio("Choose Stats", options = ["Artists","Genre Frequency", "Co-Occurrences of Genres",  "Genres of an Artist"])

    if page == "Artists":
        page_artists()

    elif page == "Genre Frequency":
        page_genre_frequency()

    elif page == "Co-Occurrences of Genres":
        page_cooccurr()
    
    elif page == "Genres of an Artist":
        page_genres_of_an_artist()

    # elif page == "Artists of a Genre":
    #     page_artists_of_a_genre()

def page_artists():
    data_male = data[data.gender == 'male']
    data_female = data[data.gender == 'female']
    tot = data.shape[0]
    m = data_male.shape[0]
    f = data_female.shape[0]
    fem = 100*f/(f+m)
    mal = 100*m/(f+m)

    st.write('### Stats on Artists')
    st.write(data.shape[0], "artists with genre and binary-gender labels")
    st.write(f, "female artists, or", round(fem,2), "%")
    st.write(m,'male artists, or',round(mal,2), '%')

    st.write('### Stats on Genre Labels and Artists')

    #summary stats on Artists
    a,b,c = data.genrelist_length.mean(), data.genrelist_length.std(), data.genrelist_length.max()
    st.write('Mean number of genre labels per artist: {}.'.format(round(a,2)))
    st.write('STD of the number of genre labels: {}.'.format(round(b,2)))
    st.write('Max number of genre labels: {}.'.format(c))


def page_genre_frequency():

    label_value_counts = frequency_by_gender(X, data, dictidg)

    fig_alpha = go.Figure(data=[go.Table(
    header=dict(values=list(label_value_counts.columns),
                fill_color='paleturquoise',
                align='left'),
    cells=dict(values=[label_value_counts[col] for col in label_value_counts.columns],
               fill_color='lavender',
               align='left'))
    ])

    # summary stats on Genres
    st.write('### Stats on Genre Labels')
    st.write('{} unique genre labels.'.format(genrelist_df.shape[0]))
    st.write('{} genre labels'.format(label_value_counts.frequency.sum()))
    st.write("The frequency of each genre (alphabetical):")
    st.plotly_chart(fig_alpha)

    fig_freq = go.Figure(data=[go.Table(
    header=dict(values=list(label_value_counts.sort_values('frequency', ascending = False).columns),
                fill_color='paleturquoise',
                align='left'),
    cells=dict(values=[label_value_counts.sort_values('frequency', ascending = False)[col] for col in label_value_counts.columns],
               fill_color='lavender',
               align='left'))
    ])

    st.write("The frequency of each genre ordered by frequency:")
    st.plotly_chart(fig_freq)

#Count genre frequencies

def frequency_by_gender(X, data, dictidg):
    """
    Create dataframe with frequencies of genres by gender
    Reliance: to be called when the following exist:
        <genre_data> as a LoadGenreData instance
        dictidg from <genre_data> method
        
    Input: 
    X: Sparse genre data output from <genre_data>
    data: genre_data.data object; does not matter if genres are in sets, lists, strings
    """
    
    # calculate frequencies from the sparse format
    freq = X.sum(0)

    # put into a dataframe
    genre_frequency = pd.DataFrame(freq).transpose()
    genre_frequency.index.name = 'genre'
    genre_frequency.columns = ['frequency']

    # convert index from id to genre
    genre_frequency.reset_index(inplace = True)
    genre_frequency['genre'] = genre_frequency.apply(lambda x: dictidg[x.genre], axis = 1)
    genre_frequency.set_index(['genre'], inplace = True)

    # create gender masks
    MaskF = (data.gender == 'female')
    MaskF.reset_index(drop = True, inplace = True)
    MaskM = (data.gender == 'male')
    MaskM.reset_index(drop = True, inplace = True)

    # apply gender masks to sparse matrix
    X_f = X[MaskF.values,:]
    X_m = X[MaskM.values,:]

    # create frequency counts by gender
    FemFreq = X_f.sum(0)
    MalFreq = X_m.sum(0)

    # convert matrix to list
    FemFreq = [*FemFreq.flat]
    MalFreq = [*MalFreq.flat]

    # put lists into frequency dataframe
    genre_frequency['female'] = pd.Series(FemFreq, index = genre_frequency.index)
    genre_frequency['male'] = pd.Series(MalFreq, index = genre_frequency.index)
    
    genre_frequency.reset_index(inplace = True)

    return genre_frequency

def page_cooccurr():

    st.title("Co-Occurrences")

    @st.cache
    def coocurr(QueryGenre):
        # set genre to query
        QueryGenre = QueryGenre 
        # select artists whose genre list contains QueryGenre
        artists_with_QueryGenre = data[data.genre_list.apply(lambda x: True if QueryGenre in x else False)]
        # create a list of genre lists from all artists that have QueryGenre on their list
        QueryGenre_CoGenres = artists_with_QueryGenre.genre_list.values.tolist()
        # flatten
        QueryGenre_CoGenres = [x for y in QueryGenre_CoGenres for x in y]
        # turn it into a Series
        QueryGenre_CoGenres = pd.Series(QueryGenre_CoGenres)
        # make counts of appearances of the co-genres
        QueryGenre_CoGenres_counts = pd.DataFrame(QueryGenre_CoGenres.value_counts(), columns = ['Frequency'])
        # drop the QueryGenre itself
        QueryGenre_CoGenres_counts.drop(QueryGenre, axis = 0, inplace = True )
        #QueryGenre_CoGenres_counts.rename_axis( 'counts', inplace = True)
        QueryGenre_CoGenres_counts.index.name = 'Genres'
        QueryGenre_CoGenres_counts.sort_index(inplace = True)
        QueryGenre_CoGenres_counts.reset_index(inplace = True)
        return QueryGenre_CoGenres_counts

    #list_sorted = sorted(genres_list_unique)

    # alphabetize genres
    genres_alphabetical = sorted(list_of_genres)

    query_genre = st.selectbox('Select a genre and see with which genres it co-occurs.', genres_alphabetical)

    #query_genre = 'hip_hop'

    st.write("The genres that co-occurr with",query_genre,":")
    cooccurrences = coocurr(query_genre)

    fig = go.Figure(data=[go.Table(
    header=dict(values=list(cooccurrences.columns),
                fill_color='paleturquoise',
                align='left'),
    cells=dict(values=[cooccurrences['{}'.format(x)] for x in cooccurrences.columns],
               fill_color='lavender',
               align='left'))
    ])

    st.plotly_chart(fig)


def page_genres_of_an_artist():

    st.write("Select an Artist to see their genres:")
            
    @st.cache
    def genres_of_an_artist(data, artist_name = 'la palabra'):
        genres = data[data.artist == artist_name].genre_list.values[0]
        #genres = ", ".join(map(str,genres))
        genres = ", ".join(genres)
        return genres.title()

    #artist_name = st.selectbox('Select an artist to see their genres',data.sort_index().index.values.tolist())
    
    
    # make case insensitive
    input_text = st.text_input("Type the name of an artist to find matches:")  
    if input_text:
        possibilities = data.artist.to_list()
        matches = get_close_matches(input_text, possibilities, 5, cutoff = 0.6)
        if matches:
            match = st.selectbox("Now select a match",matches)
            artist_name = match
            genres_of_artist = genres_of_an_artist(data, artist_name)
            genres_of_artist = genres_of_artist.replace("_"," ")
            #genres_of_artist = pd.DataFrame({'Genres':genres_of_artist})
        else:
            artist_name = 'no matches'
    else:  
        genres_of_artist = 'no matches' 
    
    st.write(genres_of_artist)
    # or as a dataframe (still needs str -> list for genres of artist)
    # fig = go.Figure(data=[go.Table(
    # header=dict(values=list(genres_of_artist.columns),
    #             fill_color='paleturquoise',
    #             align='left'),
    # cells=dict(values=[genres_of_artist['{}'.format(x)] for x in genres_of_artist.columns],
    #            fill_color='lavender',
    #            align='left'))
    # ])

    # st.plotly_chart(fig)

def page_artists_of_a_genre():
    st.write("Select a genre to see which artists in the data set have been assigned that genre label on Wikipedia.")

    @st.cache
    def artists_with_label(row, label = 'soul'):
        if label in row.genre_list:
            return True
        else:
            return False

    # alphabetize genres
    genres_alphabetical = sorted(list_of_genres)

    
    def genre_artists(data, label = 'soul'):
        artists_with = partial(artists_with_label,label = label) # create the partial function for the selected genre
        data[label] = data.apply(artists_with, axis = 1) # select those artists with the selected genre
        artists = data[data[label]].reset_index()
        artists = pd.DataFrame(artists.artist.sort_values())
        artists.reset_index(inplace = True, drop = True)
        artists.columns = ["Artists labeled with {}".format(label)]
        return artists # produce alphabetical list of artists with the selected genre


    query_genre_artist = st.selectbox('Find the artists in a genre.', genres_alphabetical)
    queried_genre_artists = genre_artists(data, query_genre_artist)



    # st.plotly_chart(queried_genre_artists.values)

    fig = go.Figure(data=[go.Table(
    header=dict(values=list(queried_genre_artists.columns),
                fill_color='paleturquoise',
                align='left'),
    cells=dict(values=[queried_genre_artists['{}'.format(x)] for x in queried_genre_artists.columns],
               fill_color='lavender',
               align='left'))
    ])

    st.plotly_chart(fig)

main()
# if want to combine with other scripts
# if __name__ == "__main__":
#     main()

