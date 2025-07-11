import requests
from typing import Callable


class Shortener:
    """
    Main interface for URL shortening. Includes built-in providers and supports custom ones.
    """

    _builtin_providers: dict[str, Callable[[str], str]] = {}
    _custom_providers: dict[str, Callable[[str], str]] = {}

    def __init__(self) -> None:
        # Register built-in providers
        self._register_builtin("isgd", self._isgd)
        self._register_builtin("tinyurl", self._tinyurl)

    def _register_builtin(self, name: str, func: Callable[[str], str]) -> None:
        self._builtin_providers[name] = func

    def list_defaults(self) -> list[str]:
        """List names of built-in providers."""
        return list(self._builtin_providers.keys())

    def list_custom(self) -> list[str]:
        """List names of custom-registered providers."""
        return list(self._custom_providers.keys())

    def shorten(self, url: str, provider: str) -> str:
        """Shorten a URL using the specified provider (built-in or custom)."""
        if provider in self._builtin_providers:
            return self._builtin_providers[provider](url)
        if provider in self._custom_providers:
            return self._custom_providers[provider](url)
        raise ValueError(
            f"Provider '{provider}' not found. Available: {self.list_defaults() + self.list_custom()}"
        )

    @staticmethod
    def _isgd(url: str) -> str:
        res = requests.get(
            "https://is.gd/create.php", params={"format": "simple", "url": url}
        )
        return res.text.strip()

    @staticmethod
    def _tinyurl(url: str) -> str:
        res = requests.get("https://tinyurl.com/api-create.php", params={"url": url})
        return res.text.strip()

    @classmethod
    def register_custom(cls, func: Callable[[str], str]) -> Callable[[str], str]:
        """Register a custom shortener function by its name."""
        cls._custom_providers[func.__name__] = func
        return func


def custom_shortener(func: Callable[[str], str]) -> Callable[[str], str]:
    """Decorator to register a custom shortener function with the Shortener class."""
    return Shortener.register_custom(func)
