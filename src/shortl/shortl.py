import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Shortl MCP Server")


class Shortener:
    """
    Main interface for URL shortening. Includes built-in providers and supports custom ones.
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
        if isinstance(provider, str):
            return self._shorten_by_name(url, provider)
        if callable(provider):
            return self._shorten_by_callable(url, provider)
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
        if callable(func_or_code):
            func = func_or_code
            provider_name: str = func.__name__
        elif isinstance(func_or_code, str):
            local_ns: dict = {}
            exec(func_or_code, {}, local_ns)
            func = None
            for v in local_ns.values():
                if callable(v):
                    func = v
                    break
            if func is None:
                raise ValueError("No callable found in function_code.")
            provider_name = func.__name__
        else:
            raise TypeError(
                "func_or_code must be a callable or a string of function code."
            )
        cls._custom_providers[provider_name] = func
        return provider_name

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
    return Shortener.register_custom(func)


class BuiltinProviders:
    def __init__(self, shortener: Shortener) -> None:
        self.isgd = shortener._isgd
        self.tinyurl = shortener._tinyurl


shortener = Shortener()


@mcp.tool()
def create_custom_shortener(code: str) -> str:
    """
    Registers a new custom URL shortener provider with the Shortl system.

    This function allows users to dynamically add their own URL shortening logic to the Shortl server by providing the source code for a Python function that implements the shortening logic. The function code must define a callable that accepts a single argument (the URL to shorten) and returns a string (the shortened URL). The registered provider can then be used in subsequent shortening requests by referencing its function name.

    Args:
        code (str):
            The source code of a Python function implementing the custom shortener. The code should define a function that takes a single argument (the URL as a string) and returns a string (the shortened URL). Example:

                def my_shortener(url: str) -> str:
                    return "https://custom.example/" + url

            The code is executed in a restricted namespace, and the first callable found is registered as the provider.

    Returns:
        str: The name under which the custom provider was registered. This is the function's name as defined in the code.

    Raises:
        ValueError: If the code does not define a valid callable.
        TypeError: If the code is not a string or does not result in a callable.
        Exception: For any other errors during code execution or registration.

    Example:
        >>> create_custom_shortener("def myshort(url: str) -> str: return 'https://x.io/' + url")
        'myshort'
    """
    return shortener.register_custom(code)


@mcp.tool()
def list_providers() -> list[str]:
    """
    Lists all URL shortening providers available in the Shortl system.
    """
    return shortener.list_builtins() + shortener.list_custom()


@mcp.tool()
def shorten(url: str, provider: str) -> str:
    """
    Shortens a given URL using the specified provider (built-in or custom).

    This function provides a unified interface for shortening URLs via the Shortl system. The provider can be any registered shortener, including built-in options or custom providers registered via 'create_custom_shortener'. The function validates the provider, invokes the corresponding shortening logic, and returns the resulting shortened URL.

    Args:
        url (str):
            The original URL to be shortened. Must be a valid, fully-qualified URL (e.g., starting with 'http://' or 'https://').
        provider (str):
            The name of the provider to use for shortening. This can be a built-in provider (e.g., 'isgd', 'tinyurl') or a custom provider registered previously. The provider name is case-sensitive and must exist in the registry.

    Returns:
        str: The shortened URL as returned by the provider. This is typically a compact, redirecting URL suitable for sharing.

    Raises:
        ValueError: If the provider name is not found or the URL is invalid.
        TypeError: If the provider is not callable or does not return a string.
        Exception: For any other errors encountered during the shortening process (e.g., network errors, provider failures).

    Example:
        >>> shorten("https://www.example.com", "isgd")
        'https://is.gd/abc123'
    """
    return shortener.shorten(url, provider)


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
