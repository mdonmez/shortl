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
    def register_custom(
        cls, func_or_code: str | Callable, name: str | None = None
    ) -> str:
        """
        Register a custom provider.
        - If func_or_code is a callable, registers it under its __name__ or the provided name.
        - If func_or_code is a string (function code), executes it and registers the first callable found under the provided name.
        Returns the provider name.
        """
        if callable(func_or_code):
            func = func_or_code
            provider_name = name if name is not None else func.__name__
        elif isinstance(func_or_code, str):
            if not name:
                raise ValueError(
                    "A name must be provided when registering from function code."
                )
            local_ns: dict = {}
            exec(func_or_code, {}, local_ns)
            func = None
            for v in local_ns.values():
                if callable(v):
                    func = v
                    break
            if func is None:
                raise ValueError("No callable found in function_code.")
            provider_name = name
        else:
            raise TypeError(
                "func_or_code must be a callable or a string of function code."
            )
        cls._custom_providers[provider_name] = func
        return provider_name

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
