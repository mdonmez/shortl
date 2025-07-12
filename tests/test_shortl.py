import pytest
from shortl.shortl import Shortener, custom_shortener
import collections.abc


class TestProvidersList:
    """Tests for listing built-in and custom providers."""

    @pytest.fixture(autouse=True)
    def reset_providers(self) -> collections.abc.Generator[None, None, None]:
        Shortener._custom_providers.clear()
        Shortener._builtin_providers.clear()
        yield
        Shortener._custom_providers.clear()
        Shortener._builtin_providers.clear()

    @pytest.mark.parametrize("provider", ["isgd", "tinyurl"])
    def test_builtin_providers_listed(self, provider: str) -> None:
        s = Shortener()
        assert provider in s.list_builtins()

    def test_list_custom_empty(self) -> None:
        s = Shortener()
        assert s.list_custom() == []

    def test_register_and_list_custom(self) -> None:
        def myshort(url: str) -> str:
            return "short-" + url

        name = Shortener.register_custom(myshort)
        assert name == "myshort"
        s = Shortener()
        assert "myshort" in s.list_custom()

    def test_register_custom_from_code(self) -> None:
        code = """
def custom(url: str) -> str:
    return 'cstm-' + url
"""
        name = Shortener.register_custom(code)
        assert name == "custom"
        s = Shortener()
        assert "custom" in s.list_custom()


class TestCustomProviderDeletion:
    """Tests for deleting custom and built-in providers."""

    @pytest.fixture(autouse=True)
    def reset_custom(self) -> None:
        Shortener._custom_providers.clear()

    def test_delete_custom_success(self) -> None:
        def foo(url: str) -> str:
            return url

        Shortener.register_custom(foo)
        assert Shortener.delete_custom("foo") is True
        assert "foo" not in Shortener._custom_providers

    def test_delete_custom_not_found(self) -> None:
        assert Shortener.delete_custom("notfound") is False

    def test_delete_builtin_raises(self) -> None:
        Shortener()  # Ensure built-ins are registered
        with pytest.raises(TypeError):
            Shortener.delete_custom("isgd")


class TestShortenFunctionality:
    """Tests for the Shortener.shorten method and error handling."""

    @pytest.fixture(autouse=True)
    def reset_providers(self) -> collections.abc.Generator[None, None, None]:
        Shortener._custom_providers.clear()
        Shortener._builtin_providers.clear()
        yield
        Shortener._custom_providers.clear()
        Shortener._builtin_providers.clear()

    def test_shorten_by_name_and_callable(self, monkeypatch) -> None:
        s = Shortener()
        monkeypatch.setattr(s, "_isgd", lambda url: "short1")
        monkeypatch.setattr(s, "_tinyurl", lambda url: "short2")
        s._register_builtin("isgd", s._isgd)
        s._register_builtin("tinyurl", s._tinyurl)
        assert s.shorten("http://a.com", "isgd") == "short1"
        assert s.shorten("http://a.com", s._tinyurl) == "short2"

    def test_shorten_provider_not_found(self) -> None:
        s = Shortener()
        with pytest.raises(ValueError):
            s.shorten("http://a.com", "notfound")

    def test_shorten_provider_not_callable(self) -> None:
        s = Shortener()
        s._custom_providers["bad"] = 123
        with pytest.raises(TypeError):
            s.shorten("http://a.com", "bad")

    def test_shorten_callable_returns_non_str(self) -> None:
        def bad(url: str) -> int:
            return 123

        Shortener.register_custom(bad)
        s = Shortener()
        with pytest.raises(TypeError):
            s.shorten("http://a.com", "bad")


class TestCustomShortenerDecorator:
    """Tests for the @custom_shortener decorator."""

    def test_custom_shortener_decorator(self) -> None:
        @custom_shortener
        def dec(url: str) -> str:
            return "d-" + url

        assert "dec" in Shortener._custom_providers


class TestBuiltinProvidersNamespace:
    """Tests for the builtin_providers namespace."""

    def test_builtin_providers_namespace(self) -> None:
        assert callable(Shortener().builtin_providers.isgd)
        assert callable(Shortener().builtin_providers.tinyurl)
