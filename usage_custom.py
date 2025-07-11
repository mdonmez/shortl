from shortl import Shortener, custom_shortener

s = Shortener()


@custom_shortener
def provider_example(url: str) -> str:
    return "https://custom.example/" + url


s.shorten("https://www.example.com", provider_example)
