import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from shortl import Shortener

import httpx

url: str = "https://www.example.com"


def test_shorten_isgd(monkeypatch) -> None:
    s: Shortener = Shortener()
    expected_short_url: str = "https://is.gd/abc123"

    def mock_get(url_: str, params: dict) -> httpx.Response:
        return httpx.Response(
            200, text=expected_short_url, request=httpx.Request("GET", url_)
        )

    monkeypatch.setattr(httpx, "get", mock_get)
    short: str = s.shorten(url, s.builtin_providers.isgd)
    assert short == expected_short_url
