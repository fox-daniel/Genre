"""

Visualization Chord Testing
From https://github.com/shahinrostami/chord

Begun 5/22/2020
Tom Johnson

6/02/2020 7:30p
1) Reads in a tidy edge-list with cols = [genrea,genreb,count]
2) turns that into a sparse matrix (eventually into list_of_lists)
3) outputs interactive chord for n most common genres.


"""

import chord
import pandas as pd
import numpy as np
from scipy.sparse import coo_matrix


# set number of top genre_pairs to visualize
n = 50

# set input and outputs
input_path = "C:\TomTests\daniel_project\genre_edges_list_wiki_corpus_full.csv"
output_path = 'chord_full_corpus_n' + str(n) + '.html'

# read in csv_file
df_list = pd.read_csv(input_path)

# read in n most common cols
genrea_col = df_list.nlargest(n, 'count')['genrea'].tolist()
genreb_col = df_list.nlargest(n, 'count')['genreb'].tolist()
count_col = df_list.nlargest(n, 'count')['count'].tolist()

# make a list of all genres
top_genres_list = genrea_col + genreb_col
top_genres_list = list(set(top_genres_list))
n_genres = len(top_genres_list)

# make an index for each member of genre list, so can "store" into sparse matrix list of lists
genre_label_dict = {}
i = 0
while i < len(top_genres_list):
    genre_label_dict[top_genres_list[i]] = i
    i = i + 1

# OK so now build "rows"
row = []
for x in genrea_col:
    row.append(genre_label_dict[x])

col = []
for x in genreb_col:
    col.append(genre_label_dict[x])

# from scipy documentation: Constructing a matrix using ijv format; make symmetrical!
array_row = np.array(row + col)
array_col = np.array(col + row)
data = np.array(count_col + count_col)
coo_mat = coo_matrix((data, (array_row, array_col)), shape=(n_genres, n_genres)).toarray()
# coo_mat = np.divide(coo_mat,100) # scaling if makes chord more legible

# then put into list of lists
matrix = coo_mat.tolist()
names = list(genre_label_dict.keys())

# NOW ready to put into the Chord maker!
chord.Chord(matrix, names,
            wrap_labels=False,
            colors="d3.schemeAccent",
            padding=.01,  # padding is amount of space between genres on edge
            width=700,  # width is diameter of whole wheel i think
            margin=0).to_html(output_path)

"""George Floyd and Breonna Taylor and Ahmaud Arbery, and...and...and..."""

