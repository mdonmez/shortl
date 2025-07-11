import httpx
from typing import Callable


class Shortener:
    """
    Main interface for URL shortening. Includes built-in providers and supports custom ones.
    """

    _builtin_providers: dict[str, Callable] = {}
    _custom_providers: dict[str, Callable] = {}

    def __init__(self) -> None:
        self._register_builtin("isgd", self._isgd)
        self._register_builtin("tinyurl", self._tinyurl)
        self.builtin_providers = BuiltinProviders(self)

    def _register_builtin(self, name: str, func: Callable) -> None:
        self._builtin_providers[name] = func

    def list_builtins(self) -> list[str]:
        return list(self._builtin_providers.keys())

    def list_custom(self) -> list[str]:
        return list(self._custom_providers.keys())

    def shorten(self, url: str, provider: str | Callable) -> str:
        if isinstance(provider, str):
            return self._shorten_by_name(url, provider)
        elif callable(provider):
            return self._shorten_by_callable(url, provider)
        else:
            raise TypeError("Provider must be a string or a callable.")

    def _shorten_by_name(self, url: str, name: str) -> str:
        provider_map = {**self._builtin_providers, **self._custom_providers}
        if name not in provider_map:
            available = self.list_builtins() + self.list_custom()
            raise ValueError(f"Provider '{name}' not found. Available: {available}")

        func = provider_map[name]
        if not callable(func):
            raise TypeError(f"Provider '{name}' is not callable.")

        result = func(url)
        if not isinstance(result, str):
            raise TypeError(f"Provider '{name}' must return a string.")

        return result

    def _shorten_by_callable(self, url: str, func: Callable) -> str:
        result = func(url)
        if not isinstance(result, str):
            raise TypeError("Custom shortener function must return a string.")
        return result

    @staticmethod
    def _isgd(url: str) -> str:
        res = httpx.get(
            "https://is.gd/create.php", params={"format": "simple", "url": url}
        )
        return res.text.strip()

    @staticmethod
    def _tinyurl(url: str) -> str:
        res = httpx.get("https://tinyurl.com/api-create.php", params={"url": url})
        return res.text.strip()

    @classmethod
    def register_custom(cls, func: Callable) -> Callable:
        if not callable(func):
            raise TypeError("Custom shortener must be callable.")
        cls._custom_providers[func.__name__] = func
        return func

    class _ProviderNamespace:
        def __init__(self, providers: dict[str, Callable]):
            self._providers = providers

        def __getattr__(self, name: str) -> Callable:
            if name in self._providers:
                func = self._providers[name]
                if not callable(func):
                    raise TypeError(f"Provider '{name}' is not callable.")
                return func
            raise AttributeError(f"No such provider: {name}")

        def __dir__(self) -> list[str]:
            return list(self._providers.keys())


def custom_shortener(func: Callable) -> Callable:
    return Shortener.register_custom(func)


class BuiltinProviders:
    def __init__(self, shortener: Shortener) -> None:
        self.isgd = shortener._isgd
        self.tinyurl = shortener._tinyurl
