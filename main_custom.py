from shortl import Shortener, custom_shortener

url = "https://www.example.com"
s = Shortener()


@custom_shortener
def provider_example(url: str) -> str:
    return "https://custom.example/" + url


short = s.shorten(url, provider_example)
