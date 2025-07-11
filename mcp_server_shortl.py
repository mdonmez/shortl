from shortl import Shortener
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("shortl")
s = Shortener()


@mcp.tool()
def register_custom_provider(name: str, function: str) -> str:
    """
    Register a custom URL shortening provider with a user-defined function.

    This function allows you to register a custom provider for URL shortening by supplying a provider name and the function code as a string. The function code should define a callable that takes a single argument (the URL as a string) and returns the shortened URL as a string. The provider will then be available for use with the `shorten_url` tool by its registered name.

    Args:
        name (str): The name to register the custom provider under. This name will be used to reference the provider when shortening URLs.
        function (str): The source code of the function to use as the provider. The code must define a callable that accepts a single argument (the URL) and returns a string (the shortened URL).

    Returns:
        str: The name of the registered provider.

    Raises:
        ValueError: If the function code does not define a callable, or if no name is provided.
        TypeError: If the function code is not a string.
        Exception: Any exception raised during the execution of the function code.

    Example:
        >>> function_code = '''\
        def myshortener(url: str) -> str:
            return "https://custom.example/" + url
        '''
        >>> register_custom_provider("myshortener", function_code)
        'myshortener'

    Note:
        - The function code is executed in a restricted namespace. Only the first callable found will be registered.
        - The provider name must be unique among all custom and built-in providers.
        - The registered provider can be used with the `shorten_url` tool by specifying its name as the provider argument.
    """
    return s.register_custom(function, name)


@mcp.tool()
def shorten_url(url: str, provider: str) -> str:
    """
    Shorten a URL using a specified provider (built-in or custom).

    This function shortens the given URL using the specified provider name. The provider can be one of the built-in providers (e.g., "isgd", "tinyurl") or a custom provider registered previously. The function delegates to the Shortener class, which performs the actual shortening and error handling.

    Args:
        url (str): The original URL to be shortened. Must be a valid URL string.
        provider (str): The name of the provider to use for shortening. This can be a built-in provider ("isgd", "tinyurl") or a custom provider registered via `register_custom_provider`.

    Returns:
        str: The shortened URL as returned by the provider.

    Raises:
        ValueError: If the specified provider is not found among built-in or custom providers.
        TypeError: If the provider is not callable or does not return a string.
        Exception: Any exception raised by the underlying HTTP request or custom provider logic.

    Example:
        >>> shorten_url("https://www.example.com", "isgd")
        'https://is.gd/abc123'
        >>> shorten_url("https://www.example.com", "mycustom")
        'https://custom.example/https://www.example.com'

    Note:
        - Built-in providers: "isgd", "tinyurl"
        - Custom providers must be registered before use.
        - The function does not validate the URL format; invalid URLs may result in provider errors.
    """
    return s.shorten(url, provider)


def main():
    mcp.run()


if __name__ == "__main__":
    main()
