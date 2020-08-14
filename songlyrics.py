import requests
from bs4 import BeautifulSoup, Comment
from sqlalchemy import create_engine
import time
import random

BASE = "https://www.songlyrics.com/"
ARTIST_URL = BASE + "guided-by-voices-lyrics/"

# drop table songs;
# create table songs (id SERIAL PRIMARY KEY, title varchar(255) NOT NULL, lyrics text NOT NULL);
DATABASE_URI = 'postgres://postgres:password@localhost:5432/postgres'
INSERT_STATEMENT = "INSERT INTO songs (title, lyrics) VALUES (E\'{}\', E\'{}\');"

engine = create_engine(DATABASE_URI)


headers_list = [
    { "Accept": "text/html", "Accept-Encoding": "gzip", "Accept-Language": "en-US,en;q=0.9", "Host": "www.songlyrics.com", "Referer": "google.com",  "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36" },
    { "Accept": "text/html", "Accept-Encoding": "gzip", "Accept-Language": "en-us", "Host": "www.songlyrics.com", "Referer": "google.com",  "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15" },
    { "Accept": "text/html", "Accept-Encoding": "gzip", "Accept-Language": "en-US,en;q=0.5", "Host": "www.songlyrics.com", "Referer": "google.com",  "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:79.0) Gecko/20100101 Firefox/79.0" }
]

# need to try with tor for new ip addresses...
def fetch_song_lyrics(song_url):
    try:
        headers = random.choice(headers_list)
        song_page_response = requests.get(song_url, headers=headers)
        assert song_page_response.ok
        song_soup = BeautifulSoup(song_page_response.content, features='html.parser')
        lyrics_section = song_soup.find(id='songLyricsDiv')
        for line in lyrics_section(text=lambda text: isinstance(text, Comment)):
            line.extract()
        return lyrics_section.get_text().replace("'", "\\'").replace("\r","")
    except Exception as e:
        # if i == SCRAPE_RETRIES_AMOUNT - 1:
        print(f'Unable to retrieve HTML from {song_url}: {e}')
    return None

artist_page = requests.get(ARTIST_URL)

# div with class album -> text value contains the album name
# list items are divs with class listalbum-item

artist_soup = BeautifulSoup(artist_page.content, 'html.parser')
tracks = artist_soup.find('table', class_='tracklist').find('tbody').find_all('tr')

# grab all songs from artist page

# iterate over songs
for track in tracks:
    song = track.find('a')
    title = song.get_text().replace("'", "\\'")
    lyrics = fetch_song_lyrics(song['href'])
    engine.execute(INSERT_STATEMENT.format(title, lyrics))


# next steps:
# write songs to local db
# start scraping site to collect
# check results
# start feeding db into neural network