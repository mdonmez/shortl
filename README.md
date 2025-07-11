# shortl

A simple, extensible Python library for URL shortening with built-in and custom providers.

---

## Overview

**shortl** provides a unified interface to shorten URLs using popular services like is.gd and TinyURL, and allows you to register your own custom shortener functions. It is designed to be easy to use, type-annotated, and extensible for developers who need URL shortening in their Python projects.

---

## Features

- 🔗 Shorten URLs using built-in providers: **is.gd** and **TinyURL**
- 🧩 Register and use custom URL shortener providers
- 🛠️ Type-annotated, clean API
- 🐍 Python 3.12+ support

---

## Installation

This project uses [uv](https://github.com/astral-sh/uv) for Python dependency management. Make sure you have `uv` installed. If not, follow the [uv installation guide](https://github.com/astral-sh/uv#installation).

```bash
uv sync
```

---

## Usage

### Basic Usage

```python
from shortl import Shortener

shortener = Shortener()

# List available built-in providers
print(shortener.list_defaults())  # ['isgd', 'tinyurl']

# Shorten a URL using is.gd
short_url = shortener.shorten("https://www.example.com", provider="isgd")
print(short_url)

# Shorten a URL using TinyURL
short_url = shortener.shorten("https://www.example.com", provider="tinyurl")
print(short_url)
```

### Registering a Custom Provider

You can register your own shortener function using the `@custom_shortener` decorator:

```python
from shortl import custom_shortener, Shortener

@custom_shortener
def my_shortener(url: str) -> str:
    # Example: just return the original URL (replace with real logic)
    return f"custom://{url}"

shortener = Shortener()
print(shortener.list_custom())  # ['my_shortener']
short_url = shortener.shorten("https://www.example.com", provider="my_shortener")
print(short_url)
```

---

## API Reference

### `Shortener`

- `shortener = Shortener()`
  - Create a new shortener instance.
- `shortener.list_defaults() -> list[str]`
  - List names of built-in providers.
- `shortener.list_custom() -> list[str]`
  - List names of custom-registered providers.
- `shortener.shorten(url: str, provider: str) -> str`
  - Shorten a URL using the specified provider.
- `Shortener.register_custom(func: Callable[[str], str]) -> Callable[[str], str]`
  - Register a custom shortener function by its name.

### `custom_shortener`

- Decorator to register a custom shortener function with the `Shortener` class.

---

## Requirements

- Python 3.12+
- [requests](https://pypi.org/project/requests/)

---

## Contributing

Contributions are welcome! Please open issues or submit pull requests for bug fixes, new features, or improvements.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
