import requests
import logging

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
    { "Accept": "text/html", "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "en-US,en;q=0.9", "Host": "www.azlyrics.com", "Referer": "google.com", "Sec-Fetch-Dest": "document", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-Site": "cross-site", "Sec-Fetch-User": "?1", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36", "X-Amzn-Trace-Id": "Root=1-5f327f4c-6ca8b970f09beea0d0b56b90" },
    { "Accept": "text/html", "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "en-us", "Host": "www.azlyrics.com", "Referer": "google.com", "Sec-Fetch-Dest": "document", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-Site": "cross-site", "Sec-Fetch-User": "?1", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15", "X-Amzn-Trace-Id": "Root=1-5f328044-58866630ab424f84ab68dd5c" },
    { "Accept": "text/html", "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "en-US,en;q=0.5", "Host": "www.azlyrics.com", "Referer": "google.com", "Sec-Fetch-Dest": "document", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-Site": "cross-site", "Sec-Fetch-User": "?1", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:79.0) Gecko/20100101 Firefox/79.0", "X-Amzn-Trace-Id": "Root=1-5f32812d-afc8be488917a9ecf8473470" }
]


for i in headers_list[0:1]:
    try:
        response = requests.get(BASE + "lyrics/guidedbyvoices/landofdanger.html", headers=i)
        print(response)
    except Exception as e:
        print(str(i) + " header doesn't work")