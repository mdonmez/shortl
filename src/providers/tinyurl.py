import httpx

class TinyurlShortener:
    def __init__(self):
        self.api_url = "http://tinyurl.com/api-create.php"
        
    def shorten(self, long_url: str) -> str:
        """
        Shorten a URL using TinyURL's API
        Args:
            long_url (str): The URL to shorten
        Returns:
            str: Shortened URL or error message
        """
        try:
            response = httpx.get(self.api_url, params={"url": long_url})
            
            if response.status_code == 200:
                return response.text
            return f"Error: Status code {response.status_code}"
            
        except Exception as e:
            return f"Error: {str(e)}"

if __name__ == "__main__":
    shortener = TinyurlShortener()
    long_url = "https://www.example.com"
    result = shortener.shorten(long_url)
    print(f"Shortened URL: {result}")
