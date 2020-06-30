"""
This script uses streamlit to run a web app for users to
explore the relationship between music genres and gender.
"""

import streamlit as st
import numpy as np
import pandas as pd
from functools import partial 
import plotly.graph_objects as go
import difflib

# import matplotlib.pyplot as plt
# import seaborn as sns; sns.set()

# choose app_dir_loc or app_dir_aws from which to import paths
from app_dir_loc import path_X_train, path_X_test, path_y_train, path_y_test, path_genre_list

def main():

    st.markdown("# Gender and Genre")

    # import the data
    X_train = pd.read_csv(path_X_train, index_col = ['artist'])
    y_train = pd.read_csv(path_y_train, index_col = ['artist'])
    X_test = pd.read_csv(path_X_test, index_col = ['artist'])
    y_test = pd.read_csv(path_y_test, index_col = ['artist'])

    # concatenate the train and test data
    X_tot = pd.concat([X_train,X_test])
    y_tot = pd.concat([y_train,y_test])

    # join the inputs and outputs
    data = y_tot.join([X_tot], how = 'outer')

    def lower_space(row):
        string = row.artist.lower()
        string = string.replace("_"," ")
        return string

    data.reset_index(inplace = True)
    data['artist'] = data.apply(lower_space, axis = 1)


    def genrelist(string):
        """This function takes in a string of the form
        appearing in the genrelist of the dataframe.
        It strips the square brackets and extra quotes and
        returns a list of strings where each string is a genre label."""
        string = string.strip("[").strip("]").replace("'","")
        L = [s for s in string.split(',')]
        L_new = []
        for x in L:
            L_new.append(x.replace(" ","_").lstrip("_").rstrip("_"))
        while (str("") in L_new):
            L_new.remove("")
        return L_new

        data['genrelist']= data['genrelist'].apply(genrelist)

    #This function takes in a string and produces a list
    def genrelist(string):
        string = string.strip("[").strip("]").replace("'","")
        L = [s for s in string.split(',')]
        L_new = []
        for x in L:
            L_new.append(x.replace(" ","_").lstrip("_").rstrip("_"))
        while (str("") in L_new):
            L_new.remove("")
        return L_new

    # use the genrelist function to turn strings into lists in the dataframe
    data['genrelist']= data['genrelist'].apply(genrelist)

    # import genre labels
    genrelist_df = pd.read_csv(path_genre_list, index_col = 'Unnamed: 0')



    data_male = data[data.gender == 'male']
    data_female = data[data.gender == 'female']
    tot = data.shape[0]
    m = data_male.shape[0]
    f = data_female.shape[0]
    fem = 100*f/(f+m)
    mal = 100*m/(f+m)


    #Count the number of times that a label occurs:

    def generate_list(data):
        genre_list_1 = data.genrelist.values.tolist()
        genre_list_1 = [x for y in genre_list_1 for x in y]
        genre_counts = pd.Series(genre_list_1)
        label_value_counts = pd.DataFrame(genre_counts.value_counts())
        label_value_counts.columns = ['Frequency']
        genres_list_unique = label_value_counts.index.values.tolist()
        return label_value_counts, genres_list_unique

    label_value_counts, genres_list_unique = generate_list(data)
    
    label_value_counts.reset_index(inplace = True)
    label_value_counts.columns = ["Genre",'Frequency']


    page = st.sidebar.radio("Choose Stats", options = ["Artists","Genre Counts", "Co-Occurrences of Genres",  "Genres of an Artist"])

    if page == "Artists":

        

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


    elif page == "Genre Counts":

        fig = go.Figure(data=[go.Table(
        header=dict(values=list(label_value_counts.columns),
                    fill_color='paleturquoise',
                    align='left'),
        cells=dict(values=[label_value_counts.Genre,label_value_counts.Frequency],
                   fill_color='lavender',
                   align='left'))
        ])

        # summary stats on Genres
        st.write('### Stats on Genre Labels')
        st.write('{} unique genre labels.'.format(genrelist_df.shape[0]))
        st.write('{} genre labels'.format(label_value_counts.Frequency.sum()))
        st.write("The frequency of each genre in descending order (scroll through table):")
        st.plotly_chart(fig)



    elif page == "Co-Occurrences of Genres":

        st.title("Co-Occurrences")

        @st.cache
        def coocurr(QueryGenre):
            # set genre to query
            QueryGenre = QueryGenre 
            # select artists whose genre list contains QueryGenre
            artists_with_QueryGenre = data[data.genrelist.apply(lambda x: True if QueryGenre in x else False)]
            # create a list of genre lists from all artists that have QueryGenre on their list
            QueryGenre_CoGenres = artists_with_QueryGenre.genrelist.values.tolist()
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
        genres_alphabetical = sorted(genres_list_unique)

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
    
    # elif page == "Artists of a Genre":
    #     st.write("Select a genre to see which artists in the data set have been assigned that genre label on Wikipedia.")

    #     @st.cache
    #     def artists_with_label(row, label = 'soul'):
    #         if label in row.genrelist:
    #             return True
    #         else:
    #             return False

    #     # alphabetize genres
    #     genres_alphabetical = sorted(genres_list_unique)

    #     @st.cache
    #     def genre_artists(data, label = 'soul'):
    #         artists_with = partial(artists_with_label,label = label) # create the partial function for the selected genre
    #         data[label] = data.apply(artists_with, axis = 1) # select those artists with the selected genre
    #         artists = data[data[label]].reset_index()
    #         artists = pd.DataFrame(artists.artist.sort_values())
    #         artists.reset_index(inplace = True, drop = True)
    #         artists.columns = ["Artists labeled with {}".format(label)]
    #         return artists # produce alphabetical list of artists with the selected genre


    #     query_genre_artist = st.selectbox('Find the artists in a genre.', genres_alphabetical)
    #     queried_genre_artists = genre_artists(data, query_genre_artist)



    #     # st.plotly_chart(queried_genre_artists.values)

    #     fig = go.Figure(data=[go.Table(
    #     header=dict(values=list(queried_genre_artists.columns),
    #                 fill_color='paleturquoise',
    #                 align='left'),
    #     cells=dict(values=[queried_genre_artists['{}'.format(x)] for x in queried_genre_artists.columns],
    #                fill_color='lavender',
    #                align='left'))
    #     ])

    #     st.plotly_chart(fig)

    elif page == "Genres of an Artist":
        st.write("Select an Artist to see their genres:")
        
        @st.cache
        def genres_of_an_artist(data, artist_name = 'la palabra'):
            genres = data[data.artist == artist_name].genrelist.values[0]
            #genres = ", ".join(map(str,genres))
            genres = ", ".join(genres)
            return genres.title()

        #artist_name = st.selectbox('Select an artist to see their genres',data.sort_index().index.values.tolist())
        
        
        # make case insensitive
        input_text = st.text_input("Type the name of an artist to find matches:")  
        if input_text:
            possibilities = data.artist.to_list()
            matches = difflib.get_close_matches(input_text, possibilities, 5, cutoff = 0.6)
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

main()
# if want to combine with other scripts
# if __name__ == "__main__":
#     main()

