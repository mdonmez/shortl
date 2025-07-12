from mcp.server.fastmcp import FastMCP
from shortl import Shortener

mcp = FastMCP("Shortl MCP Server")
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
def shorten(url: str, provider: str) -> str:
    """
    Shortens a given URL using the specified provider (built-in or custom).

    This function provides a unified interface for shortening URLs via the Shortl system. The provider can be any registered shortener, including built-in options (such as 'isgd' or 'tinyurl') or custom providers registered via 'create_custom_shortener'. The function validates the provider, invokes the corresponding shortening logic, and returns the resulting shortened URL.

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
