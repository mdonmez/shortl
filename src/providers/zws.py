import httpx

class ZWSShortener:
    def __init__(self):
        self.base_url = "https://api.zws.im"
    
    def shorten(self, long_url):
        try:
            payload = {
                "url": long_url
            }
            headers = {
                "accept": "application/json",
                "Content-Type": "application/json"
            }
            
            with httpx.Client() as client:
                response = client.post(
                    f"{self.base_url}/",
                    json=payload,
                    headers=headers
                )
                response.raise_for_status()
                return response.json()['url']
        except httpx.RequestError as e:
            return f"Error: {str(e)}"

if __name__ == "__main__":
    shortener = ZWSShortener()
    url = "https://example.com"
    result = shortener.shorten(url)
    print(f"Result: {result}")