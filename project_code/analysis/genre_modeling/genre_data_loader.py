# imports
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import string


class LoadGenreData():
    """Load and prepreocess the genre label data.
    NOTE: "!" are removed from genre labels. This affects "oi!" and "cuidado!"
    Input:
    date: used for names of data files
    df_X: optional, X data as DF; overrides paths
    df_y: optional, y data as DF; overrides paths
    train and test data paths for X,y -- only used if DF is not provided
    """
    
    
    def __repr__(self):
        return "Data Frame {}".format(self.data.iloc[:3])

    def __str__(self):
        return "Data Frame {}".format(self.__repr__())
    
    
    def __init__(self, date, df_X = None, df_y = None, X_path_train = None, y_path_train = None, X_path_test = None, y_path_test = None):
    
        self.date = date
        
        if df_X  is not None:
            self.X = df_X
            self.y = df_y
        else:
            self.X_path_train = X_path_train
            self.y_path_train = y_path_train
            self.X_path_test = X_path_test
            self.y_path_test = y_path_test

            # import from CSV
            if X_path_test is None:
                self.X = pd.read_csv(self.X_path_train, index_col = ['artist'])
            else:
                self.X_train = pd.read_csv(self.X_path_train, index_col = ['artist'])
                self.X_test = pd.read_csv(self.X_path_test, index_col = ['artist'])
                self.X = pd.concat([self.X_train,self.X_test])

            if y_path_test is None:
                self.y = pd.read_csv(self.y_path_train, index_col = ['artist'])
            else:
                self.y_train = pd.read_csv(self.y_path_train, index_col = ['artist'])
                self.y_test = pd.read_csv(self.y_path_test, index_col = ['artist'])
                self.y = pd.concat([self.y_train,self.y_test])

        # assemble X,y into DF
        self.data = self.X.join(self.y, how = 'inner', on = 'artist')

    def data(self):
        return self.data
    

    def get_balanced_sample(self):
        data_fem = self.data[self.data.gender == 'female']
        data_mal = self.data[self.data.gender == 'male']
        fem_size = data_fem.shape[0]
        data_mal_sub = data_mal.sample(fem_size)
        data_sub = pd.concat([data_fem, data_mal_sub])
        data_sub.sample(frac = 1)
        return data_sub

    def as_sets(self):
        """Return view of data with genre labels in a set for each artist;
        'genrelist' column is not shown"""
        self.data['genre_set']= self.data['genrelist'].apply(to_sets)
        # remove old version of genre labels
        columns = self.data.columns.tolist()
        columns.remove('genrelist')
        #columns = pd.Index(columns)
        return self.data[columns]
    
    def as_lists(self):
        """Return view of data with genre labels in a list for each artist;
        'genrelist' column is not shown"""
        self.data['genre_list']= self.data['genrelist'].apply(to_lists)
        # remove old version of genre labels
        columns = self.data.columns.tolist()
        columns.remove('genrelist')
        #columns = pd.Index(columns)
        return self.data[columns]
    
    def as_strings(self):
        """Return view of data with genre labels as string for each artist;
        'genrelist' column is not shown"""
        self.data['genre_string']= self.data['genrelist'].apply(to_strings)
        # remove old version of genre labels
        columns = self.data.columns.tolist()
        columns.remove('genrelist')
        #columns = pd.Index(columns)
        return self.data[columns]
    
    # WARNING: don't add a column to self.X in this method; use a temp DF instead
    def get_list_of_genres(self):
        """Returns a sorted list of genres for the dataset provided to the instance."""
        self.X['genre_list']= self.X['genrelist'].apply(to_lists)
        self.list_of_genres = self.X['genre_list'].values.tolist()
        self.list_of_genres = [label for artists_labels in self.list_of_genres for label in artists_labels]
        self.list_of_genres = list(set(self.list_of_genres))
        self.list_of_genres.sort()
        return self.list_of_genres
    
    def get_sparse_X_vector(self):
        """Return X as a sparse vector with a 1 in the entry (row, id) if the artist has the label with id
        Notes on sparse vector commands: 
        To get the number of nonzero entries: X_sparse.nnz
        To get the nonzero entries of a row: X_sparse[n:m].nonzero() -- returns list of rows and columns with nonzero entries
        """
        dict_genre_to_id = self.get_dict_genre_to_id()
        vec = CountVectorizer(vocabulary = dict_genre_to_id) # uses scipy.sparse.csr_matrix representation
        self.data_genre_strings = self.as_strings()
        self.X_genre_string = self.data_genre_strings['genre_string']
        self.X_sparse = vec.fit_transform(self.X_genre_string)
        return self.X_sparse
    
    def get_dict_genre_to_id(self):
        """Return dictionary of the form {'label':id_number}
        """
        self.list_of_genres = self.get_list_of_genres()
        dict_genre_to_id = dict(zip(self.list_of_genres,range(len(self.list_of_genres))))
        return dict_genre_to_id
    
    def get_dict_id_to_genre(self):
        """Return dictionary of the form {id_number:'label'}
        """
        self.list_of_genres = self.get_list_of_genres()
        dict_genre_to_id = dict(zip(range(len(self.list_of_genres)),self.list_of_genres))
        return dict_genre_to_id
    
    def get_coo_matrix(self):
        """Return the (values, (rows, cols)) for a COO matrix
        of the genre sets"""
        self.as_lists()
        dict_gid = self.get_dict_genre_to_id()
        
        def coo_rows(row):
            """Get the row info for the COO sparse matrix
            version of the genre sets"""
            row = [self.data.index.get_loc(row.name) for genre in row.genre_list]
            return np.array(row)

        def coo_cols(row):
            """Get the col info for the COO sparse matrix
            version of the genre sets"""
            col = [dict_gid[genre] for genre in row.genre_list]
            return np.array(col)

        def coo_values(row):
            """Get the values info for the COO sparse matrix
            version of the genre sets"""
            values = [1 for genre in row.genre_list]
            return np.array(values)

        self.data['coorows'] = self.data.apply(coo_rows, axis = 1)
        self.data['coocols'] = self.data.apply(coo_cols, axis = 1)
        self.data['coovalues'] = self.data.apply(coo_values, axis = 1)

        rows = create_coo_list(self.data.coorows)
        cols = create_coo_list(self.data.coocols)
        values = create_coo_list(self.data.coovalues)

        coo_info = (values, (rows, cols))
        
        return coo_info
    

