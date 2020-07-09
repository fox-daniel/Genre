"""
Input:
Reads in a csv file with a col of ['genrelist']

Output:
And make a tidy dataset of [a,b,count] that includes [b,a,count], outputs to csv

This does take a little bit of time
"""

import pandas as pd
import itertools

output_path = 'genre_edges_list_wiki_corpus_full.csv'
# get genre lists for artists in corpus
# training corpus: "C:\TomTests\daniel_project\Genre\data\genre_lists\data_ready_for_model\wiki-kaggle_X_train_2020-05-18-10-06.csv"
# full corpus:
input_path = "C:\TomTests\daniel_project\Genre\data\genre_lists\data_ready_for_model\wiki-kaggle_genres_gender_cleaned_2020-05-11-14-34.csv"
df = pd.read_csv(input_path)
input_genre_list = df['genrelist'].tolist()

# genre_list is read in as  a list of strings. Use Daniel's function to convert to list of lists
# FROM DANIEL's "genre_model_logistic_regression.py"
"""This function takes in a string of the form
appearing in the genrelist of the dataframe.
It strips the square brackets and extra quotes and
returns a list of strings where each string is a genre label."""
def genrelist(string):
    string = string.strip("[").strip("]").replace("'","")
    L = [s for s in string.split(',')]
    L_new = []
    for x in L:
        L_new.append(x.replace(" ","_").lstrip("_").rstrip("_"))
    while (str("") in L_new):
        L_new.remove("")
    return L_new

genre_list_of_lists = []
for x in input_genre_list:
    genre_list_of_lists.append(genrelist(x)) #Daniel's function

# drop out any singletons since not needed for edges between genre pairs
genre_list_of_lists = [list for list in genre_list_of_lists if len(list) > 1]

# get a list of all unique genres
unique_genres = []
for x in genre_list_of_lists:
    for y in x:
        unique_genres.append(y)

# get a list of all pairs
genre_pairs_list = []
for x in genre_list_of_lists:
    genre_pairs_list.append(list(itertools.combinations(x,2)))

# flatten
genre_pairs_list = [item for sublist in genre_pairs_list for item in sublist]

# get unique pairs
unique_genre_pairs = list(set(genre_pairs_list))

# get a TIDY list of [genrea, genreb, count], while adding count from [genreb,genrea, count],
# then removing from search list
genre_pairs_count = []
for x in unique_genre_pairs:
    temp_count = genre_pairs_list.count(x)
    order_swap = (x[1], x[0])

    # add (genreb, genrea) count since undirected graph
    try:
        unique_genre_pairs.remove(order_swap)
        temp_count = temp_count + (genre_pairs_list.count(order_swap))
        #print('swap', order_swap, temp_count)
        print(len(unique_genre_pairs))
    except ValueError:
        #print('pass')
        pass
    genre_pairs_count.append([x[0],x[1],temp_count])

df_list = pd.DataFrame(genre_pairs_count, columns=['genrea','genreb','count'])
df_list.to_csv(output_path)

