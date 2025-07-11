from shortl import Shortener

url = "https://www.example.com"
s = Shortener()

short = s.shorten(url, s.builtin_providers.isgd)
