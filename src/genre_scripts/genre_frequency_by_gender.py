import pandas as pd
import numpy as np


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
    genre_frequency.index.name = "genre"
    genre_frequency.columns = ["frequency"]

    # convert index from id to genre
    genre_frequency.reset_index(inplace=True)
    genre_frequency["genre"] = genre_frequency.apply(lambda x: dictidg[x.genre], axis=1)
    genre_frequency.set_index(["genre"], inplace=True)

    # create gender masks
    MaskF = data.gender == "female"
    MaskF.reset_index(drop=True, inplace=True)
    MaskM = data.gender == "male"
    MaskM.reset_index(drop=True, inplace=True)

    # apply gender masks to sparse matrix
    X_f = X[MaskF.values, :]
    X_m = X[MaskM.values, :]

    # create frequency counts by gender
    FemFreq = X_f.sum(0)
    MalFreq = X_m.sum(0)

    # convert matrix to list
    FemFreq = [*FemFreq.flat]
    MalFreq = [*MalFreq.flat]

    # put lists into frequency dataframe
    genre_frequency["female"] = pd.Series(FemFreq, index=genre_frequency.index)
    genre_frequency["male"] = pd.Series(MalFreq, index=genre_frequency.index)

    genre_frequency.reset_index(inplace=True)

    return genre_frequency
