import requests
from bs4 import BeautifulSoup, Comment
from sqlalchemy import create_engine
import time
import random

from stem import Signal
from stem.control import Controller

BASE = "https://www.azlyrics.com/"
ARTIST_URL = BASE + "g/guidedbyvoices.html"

# drop table songs;
# create table songs (id SERIAL PRIMARY KEY, title varchar(255) NOT NULL, lyrics text NOT NULL);
DATABASE_URI = 'postgres://postgres:password@localhost:5432/postgres'
INSERT_STATEMENT = "INSERT INTO songs (title, lyrics) VALUES (E\'{}\', E\'{}\');"

engine = create_engine(DATABASE_URI)

SCRAPE_RETRIES_AMOUNT = 5
SCRAPE_PROXY = 'socks5://127.0.0.1:9050'

headers_list = [
    { "Accept": "text/html", "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "en-US,en;q=0.9", "Host": "www.azlyrics.com", "Referer": "google.com", "Sec-Fetch-Dest": "document", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-Site": "cross-site", "Sec-Fetch-User": "?1", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36", "X-Amzn-Trace-Id": "Root=1-5f327f4c-6ca8b970f09beea0d0b56b90" },
    { "Accept": "text/html", "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "en-us", "Host": "www.azlyrics.com", "Referer": "google.com", "Sec-Fetch-Dest": "document", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-Site": "cross-site", "Sec-Fetch-User": "?1", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15", "X-Amzn-Trace-Id": "Root=1-5f328044-58866630ab424f84ab68dd5c" },
    { "Accept": "text/html", "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "en-US,en;q=0.5", "Host": "www.azlyrics.com", "Referer": "google.com", "Sec-Fetch-Dest": "document", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-Site": "cross-site", "Sec-Fetch-User": "?1", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:79.0) Gecko/20100101 Firefox/79.0", "X-Amzn-Trace-Id": "Root=1-5f32812d-afc8be488917a9ecf8473470" }
]

def song_url(song_path):
    return BASE + song_path[2:]

# need to try with tor for new ip addresses...
def fetch_song_lyrics(song_path):
    for i in range(0, SCRAPE_RETRIES_AMOUNT):
        time.sleep(random.randint(1,5))
        try:
            with Controller.from_port(port=9051) as c:
                c.authenticate()
                c.signal(Signal.NEWNYM)
            proxies = {'http': SCRAPE_PROXY, 'https': SCRAPE_PROXY}
            headers = random.choice(headers_list)
            song_page_response = requests.get(song_url(song_path), proxies=proxies, headers=headers)
            assert song_page_response.ok
            song_soup = BeautifulSoup(song_page_response.content, 'html.parser')
            lyrics_section = song_soup.find('div', class_='ringtone').find_next_sibling('div')
            for line in lyrics_section(text=lambda text: isinstance(text, Comment)):
                line.extract()
            return lyrics_section.get_text().replace("'", "\\'").replace("\r","")
        except Exception as e:
            if i == SCRAPE_RETRIES_AMOUNT - 1:
                print(f'Unable to retrieve HTML from {song_path}: {e}')
    return None

artist_page = requests.get(ARTIST_URL)

# div with class album -> text value contains the album name
# list items are divs with class listalbum-item

artist_soup = BeautifulSoup(artist_page.content, 'html.parser')
album_list = artist_soup.find(id='listAlbum')

# grab all songs from artist page

song_elements = album_list.find_all('div', class_='listalbum-item')

# iterate over songs
for song in song_elements[0:5]:
    title = song.get_text().replace("'", "\\'")
    lyrics = fetch_song_lyrics(song.find('a')['href'])
    engine.execute(INSERT_STATEMENT.format(title, lyrics))


# next steps:
# write songs to local db
# start scraping site to collect
# check results
# start feeding db into neural network