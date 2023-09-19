import requests
from bs4 import BeautifulSoup
import json
from tenacity import retry, stop_after_attempt

URL = "https://www.webtoons.com/en/slice-of-life/yumi-cell/list?title_no=478"

class Scrape:
    def __init__(self) -> None:
        self.session = requests.Session()
        self.url = URL

