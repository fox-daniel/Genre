"""
This script uses streamlit to run a web app for users to
explore the co-occurrences of genres.
"""

import streamlit as st
import numpy as np
import pandas as pd

# import matplotlib.pyplot as plt
# import seaborn as sns; sns.set()

# import re

# from functools import partial

# import plotly.graph_objects as go


st.markdown("# Gender and Genre")

#reference the datetime used to title the data
now = '2020-05-18-10-06'

# import the data
X_train = pd.read_csv('/Users/Daniel/Code/Genre/data/genre_lists/data_ready_for_model/wiki-kaggle_X_train_{}.csv'.format(now), index_col = ['artist'])
y_train = pd.read_csv('/Users/Daniel/Code/Genre/data/genre_lists/data_ready_for_model/wiki-kaggle_y_train_{}.csv'.format(now), index_col = ['artist'])
X_test = pd.read_csv('/Users/Daniel/Code/Genre/data/genre_lists/data_ready_for_model/wiki-kaggle_X_test_{}.csv'.format(now), index_col = ['artist'])
y_test = pd.read_csv('/Users/Daniel/Code/Genre/data/genre_lists/data_ready_for_model/wiki-kaggle_y_test_{}.csv'.format(now), index_col = ['artist'])

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
genrelist_df = pd.read_csv('/Users/Daniel/Code/Genre/data/genre_lists/data_ready_for_model/genre_list_{}.csv'.format(now), index_col = 'Unnamed: 0')



data_male = data[data.gender == 'male']
data_female = data[data.gender == 'female']
tot = data.shape[0]
m = data_male.shape[0]
f = data_female.shape[0]
fem = 100*f/(f+m)
mal = 100*m/(f+m)

st.write(data.shape[0], "artists with genre and binary-gender labels")
st.write(f, "female artists, or", round(fem,2), "%")
st.write(m,'male artists, or',round(mal,2), '%')
st.write('{} unique genre labels.'.format(genrelist_df.shape[0]))

#Count the number of times that a label occurs:
@st.cache(persist=True)
def generate_list(data):
    genre_list_1 = data.genrelist.values.tolist()
    genre_list_1 = [x for y in genre_list_1 for x in y]
    genre_counts = pd.Series(genre_list_1)
    label_value_counts = pd.DataFrame(genre_counts.value_counts())
    label_value_counts.columns = ['Frequency']
    genres_list_unique = label_value_counts.index.values.tolist()
    return label_value_counts, genres_list_unique

label_value_counts, genres_list_unique = generate_list(data)

st.write("The frequency of each genre in descending order")
label_value_counts

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
    QueryGenre_CoGenres_counts.index.name = 'genres'
    return QueryGenre_CoGenres_counts

query_genre = st.selectbox('Select a genre and see with which genres it co-occurs.',genres_list_unique)

#query_genre = 'hip_hop'

st.write("The genres that co-occurr with",query_genre,":")
cooccurrences = coocurr(query_genre)

cooccurrences