"""
This script uses streamlit to run a web app for users to
explore the relationship between music genres and gender.
"""

import streamlit as st
import numpy as np
import pandas as pd
from functools import partial 
import plotly.graph_objects as go

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


    page = st.sidebar.radio("Choose Stats", options = ["Artists","Genres"])

    if page == "Artists":

        # summary stats on Artists
        #a,b,c = data.genrelist_length.mean(), data.genrelist_length.std(), data.genrelist_length.max()

        st.write('### Stats on Artists')
        st.write(data.shape[0], "artists with genre and binary-gender labels")
        st.write(f, "female artists, or", round(fem,2), "%")
        st.write(m,'male artists, or',round(mal,2), '%')

    elif page == "Genres":

        # summary stats on Genres
        st.write('### Stats on Genre Labels')
        st.write('{} unique genre labels.'.format(genrelist_df.shape[0]))
        st.write('{} genre labels'.format(label_value_counts.Frequency.sum()))
        st.write("The frequency of each genre in descending order:")

        #st.write('### Stats on Genre Labels and Artists')
        #st.write('Mean number of genre labels per artist: {}.'.format(round(a,2)))
        #st.write('STD of the number of genre labels: {}.'.format(round(b,2)))
        #st.write('Max number of genre labels: {}.'.format(c))

    fig = go.Figure(data=[go.Table(
        header=dict(values=list(label_value_counts.columns),
                    fill_color='paleturquoise',
                    align='left'),
        cells=dict(values=[label_value_counts.Genre,label_value_counts.Frequency],
                   fill_color='lavender',
                   align='left'))
    ])

    st.plotly_chart(fig)


if __name__ == "__main__":
    main()

