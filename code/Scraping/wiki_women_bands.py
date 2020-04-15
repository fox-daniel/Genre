"""

List, manually copy/pasted from wikipedia

https://en.wikipedia.org/wiki/List_of_all-female_bands

"""

import pandas as pd
from genre_functions import *
from spotify_functions import get_artist_id, get_artist_name
import requests

filename_to_write = 'C:\TomTests\daniel_project\\wiki_bands_women.csv'

artist_list = ["The 5,6,7,8's", '21st Century Girls', '7 Year Bitch', "The Ace of Cups", "The Aces", "Adickdid", "Audrey", "Afrirampo", "Ajaqa", "Aldious", "The All Girl Summer Fun Band", "Aly & AJ", "American Girls", "Amiina", "The Amorettes", "Androids of Mu", "Antigone Rising", "Aphasia", "The Applicators", "Au Revoir SimoneThe Aquanettas", "Ars Nova", "Arven", "Astarte", "Autoclave", "Azure Ray", "Babes in Toyland", "Baby in Vain", "Band-Maid", "The Bangles", "BarlowGirl", "BeBe K'Roche", "The Be Good Tanyas", "Bellatrix", "Bella Tromba", "The Belle Stars", "Betty Blowtorch", "Betty Boop", "Big Joanie", "Big Trouble", "Birtha", "The Black Belles", "Blaxy Girls", "Blue Rose", "Bleach03", "The Bodysnatchers", "Bond", "Boye", "Bones Apart", "Bratmobile", "Broadzilla", "The Butchies", "Cacadou Look", "Cadallaca", "Celtic WomanCake Like", "Calamity Jane", "Calamity Jane", "Candy", "Care Bears on Fire", "Chai", "Chalk Circle", "ChatmonchyCherri Bomb", "Cherry BoomThe Capricorns", "Chicks on SpeedChildbirth", "Chocolate, Menta, Mastik", "Cibo Matto", "Cimorelli", "Civet", "Client", "The Coathangers", "Cobra", "Cobra Killer", "", "CocoRosie", "Cookie Crew", "The Continental Co-ets", "", "The Contractions", "Conquer DivideCowboy Crush", "Coyote Sisters", "Crucified Barbara", "Cub", "Cyntia", "Cypher in the Snow", "Daddy Issues", "The Daisy Chain", "The Deadly Nightshade", "", "Dead Disco", "The Devotchkas", "Dickless", "Dixie Chicks", "Dog Party", "Doll Skin", "Dolly Mixture", "The Donnas", "Drain STH", "Dream Nails", "Dum Dum Girls", "Electrelane", "Emily's Sassy Lime", "Erase Errata", "Everlife", "eX-Girl", "Ex-Hex", "Exist Trace", "The Eyeliners", "Fabulous Disaster", "The Faders", "Fanny", "The Feminine Complex", "Femme Fatale", "Fifth Column", "Finally Punk", "Fire Party", "First Aid Kit", "Fluffy", "Flying Lesbians", "Frau", "Free Kitten", "Frightwig", "Gacharic Spin", "Gallhammer", "Girlpool", "The Girls", "Girlschool", "Girl in a Coma", "Girl Monstar", "Gito Gito Hustler", "Go Betty Go", "Go-Bang's", "Gore Gore Girls", "The Go-Go's", "The Gymslips", "Halo Friendlies", "Hang On The Box", "Harry Crews", "Thee Headcoatees", "The Heart Beats", "Heavens to Betsy", "Hepburn", "Hijas de Violencia", "Hinds", "The Holy Sisters of the Gaga Dada", "Honeyblood", "Indica", "Indigo Girls", "International Sweethearts of Rhythm", "Isis", "Ivy Benson All Girls Band", "Ivy Lies", "Jack Off Jill", "The Jades", "Jale", "Junkyard Lipstick", "Katzenjammer", "Kitten Forever", "Kittie", "Kleenex", "Klymaxx", "Kostars", "KSM", "The Kut", "Lash", "Le Tigre", "Lesbians On Ecstasy", "The Like", "LiLiPUT", "L7LiveOnRelease", "The Liverbirds", "Lolita No. 18", "Look Blue Go Purple", "The Lounge Kittens", "Lovendor", "Lovebites", "Lunachicks", "Lungleg", "Luscious Jackson", "Luv'd Ones", "M2M", "Madam X", "Magneta Lane", "Mambo Taxi", "Maow", "Marine Girls", "Marsheaux", "Mary's Blood", "Melt Banana", "The Micragirls", "Mika Miko", "The Mo-dettes", "Mrs. Fun", "The Murmurs", "MT-TV", "Nice Horse", "Nisennenmondai", "Northern State", "Nots", "Octavia Sperati", "OOIOO", "Oreskaband", "The Organ", "Otoboke Beaver", "The Pack A.D.", "The Pandoras", "Peaness", "Partyline", "Phantom Blue", "The Pierces", "PINS", "Plastiscines", "The Pleasure Seekers and Cradle", "Plumtree", "Poison Dollys", "Pony Up", "Poussez Posse", "Precious Metal", "The Prettiots", "Princess Princess", "The Priscillas", "Pussy Riot", "Rachel Rachel", "The Raincoats", "Rasputina", "Razika", "", "Rebecca & Fiona", "Red Aunts", "Red Bacteria Vacuum", "Red Molly", "Red Poppy", "Rock Goddess", "The Runaways", "Sahara Hotnights", "Salem 66", "Savages", "Scandal", "Scarlet", "Scissor Girls", "Scrawl", "Screamin' Sirens", "September Girls", "Shampoo", "The Shaggs", "She Devils", "She Rockers", "The She Trinity", "Shonen Knife", "Show-Ya", "Sick of Sarah", "Sidi Bou Said", "Silent Siren", "Skating Polly", "Skinned Teen", "Skinny Girl Diet", "Skulker", "Slant 6", "Sleater-Kinney", "The Slits", "Smoosh", "Snatch", "Some Girls", "The Spazzys", "Spice Girls", "Spires That in the Sunset Rise", "Spitboy", "Splendora", "The Staves", "Stealing Sheep", "Stereopony", "Strawberry Switchblade", "Super Junky Monkey", "Supercute!", "Super Heroines", "Stonefield", "Switchblade Symphony", "TCR", "Tattle Tale", "Team Dresch", "Tegan and Sara", "The Third Sex", "Thunderbugs", "Thunderpussy", "The Trashwomen", "Those Dancing Days", "Thug Murder", "Tijuana Sweetheart", "Tiktak", "Tribe 8", "The Tuts", "Twelve Girls Band, Traditional", "Two Nice Girls", "Ut", "Uh Huh Her", "Uncle Earl", "Urban Symphony", "Upset", "Vanilla Ninja", "Vivian Girls", "Vixen", "Von Iva", "Voodoo Queens", "Vulpes", "The Wailin' Jennys", "The Warning", "Warpaint", "We've Got a Fuzzbox and We're Gonna Use It", "Whiteberry", "The Whoreshoes", "Wild Flag", "Wild Rose", "The Wimmins' Institute", "Wishing Chair", "Y Pants", "Zelda", "Zone"]
artist_list = list(set(artist_list))

df1=pd.DataFrame(artist_list,columns=['artist'])
genre_list = []
artist_result_list = []
gender_list = []

for x in artist_list:
    print(x)
    temp_uri = get_artist_id(x)
    if temp_uri == "No URI":
        genre_list.append('none')
        artist_result_list.append('none')
        gender_list.append('none')
        
    else:
        genre_list.append(get_spotify_genres(temp_uri))
        artist_result_list.append((get_artist_name(temp_uri)))
        gender_list.append('female')

df1['retrieved'] = artist_result_list
df1['gender'] = gender_list
df1['genre'] = genre_list

df1.to_csv(filename_to_write)



