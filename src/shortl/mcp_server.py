from mcp.server.fastmcp import FastMCP
from shortl.shortl import Shortener

mcp = FastMCP("Shortl MCP Server")
shortener = Shortener()


@mcp.tool()
def create_custom_shortener(code: str) -> str:
    """
    Registers a new custom URL shortener provider with the Shortl system.
    The code must define a function that takes a single argument (the URL as a string) and returns a string (the shortened URL).
    Returns the function's name as the provider name.
    """
    return shortener.register_custom(code)


@mcp.tool()
def delete_custom_provider(provider_name: str) -> bool:
    """
    Deletes a custom URL shortener provider from the Shortl system by name.
    Returns True if the provider was deleted, False if not found.
    Raises TypeError if attempting to delete a built-in provider.
    """
    return Shortener.delete_custom(provider_name)


@mcp.tool()
def list_providers() -> list[dict[str, str]]:
    """
    Lists all URL shortening providers available in the Shortl system, with metadata indicating whether each provider is built-in or custom.
    Returns a list of dicts with 'name' and 'type' ('builtin' or 'custom').
    """
    builtins: list[str] = shortener.list_builtins()
    customs: list[str] = shortener.list_custom()
    providers: list[dict[str, str]] = [
        {"name": name, "type": "builtin"} for name in builtins
    ] + [{"name": name, "type": "custom"} for name in customs]
    return providers


@mcp.tool()
def shorten(url: str, provider: str) -> str:
    """
    Shortens a given URL using the specified provider (built-in or custom).
    Returns the shortened URL as returned by the provider.
    Raises ValueError, TypeError, or Exception for errors.
    """
    return shortener.shorten(url, provider)


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
