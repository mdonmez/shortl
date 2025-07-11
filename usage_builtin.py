from shortl import Shortener

s = Shortener()

s.shorten("https://www.example.com", s.builtin_providers.isgd)
