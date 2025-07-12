import pytest
import sys
from pathlib import Path
import collections.abc

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from shortl import mcp_server
from shortl.shortl import Shortener


class TestCustomShortenerManagement:
    """Tests for creating and deleting custom shorteners via mcp_server."""

    @pytest.fixture(autouse=True)
    def reset_custom(self) -> None:
        Shortener._custom_providers.clear()

    def test_create_custom_shortener_from_code(self) -> None:
        code = """
def foo(url: str) -> str:
    return 'f-' + url
"""
        name = mcp_server.create_custom_shortener(code)
        assert name == "foo"
        assert "foo" in Shortener._custom_providers

    def test_delete_custom_provider_success(self) -> None:
        def bar(url: str) -> str:
            return url

        Shortener.register_custom(bar)
        assert mcp_server.delete_custom_provider("bar") is True
        assert "bar" not in Shortener._custom_providers

    def test_delete_custom_provider_not_found(self) -> None:
        assert mcp_server.delete_custom_provider("notfound") is False

    def test_delete_custom_provider_builtin_raises(self) -> None:
        with pytest.raises(TypeError):
            mcp_server.delete_custom_provider("isgd")


class TestProviderListing:
    """Tests for listing providers and their types via mcp_server."""

    @pytest.fixture(autouse=True)
    def reset_all(self) -> collections.abc.Generator[None, None, None]:
        Shortener._custom_providers.clear()
        Shortener._builtin_providers.clear()
        Shortener()
        yield
        Shortener._custom_providers.clear()
        Shortener._builtin_providers.clear()

    def test_list_providers_types(self) -> None:
        def custom(url: str) -> str:
            return url

        Shortener.register_custom(custom)
        providers = mcp_server.list_providers()
        names = {p["name"]: p["type"] for p in providers}
        assert "isgd" in names and names["isgd"] == "builtin"
        assert "tinyurl" in names and names["tinyurl"] == "builtin"
        assert "custom" in names and names["custom"] == "custom"


class TestShortenFunctionality:
    """Tests for shortening URLs via mcp_server and error handling."""

    @pytest.fixture(autouse=True)
    def reset_all(self) -> collections.abc.Generator[None, None, None]:
        Shortener._custom_providers.clear()
        Shortener._builtin_providers.clear()
        Shortener()
        yield
        Shortener._custom_providers.clear()
        Shortener._builtin_providers.clear()

    def test_shorten_builtin(self, monkeypatch) -> None:
        monkeypatch.setattr(mcp_server.shortener, "_isgd", lambda url: "shortx")
        mcp_server.shortener._register_builtin("isgd", mcp_server.shortener._isgd)
        result = mcp_server.shorten("http://a.com", "isgd")
        assert result == "shortx"

    def test_shorten_custom(self) -> None:
        def myshort(url: str) -> str:
            return "s-" + url

        Shortener.register_custom(myshort)
        result = mcp_server.shorten("http://b.com", "myshort")
        assert result == "s-http://b.com"

    def test_shorten_provider_not_found(self) -> None:
        with pytest.raises(ValueError):
            mcp_server.shorten("http://a.com", "notfound")

    def test_shorten_provider_type_error(self) -> None:
        Shortener._custom_providers["bad"] = 123
        with pytest.raises(TypeError):
            mcp_server.shorten("http://a.com", "bad")
