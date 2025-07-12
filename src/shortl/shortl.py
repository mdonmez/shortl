import httpx


class Shortener:
    """
    Main interface for URL shortening. Includes built-in providers and supports custom ones.
    This is the SDK class and does not depend on MCP or any server logic.
    """

    _builtin_providers: dict[str, object] = {}
    _custom_providers: dict[str, object] = {}

    def __init__(self) -> None:
        self._register_builtin("isgd", self._isgd)
        self._register_builtin("tinyurl", self._tinyurl)
        self.builtin_providers = BuiltinProviders(self)

    def _register_builtin(self, name: str, func: object) -> None:
        self._builtin_providers[name] = func

    def list_builtins(self) -> list[str]:
        return list(self._builtin_providers.keys())

    def list_custom(self) -> list[str]:
        return list(self._custom_providers.keys())

    def shorten(self, url: str, provider: str | object) -> str:
        match provider:
            case str():
                return self._shorten_by_name(url, provider)
            case _ if callable(provider):
                return self._shorten_by_callable(url, provider)
            case _:
                raise TypeError("Provider must be a string or a callable.")

    def _shorten_by_name(self, url: str, name: str) -> str:
        provider_map: dict[str, object] = {
            **self._builtin_providers,
            **self._custom_providers,
        }
        if name not in provider_map:
            available: list[str] = self.list_builtins() + self.list_custom()
            raise ValueError(f"Provider '{name}' not found. Available: {available}")
        func_obj: object = provider_map[name]
        if not callable(func_obj):
            raise TypeError(f"Provider '{name}' is not callable.")
        result = func_obj(url)
        if not isinstance(result, str):
            raise TypeError(f"Provider '{name}' must return a string.")
        return result

    def _shorten_by_callable(self, url: str, func: object) -> str:
        if not callable(func):
            raise TypeError("Custom shortener function must be callable.")
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
    def register_custom(cls, func_or_code: str | object) -> str:
        """
        Register a custom provider.
        - If func_or_code is a callable, registers it under its __name__.
        - If func_or_code is a string (function code), executes it and registers the first callable found under its function name.
        Returns the provider name.
        """
        match func_or_code:
            case _ if callable(func_or_code):
                func = func_or_code
                provider_name: str = func.__name__
            case str():
                local_ns: dict = {}
                exec(func_or_code, {}, local_ns)
                func = next((v for v in local_ns.values() if callable(v)), None)
                if func is None:
                    raise ValueError("No callable found in function_code.")
                provider_name = func.__name__
            case _:
                raise TypeError(
                    "func_or_code must be a callable or a string of function code."
                )
        cls._custom_providers[provider_name] = func
        return provider_name

    @classmethod
    def delete_custom(cls, provider_name: str) -> bool:
        """
        Delete a custom provider by its name.
        Returns True if deleted, False if not found.
        Raises TypeError if trying to delete a built-in provider.
        """
        if provider_name in cls._builtin_providers:
            raise TypeError(f"Cannot delete built-in provider: {provider_name}")
        if provider_name in cls._custom_providers:
            del cls._custom_providers[provider_name]
            return True
        return False

    class _ProviderNamespace:
        def __init__(self, providers: dict[str, object]):
            self._providers = providers

        def __getattr__(self, name: str) -> object:
            if name in self._providers:
                func_obj: object = self._providers[name]
                if not callable(func_obj):
                    raise TypeError(f"Provider '{name}' is not callable.")
                return func_obj
            raise AttributeError(f"No such provider: {name}")

        def __dir__(self) -> list[str]:
            return list(self._providers.keys())


def custom_shortener(func: object) -> str:
    """
    Register a custom shortener function with the SDK.
    Returns the provider name.
    """
    return Shortener.register_custom(func)


class BuiltinProviders:
    def __init__(self, shortener: Shortener) -> None:
        self.isgd = shortener._isgd
        self.tinyurl = shortener._tinyurl
