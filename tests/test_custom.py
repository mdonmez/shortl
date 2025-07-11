import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from shortl import Shortener, custom_shortener

url: str = "https://www.example.com"


def test_shorten_custom_provider() -> None:
    s: Shortener = Shortener()

    @custom_shortener
    def provider_example(url: str) -> str:
        return "https://custom.example/" + url

    expected_short_url: str = "https://custom.example/https://www.example.com"
    short: str = s.shorten(url, provider_example)
    assert short == expected_short_url
