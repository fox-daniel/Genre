import numpy as np
np.random.seed(23)
import pandas as pd
import re
from datetime import datetime

# from my scripts
#from genre_scripts.genre_cleaning_individual_cases_1 import cleaning_individual_cases_1

def clean_genre_data():
    

    data = pd.read_csv('../../data/genre_lists/data_to_be_cleaned/wiki-kaggle_genres_rescrape.csv', header = 0)
    data.drop(['Unnamed: 0'], axis = 1, inplace = True)

    data['retrieved'] = data['retrieved'].replace('none', np.nan)

    data.dropna(axis = 0, inplace = True)

    # remove url prefix from retrieved values
    data['retrieved'] = data.retrieved.apply(retrieved_artist)

    # replace whitespace with underscore in artist columns
    data['artist'] = data.artist.apply(underscore)
    
    # remove designations from artists names in retrieved
    data['retrieved_clean'] = data.retrieved.apply(remove_designation)
    
    # find mismatches between artist and retrieved columns
    data['match'] = (data.artist.apply(lambda x: x.casefold())\
                     != data.retrieved_clean.apply(lambda x: x.casefold())).astype('int64')
    
    #remove artists with mismatch
    data = data[data.match == 0].copy(deep = True)
    
    # run this imported function to deal with individual cases
    data = cleaning_individual_cases_1(data)
    
    # respell genre labels
    data['genre_respell']= data['genre'].apply(GenreReSpelling)
    
    # clean labels and output a list of labels
    data['genrelist']= data['genre_respell'].apply(genrelist)
    
    # clean casses by hand
    data = cleaning_individual_cases_2(data)
    
    # create column with list lengths
    data['genrelist_length'] = data.genrelist.apply(lambda x: len(x))
    
    # remove artists with lists of length zero
    data = data[data.genrelist_length > 0]
    
    # remove bands (which can have multiple genders)
    data = data[~data.retrieved.str.contains('band')]
    
    # drop unnecessary columns
    data.drop(['retrieved','genre','retrieved_clean', 'match', 'genre_respell'], axis = 1, inplace = True)
    
    return data
    
# Functions called:

def retrieved_artist(text):
    """
    This function extracts artist name from the url.
    Apply it to the 'retrieved' values.
    """
    try:
        retrieved = text
        p = re.compile(r'(https://en.wikipedia.org/wiki/)(.*)')
        result = re.match(p, retrieved)
        return result.group(2)
    except:
        if text == 'none':
            return 'none'
    else:
        return 'None'
    

def underscore(text):
    """
    This function replaces white space in the values of
    the column artist with an underscore.
    """
    try:
        split_name = text.split(' ')
        return '_'.join(split_name)  
    except:
        return 'error'

def remove_designation(text):
    """
    This function uses re. to remove any parenthetical designations
    form the retrieved artist name
    """
    designations = [r'_\(singer\)', r'_\(musician\)', r'_\(rapper\)', r'_\(band\)', r'_\(composer\)', r'_\(music_producer\)', r'_\(singer-songwriter\)' ]
    x = text
    for des in designations:
        if re.search(des, x):
            x = re.sub(r'{}'.format(des),'',text)
    return x


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


def verify_artist(x,y):
    """This function takes a pair of strings and checks
    if they are equivalent (case insensitive). The method 
    .casefold is used to be case insensitive; 
    still might have problems on some characters"""
    if x.casefold() == y.casefold(): 
        return 1
    else:
        return 0
    
def GenreReSpelling(string):
    """
    This function respells genre labels to normalize spellings.
    It calls respell_dict which is below.
    """
    for key in respell_dict.keys():
        string = re.sub(key, respell_dict[key], string)
    return string


def genrelist(string):
    """This function takes in a string of the form
    appearing in the genrelist of the dataframe.
    It strips the square brackets and extra quotes and
    returns a list of strings where each string is a genre label.
    It also removes strings in parentheses and removes \( or \) that are isolated.
    It replaces 'singer/songwriter' with 'singer-songwriter' and replaces forward slashes with commas.
    """
    string = string.strip("[").strip("]").replace("'","").replace('"',"") \
    .replace("/",",").replace("·",",") \
    .replace(r";",",").replace(r"|",",").replace(u"\xa0",u" ")\
    .replace(u"\\xa0",u" ")\
    .replace(r"\n",",")
    L = [s for s in string.split(',')]
    L_new = []
    for x in L:
        x = re.sub(r"\(.*?\)", "", x) 
        x = re.sub(r"\(", "", x) 
        x = re.sub(r"\)", "", x) 
        x = re.sub(r":", "", x)
        x = re.sub(r"\.", "", x)
        x = re.sub(r"\]", "", x)
        x = re.sub(r"\[", "", x)
        x = x.replace(" ","_").lstrip("_").rstrip("_").lstrip("-").rstrip("-")
        x = re.sub(r"\band_{0,1}", "", x)
        x = re.sub(r"_music\b", "", x)
        x = re.sub(r"_musician\b", "", x)
        x = re.sub(r"_with\b", "", x)
        x = re.sub(r"-", "_", x)
        x = re.sub(r"\*","", x)
        L_new.append(x)
    while (str("") in L_new):
        L_new.remove("")
    return L_new

