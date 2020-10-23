import spotipy
import pandas as pd

# start API session
from spotipy.oauth2 import SpotifyClientCredentials

client_credentials_manager = SpotifyClientCredentials(client_id='',
                                                      client_secret='')

sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
sp.trace = False



def get_spotify_genres(x):
    result0 = sp.artist(x)

    try:
        artist_1_genre = result0['genres']
    except IndexError:
        artist_1_genre = ['Index Error None']

    return artist_1_genre

    wiki_url = 'https://en.wikipedia.org/wiki/'+str(name)
def get_wiki_genre(site_example):
    # OK, so first call wiki
    import requests
    import re
    from bs4 import BeautifulSoup as bs
    page = requests.get(site_example)

    # Then get the whole page content via BS lol
    soup = bs(page.content, 'html.parser')

    # Find the "Genres" header row thing of the side table thing ('table', class_="infobox biography vcard")
    genre_place = soup.find('th', scope="row", text="Genres")

    # Then get the cell next to the "Genres" cell
    genres_td = genre_place.find_next_siblings("td")

    """Not exactly sure how the beautifulsoup works here...but it gets the text of whatever's in the "Genres" cell"""
    # Some have hyperlinks to those genres, some do not.
    # So, there's some different ways the genre names are stored in the HTML
    genre_list = [text for text in genres_td[0].stripped_strings]
    #print('stripped_strings', genre_list)

    """Get rid of some extraneous values that pop in due to html inconsistencies"""
    # removes those with footnotes e.g., '[1]' in https://en.wikipedia.org/wiki/Rachel_Potter
    genre_list[:] = (value for value in genre_list if '[' not in value)

    # If there's NO links for the genres and genres > 1, split into a list since it's stored as a string
    # e.g., https://en.wikipedia.org/wiki/Katharina_Nuttall
    if ',' in str(genre_list) and len(genre_list) == 1:
        genre_list = genre_list[0].split(', ')

    # do some string cleaning here, basically
    # https://en.wikipedia.org/wiki/The_Scissor_Girls
    # https: // en.wikipedia.org / wiki / Stu_Davis
    genre_list[:] = (value for value in genre_list if value !='.')
    genre_list[:] = (value for value in genre_list if value != ',')
    genre_list[:] = (value for value in genre_list if value != '/')
    genre_list[:] = (value for value in genre_list if value != '•')
    genre_list[:] = (value for value in genre_list if value != ';')
    genre_list[:] = (value for value in genre_list if value != '(')
    genre_list[:] = (value for value in genre_list if value != ')')
    genre_list[:] = (value for value in genre_list if value != '.')

    # keep hyphenated genres UNLESS they are linked to separate genre-pages
    # e.g., 'https://en.wikipedia.org/wiki/Rachel_Carns'
    genre_list[:] = (value for value in genre_list if value != '-')

    # Get rid of any beginning or trailing spaces
    genre_list = [x.strip(' ') for x in genre_list]

    # Get rid of the odd semi-colon
    genre_list = [x.replace('; ', '') for x in genre_list]
    genre_list = [x.replace(';', '') for x in genre_list]

    # make all lowercase so doesn't matter if it's at the beginning
    genre_list = [x.lower() for x in genre_list]
    #print('*********final**********', genre_list)

    # Very occasional commas still in a list element, so get rid of those
    genre_list = [x.replace(',', '') for x in genre_list]


    return genre_list
"""
OLD wiki genres; gets ONLY hyperlinked genres, and gets the "Title:" from the <a> anchor tags
def get_wiki_genre(site_example):
    # OK, so first call wiki
    import requests
    import re
    from bs4 import BeautifulSoup as bs
    page = requests.get(site_example)

    # Then get the whole page content via BS lol
    soup = bs(page.content, 'html.parser')

    # Find the "Genres" header row thing of the side table thing ('table', class_="infobox biography vcard")
    genre_place = soup.find('th', scope="row", text="Genres")

    # Then get the cell next to the "Genres" cell
    genres_td = genre_place.find_next_siblings("td")

    # Then couldn't figure out how to get nested bits of HTML so just converted it to a string and started searching
    # The Genres are always(?) linked to other places on wiki, so they have a link, which is called by a title=""
    genre_match_list = []
    for m in re.finditer('title=".*?"', str(genres_td)):
        genre_titles = m.group()
        # print(genre_titles)
        genre_match_list.append(str(genre_titles))

    # basically get rid of excess string info stuff lol, make into neat list
    genre_list = []
    for x in genre_match_list:
        z = x[7:]
        y = z[:-1]
        genre_list.append(y)

    return genre_list
"""



