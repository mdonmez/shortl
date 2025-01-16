<div style="text-align: center;" align="center">
<a href="https://github.com/mdonmez/shortl">
</a>
<h1>shortl - Versatile URL Shortener</h1>
<p>
shortl is a versatile URL shortening application that supports multiple URL shortening services. It's designed to be easily extensible with new providers.
</p>
</div>

## Features

- Supports multiple URL shortening services.
- Easily extensible with new providers by adding new Python files to the `providers` directory.
- Uses the `httpx` library for making HTTP requests in pre-defined providers.
- All providers is API-keyless. So all providers are free to use.
- Includes pre-defined providers for TinyURL, Ulvis, and ZWS services.

## Usage

The application can be used to shorten URLs using different providers. You can specify which provider to use when calling the `ShortL.shortener()` method.

## Operation Logic

The `main.py` file dynamically loads URL shortening providers from the `providers` directory. It looks for Python files in that directory and tries to import a class that ends in "Shortener" from each. The `ShortL.shortener()` method returns an instance of the found class.

## Add new provider

To add a new provider, create a new Python file in the `providers` directory. The file should contain a class that ends in "Shortener" and that implements a `shorten` method which takes the long URL as a parameter. The class should make a call to the API of the service to shorten the URL and return the short URL.

Here's an example of how a provider file should be structured:

```python
import httpx

class ExampleShortener:
    def __init__(self):
        # Set the API endpoint for the shortening service.
        self.api_url = "API_ENDPOINT_HERE"

    def shorten(self, long_url):
        # Prepare the parameters for the API request, if needed.
        # params = {"url": long_url}

        # Make an HTTP request to the API to shorten the URL.
        with httpx.Client() as client:
            # response = client.get(self.api_url, params=params) # Example GET request
            # response = client.post(self.api_url, json={"url":long_url}) # Example POST request
            
            # Raise an exception if the request fails.
            # response.raise_for_status()

            # Return the shortened URL.
            return "SHORT_URL_HERE"
```

See `providers/tinyurl.py`, `providers/ulvis.py`, and `providers/zws.py` for more examples.

## Technology Stack

- Python 3.6+
- httpx

## Setup

### Requirements

- Python 3.6 or higher
- httpx library

### Installation

1. Clone the repository.
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment: `venv\Scripts\activate` on Windows, or `source venv/bin/activate` on Linux/macOS.
4. Install the dependencies: `pip install -r requirements.txt`

### Usage

Run the `main.py` file to test the application. You can modify the `if __name__ == '__main__'` block to test with different providers and URLs.
For example, to use the ulvis provider, you can use the following code:
```python
from main import ShortL
shortener = ShortL.shortener("ulvis")
print(shortener.shorten("https://www.example.com"))
```
You can replace `"ulvis"` with `"tinyurl"` or `"zws"` to use other providers.

## License

This project is licensed under the GPLv3 License - See [LICENSE](LICENSE) for details.

## Notes

I will try to package this application and make it into an installable pip package.
