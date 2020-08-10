import requests
from bs4 import BeautifulSoup, Comment
from sqlalchemy import create_engine
import time
import random

from stem import Signal
from stem.control import Controller
from fake_useragent import UserAgent

BASE = "https://www.azlyrics.com/"
ARTIST_URL = BASE + "g/guidedbyvoices.html"

# create table songs (id SERIAL PRIMARY KEY, title varchar(255) NOT NULL, lyrics BYTEA NOT NULL);
DATABASE_URI = 'postgres://postgres:password@localhost:5432/postgres'
INSERT_STATEMENT = "INSERT INTO songs (title, lyrics) VALUES (E\'{}\', E\'{}\');"

engine = create_engine(DATABASE_URI)

SCRAPE_PROXY = 'socks5://127.0.0.1:9050'

def song_url(song_path):
    return BASE + song_path[2:]

def fetch_song_lyrics(song_path):
    with Controller.from_port(port=9051) as c:
                c.authenticate()
                c.signal(Signal.NEWNYM)
    proxies = {'http': SCRAPE_PROXY, 'https': SCRAPE_PROXY}
    headers = {'User-Agent': UserAgent().random}
    song_page = requests.get(song_url(song_path), proxies=proxies, headers=headers)
    song_soup = BeautifulSoup(song_page.content, 'html.parser')
    lyrics_section = song_soup.find('div', class_='ringtone').find_next_sibling('div')
    for line in lyrics_section(text=lambda text: isinstance(text, Comment)):
        line.extract()
    return lyrics_section.get_text().replace("'", "\\'")

artist_page = requests.get(ARTIST_URL)

# div with class album -> text value contains the album name
# list items are divs with class listalbum-item

artist_soup = BeautifulSoup(artist_page.content, 'html.parser')
album_list = artist_soup.find(id='listAlbum')

# grab all songs from artist page

song_elements = album_list.find_all('div', class_='listalbum-item')

# iterate over songs
for song in song_elements:
    time.sleep(random.randint(1,5))
    title = song.get_text().replace("'", "\\'")
    lyrics = fetch_song_lyrics(song.find('a')['href'])
    engine.execute(INSERT_STATEMENT.format(title, lyrics))


# next steps:
# write songs to local db
# start scraping site to collect
# check results
# start feeding db into neural network