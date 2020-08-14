import requests
import logging

from stem import Signal
from stem.control import Controller


try:
    import http.client as http_client
except ImportError:
    # Python 2
    import httplib as http_client
http_client.HTTPConnection.debuglevel = 1

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True

BASE = "https://www.azlyrics.com/"
ARTIST_URL = BASE + "g/guidedbyvoices.html"

headers_list = [
    { "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "en-US,en;q=0.9", "Cache-Control": "max-age=0", "Connection": "keep-alive", "Host": "www.azlyrics.com", "Referer": "https://www.azlyrics.com/g/guidedbyvoices.html", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36" },
    { "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "en-us", "Cache-Control": "max-age=0", "Connection": "keep-alive", "Host": "www.azlyrics.com", "Referer": "https://www.azlyrics.com/g/guidedbyvoices.html", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15"},
    { "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "en-US,en;q=0.5", "Cache-Control": "max-age=0", "Connection": "keep-alive", "Host": "www.azlyrics.com", "Referer": "https://www.azlyrics.com/g/guidedbyvoices.html", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:79.0) Gecko/20100101 Firefox/79.0" }
]

SCRAPE_PROXY = 'socks5://127.0.0.1:9050'

for i in headers_list[0:1]:
    try:
        with Controller.from_port(port=9051) as c:
            c.authenticate()
            c.signal(Signal.NEWNYM)
        proxies = {'http': SCRAPE_PROXY, 'https': SCRAPE_PROXY}
        # song_page_response = requests.get(song_url(song_path), proxies=proxies, headers=headers)
        response = requests.get(BASE + "lyrics/guidedbyvoices/landofdanger.html", proxies=proxies, headers=i)
        print(response)
    except Exception as e:
        print(e)
        print(str(i) + " header doesn't work")