import numpy as np
import pandas as pd

def UpperBound(df_input):
    """Function Description: input is a dataframe 
    with the type of 'data' above. It returns (DataFrame, float):
    DataFrame: a dataframe with the counts for female/male
    and a column classifying by majority vote
    and the error for that input type;
    float: the error of the classifier, which is the smallest
    error of any classifier on this data"""
    
    # Initialize list of genre sets and counts:
    genre_sets = [] # a list of the genre sets

    df = df_input.copy(deep = True)

    def set_id(row):
        if row.genre_set in genre_sets:
            row_id = genre_sets.index(row.genre_set)
        else:
            # add to list of all genre sets
            genre_sets.append(row.genre_set)
            row_id = genre_sets.index(row.genre_set)
        return row_id


    df['set_id'] = df.apply(set_id, axis = 1)
    
    df.reset_index(inplace = True)

    set_counts = pd.pivot_table(df, index = 'set_id', columns = 'gender', values = 'artist', aggfunc = 'count', fill_value = 0)
    set_counts['genre_set_encoded'] = set_counts.apply(lambda x: genre_sets[int(x.name)], axis = 1)
    set_counts['total'] = set_counts.female + set_counts.male
    set_counts = set_counts[['total','female','male','genre_set_encoded']]

    # Calculate a column that classifies by majority vote for each genre set
    def classify(row):
        if row.female < row.male:
            return 0 # male = 0
        else:
            return 1 # female = 1
    
    # indicate class
    set_counts['classifier'] = set_counts.apply(classify, axis = 1)
    
    # Create a column with the error of the classifier for that genre_set
    set_counts['error_bound'] = set_counts.apply(
        lambda x: x.female if x.classifier == 0 else x.male, axis = 1)
    
    # Calculate the total error of the model
    error = round(set_counts.error_bound.sum()/set_counts.shape[0],6)
    

    return set_counts, error