def cleaning_individual_cases_2(data):
    data.at[14654, 'genrelist'] = ['blues','soul','r&b','gospel','funk','folk','african_american']
    data.at[8471, 'genrelist'] = ['pop','hip_hop','r&b']
    data.at[2416,'genrelist'] = ['disco', 'funk', 'electric', 'latin_soul']
    data.at[7861,'genrelist'] = ['torch_song']
    data.at[7908,'genrelist'] = ['rock',
                                 'alternative_rock',
                                 'experimental',
                                 'mpb',
                                 'progressive_rock',
                                 'post_punk',
                                 'new_wave',
                                 'samba_rock']
    return data

# the dictionary needed to respell genre labels
respell_dict = {r'r & b': 'r&b', 
    r'rhythm\s{0,1}(and|&)\s{0,1}blues': 'rhythm&blues', 
    r'rhythm and grime': 'r&g', 
    r'rhythm & grime': 'r&g', 
    "electronic dance music": "edm",
    r'country\s{0,1}(and|&)\s{0,1}western':'country&western', 
    r"rock[\w. &''-]{0,5}roll":'rock&roll', 
    r"r.{0,1}n.{0,1}b":"r&b",
    r"hip.{0,1}hop":"hip-hop",
    r"hip.{0,1}house":"hip-house",
    r"adult":"",
    r"afrobeats":"afrobeat",
    r"boleros":"bolero",
    r"musicals":"musical",
    r"neo_souls":"neo_soul",
    r"protest_songs":"protest_song",
    r"spirituals":"spiritual",
    r"television_scores":"television_score",
    r"show tune":"show_tunes",
    r"showtunes":"show_tunes",
    r"showtunes adult contemporary": "show_tunes, adult_contemporary",
    r"ballad\b":"ballads",
    r"soundtracks":"soundtrack",
    r"afropop":"afro-pop",
    
    r"alt/rock":"alternative-rock",
    r"alt.\s{0,1}country":"alternative-country",
    r"\balt-":"alternative-",
    r"\balt\b":"alternative",
    r"alternative ":"alternative-",
    
    r"antifolk":"anti-folk",
    
    r"avant(-|\s)pop":"avant-garde_pop",
    r"avant-rock":"avant-garde_rock",
    r"avant-prog":"avant-garde_prog",
    r"avant\s{0,1}garde":"avant-garde",
    r"\bavant\s\b":"avant-garde",
    r"\bavant[^-]":"avant-garde",
    
    r"avantgarde":"avant-garde",
    
    r"balladeer":"ballads",
    r"bossanova":"bossa_nova",
    r"brazilian {0,1}music":"brazilian",
    r"broadway musicals{0,1}":"broadway",
    r"broadway music":"broadway",
    r"broadway theatre":"broadway",
    r"broadway theatre":"broadway",
    
    r"breton singing":"breton",
    r"canterbury scene":"canterbury_sound",
    r"chansonnier":"chanson",
    r"children.{0,2} songs":"childrens",
    r"chill-out":"chillout",
    r"christian and gospel":"christian, gospel",
    r"christian & gospel":"christian, gospel",
    
    r"citation needed":"",
    r"clarification needed":"",
    
    r"concerts":"concert",
    r"cpop":"c-pop",
    r"crooning":"crooner",
    r"darkwave":"dark_wave",
    r"downtempo":"down_tempo",
    r"dreampop":"dream_pop",
    r"drum\s{0,1}(and|&)\s{0,1}bass":"drum&bass",
    r"electroacoustic":"electro-acoustic",
    r"electropop":"electro pop",
    r"electro\s{0,1}pop\s{0,1}alternative\spop":"electro_pop, alternative_pop",
    r"electro-pop dance-rock":"electro_pop, dance_rock",
    r"electropunk":"electro_punk",
    r"experimental & brazilian jazz":"experimental, brazilian_jazz",
    r"expressionist":"expressionism",
    
    r"film scores":"film",
    r"film score":"film",
    r"film soundtrack":"film",
    
    r"fingerstyle_and_classical_guitar":"fingerstyle, classical_guitar",
    r"folk and country":"folk, country",
    r"folk rock folk pop":"folk_rock, folk_pop",
    
    r"free improv\b":"free_improvisation",
    r"freestyling":"freestyle",
    r"french variÃ©tÃ©":"french variety",
    r"french variété":"french variety",
    r"french varieties":"french variety",
    
    r"futurepop":"future_pop",
    r"gospel_and_gospel_blues":"gospel, gospel_blues",
    r"hard core":"hardcore",
    r"hawaii":"hawaiian",
    r"hymnal":"hymns",

    r"hip-hop_soulhip-hop, soul":"hip-hop, soul",
    r"indipop":"indie_pop",
    r"indiepop":"indie_pop",
    r"lo fi":"lo-fi",
    r"lofi":"lo-fi",
    r"mellow_&_acoustic_rock":"acoustic_rock",
    r"minimalist":"minimalism",
    r"mor":"middle_of_the_road",
    r"motown sound":"motown",
    
    r"music pop rock":"pop_rock",
    r"musical theater":"musical",
    r"musical theatre":"musical",
    r"musical theatre pop":"musical_pop",
    r"musicals":"musical",
    r"music-jewish liturgy":"jewish_liturgy",
    r"musique concrÃ¨te":"musique_concrete",
    r"musique concrÃ©te":"musique_concrete",
    r"musique concrète":"musique_concrete",
    r"musique concréte":"musique_concrete",
    
    r"neo souls": "neo_soul",
    r"neo-cla": "neocla",
    
    r"neofolk": "neo_folk",
    r"neo-prog\b": "neo-progressive_rock",
    r"prog.{0,1}rock": "progressive rock",
    r"neotraditionalist country": "neotraditional country",
    r"pacific northwest hip-hop": "pacific_northwest_hip-hop",
    r"\snorthwest hip-hop": "pacific_northwest_hip-hop",
    r"hip-hop music in the pacific northwest":"pacific_northwest_hip-hop",
    r"old-school": "old school",
    r"old school rap": "old_school_hip-hop",
    
    r"oldtime": "old-time",
    r"old-timey": "old-time",
    r"opera\s(&|and)\smusical theatre": "opera, musical",
    r"opera and comic opera": "opera, comic_opera",
    r"opera arias": "opera",
    r"operatic": "opera",

    r"pitbash jewish punk thrash opera": "jewish_punk, thrash, opera",
    r"pbr&b": "alternative r&b",
    r"pop  dance": "pop_dance",
    r"pop dance rock jazz": "pop, dance, rock, jazz",
    r"pop edm hip-hop": "pop, edm, hip-hop",
    r"pop folksinger songwriter": "pop_folk, singer-songwriter",
    r"pop rock dance": "pop, rock, dance",
    r"pop rock soul": "pop, rock, soul",
    r"pop traditional pop": "pop, traditional_pop",
    
    r"poprock": "pop_rock",
    r"backing": "",
    r"post ": "post-",
    r"powerpop": "power_pop",
    r"praise & worship": "praise&worship",
    r"protest songs": "protest song",
    r"proto punk": "proto-punk",
    r"protopunk": "proto-punk",
    r"singer[ -/]{0,1}songwriter": "singer-songwriter",
    
    r"psych ": "psychedelic ",
    r"psychedelia": "psychedelic",
    
    r"punk-{0,1}rock": "punk_rock",
    r"r&b soul dance": "r&b, soul, dance",
    r"reggae cultural influence": "reggae",
    r"revival punk psycho blues": "revival_punk, psycho_blues",
    r"rock&roll_americana_rhythm_and_blues_alternative": "rock&roll, americana, rhythm&blues, alternative",
    r"rock&roll blues": "rock&roll, blues",
    r"sea shanty": "sea_shanties",
    r"shoegazing": "shoe gaze",
    r"singer-songwriter rock": "singer-songwriter, rock",

    r"soundtracks": "soundtrack",
    r"spirituals": "spiritual",
    r"surreal humour": "surreal_humor",
    r"synthpop": "synth_pop",
    r"synthpunk": "synth_punk",
    r"television scores": "television_score",
    r"the motown sound": "the_motown_sound",
    r"theatre": "theater",
    r"theatre performer": "theater",
    
    r"torch singer": "torch",
    r"torch songs{0,1}": "torch",
    r"trad\b": "traditional",
    r"traditional irish early": "traditional_irish",
    r"trance-blues r&b": "trance-blues, r&b",
    r"various styles": "various",
    r"vaudevillian": "vaudeville",
    r"western movies": "western films",
    r"with": "",
    r"with electronics": "electronics",
    r"world music deep-house quiet storm": "world, deep-house, quiet_storm",
    r"world music folk world jazz": "world, folk, worl_jazz",
    r"worldbeat": "world_beat",
    r"yéyé": "yé-yé",
    r"yodelling": "yodeling",
    
    r"alternative.{0,1}rock.{0,1}garage.{0,1}rock": "alternative_rock,garage_rock",
    r"americana folk alternative country garage rock": "americana,folk, alternative_country,garage_rock",
    r"acoustic rock folk rock": "acoustic_rock,folk_rock",
    r"americana.{0,1}folk.{0,1}alternative.{0,1}country.{0,1}garage.{0,1}rock": "americana,folk,alternative_country,garage_rock",
    r"'blues soul r & b gospel funk folk', 'african american music'": "blues,soul,r&b,gospel,funk,folk,african_american",
    r"jazz funk bluegrass pop": "jazz,funk,bluegrass,pop",
    
    r" music\b": "",
    " songs": "",
    r"\bsinger[^- ]": "",
    r"_&_":"&",
    r"screwed & chopped":"screwed&chopped",
    r"struggle & protest": "struggle&protest",
    r'opera & musical':'opera&musical'}

