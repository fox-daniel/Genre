import numpy as np
np.random.seed(23)
import pandas as pd
import re
from datetime import datetime

# indices are loc

def cleaning_individual_cases_1(data):
    data.genre.at[6650] = "['ambient pop', 'folktronica', 'indietronica', 'indie folk']"
    data.genre.at[17600] = "['alternative rock', 'alternative metal', 'nu metal', 'gothic metal']"
    data.genre.at[11961] = "['celticana']"
    data.genre.at[13278] = "['pop', 'house music']"
    data.genre.at[15232] = "['pop', 'rock', 'folk-rock', rock-electronic, ballad']"
    data.genre.at[15556] = "['cajun', 'country', ' hillbilly, rockabilly, r&b']"
    data.genre.at[11935] = '[rock, active rock, country, jazz standards, childrens folk]'
    data.at[13009, 'genre'] = "['punk rock', 'art rock', 'jewish rock', 'garage punk', 'obscuro', 'metal','marching band', 'jewish music', 'jazz',  'pitbash', 'jewish punk', 'thrash', 'opera']"
    data.at[11170,'genre'] = "['aor', 'pop_rock', 'pop', 'disco', 'soul']"
    data.at[3535,'genre'] = "['praise&worship']"
    data.at[22536, 'genre'] = "['observational', 'blue comedy', 'musical_comedy']"
    data.at[12183, 'genre'] = "['jazz', 'blues', 'jump_blues', 'rock']"
    data.at[9679, 'genre'] = "['singer-songwriter', 'world beat', 'alternative pop', 'lounge', 'electronic', 'world music', 'indie pop', 'j-synth', 'cool jazz', 'fusion', 'electro-pop']"
    data.at[2374, 'genre'] = "['blues', 'ballads', 'rock&roll']"
    data.at[7946, 'genre'] = "['dancehall', 'reggae fusion', 'eurodance']"
    data.at[12500, 'genre'] = "['classical', 'folk']"
    data.at[9732, 'genre'] = "['pop', 'r&b', ' electropop', 'alternative pop']"
    data.at[19082, 'genre'] = "['pop', 'r&b', ' electropop', 'alternative pop']"
    data.at[3843, 'genre'] = "['gospel','gospel blues']"
    data.at[17494, 'genre'] = "['lo-fi','diy','indie','popcore', 'beat poetry']"
    data.at[10414, 'genre'] = "['cabaret', 'pop', 'contemporary opera']"
    data.at[14600, 'genre'] = "['rock', 'pop', 'jazz', 'r&b', 'country', ' blues', 'roots']"
    data.at[10022, 'genre'] = "['indie','alternative rock', 'pop punk']"
    data.at[13433, 'genre'] = "['blues', 'roots', ' rock&roll', 'americana', 'rhythm&blues', 'alternative']"
    data.at[2295, 'genre'] = "['r&b', ' jazz', 'funk', 'rock']"
    data.at[3017, 'genre'] = "['jazz fusion', 'jazz funk', 'bluegrass pop']"
    data.at[18667, 'genre'] = "['jazz', 'latin-jazz', 'pop']"
    data.at[8968, 'genre'] = "['rock', 'folk_rock', 'alternative_rock', 'acoustic_rock', 'reggae']"
    
    return data