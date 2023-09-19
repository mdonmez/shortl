#!/usr/bin/python3
import requests
import clipboard

class Shortener:
    def __init__(self):
        self.api_url = "http://tinyurl.com/api-create.php"

    def shorten_url(self, url):
        query_params = {"url": url}
        response = requests.get(self.api_url, params=query_params)
        return response.text

class URL:
    def __init__(self, long_url):
        self.long_url = long_url

    def add_https(self):
        if not self.long_url.startswith("http://") and not self.long_url.startswith("https://"):
            self.long_url = "https://" + self.long_url

    def remove_unwanted_characters(self):        
        self.long_url = self.long_url.strip('"')
        self.long_url = self.long_url.strip("'")
        self.long_url = self.long_url.strip(" ")

class Shortl:
    def __init__(self):
        self.shortener = Shortener()

    def shorten(self, long_url, copy=False):
        url = URL(long_url)
        url.add_https()
        url.remove_unwanted_characters()
        short_url = self.shortener.shorten_url(url.long_url)
        if copy:
            clipboard.copy(short_url)
        return short_url