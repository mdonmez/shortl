import httpx

class UlvisShortener:
    def __init__(self):
        self.api_url = "https://ulvis.net/api.php"

    def shorten(self, long_url):
        params = {"url": long_url, "type": "json"}
        with httpx.Client() as client:
            response = client.get(self.api_url, params=params)
            response.raise_for_status()
            return response.text
        
if __name__ == "__main__":
    shortener = UlvisShortener()
    url = "https://example.com"
    result = shortener.shorten(url)
    print(f"Result: {result}")