# Functions needed

def remove_punctuation_from_word(word):
    # remove '!'
    table = str.maketrans('', '', '!')
    stripped = word.translate(table) 
    print(stripped)

def to_strings(string):
    """This function takes in a string of the form
     appearing in the genrelist of the dataframe.
     It converts it to a list, then a set (to remove duplicates), and then a string."""
    string = string.strip("[").strip("]").replace("'","")
    L = [s for s in string.split(',')]
    L_new = []
    for x in L:
        L_new.append(x.replace(" ","_").lstrip("_").rstrip("_").strip("!").replace("+","_"))
    while (str("") in L_new):
        L_new.remove("")
    L_new = list(set(L_new))
    L_string = " ".join(L_new)
    return L_string


def to_sets(string):
    """This function takes in a string of the form
    appearing in the genrelist of the dataframe.
    It strips the square brackets and extra quotes and
    returns a set of strings where each string is a genre label."""
    string = string.strip("[").strip("]").replace("'","")
    L = [s for s in string.split(',')]
    L_new = []
    for x in L:
        L_new.append(x.replace(" ","_").lstrip("_").rstrip("_").strip("!").replace("+","_"))
    while (str("") in L_new):
        L_new.remove("")
    return set(L_new)


def to_lists(string):
    """This function takes in a string of the form
    appearing in the genrelist of the dataframe.
    It strips the square brackets and extra quotes and
    returns a list of strings where each string is a genre label."""
    string = string.strip("[").strip("]").replace("'","")
    L = [s for s in string.split(',')]
    L_new = []
    for x in L:
        L_new.append(x.replace(" ","_").lstrip("_").rstrip("_").strip("!").replace("+","_"))
    while (str("") in L_new):
        L_new.remove("")
    L_new = list(set(L_new))
    return L_new

# for getting a coo matrix

def create_coo_list(series):
    """turn series (column of df) whose values
    are numpy arrays into a list
    used as info for a coo matrix"""
    info = series.values.tolist()
    info = np.hstack(info)
    return info
