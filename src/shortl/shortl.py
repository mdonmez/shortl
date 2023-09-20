#!/usr/bin/python3

# Import necessary libraries
import requests
import clipboard

# Define a class for URL shortening
class Shortener:
    def __init__(self):
        # API URL for TinyURL service
        self.api_url = "http://tinyurl.com/api-create.php"

    # Method to shorten a given URL
    def shorten_url(self, url):
        # Define query parameters for the API request
        query_params = {"url": url}
        # Send a GET request to the TinyURL API
        response = requests.get(self.api_url, params=query_params)
        
        # Return the shortened URL received in the response
        return response.text

# Define a class for handling URLs
class URL:
    def __init__(self, long_url):
        # Initialize with the long URL
        self.long_url = long_url

    # Method to add "https://" to the URL if not present
    def add_https(self):
        # Check if the URL starts with "http://" or "https://"
        if not self.long_url.startswith("http://") and not self.long_url.startswith("https://"):
            # If not, add "https://"
            self.long_url = "https://" + self.long_url

    # Method to remove unwanted characters from the URL
    def remove_unwanted_characters(self):
        # Strip double quotes, single quotes, and spaces from the URL
        self.long_url = self.long_url.strip('"')
        self.long_url = self.long_url.strip("'")
        self.long_url = self.long_url.strip(" ")

# Define a class for URL shortening operations
class Shortl:
    def __init__(self):
        # Initialize with a Shortener object
        self.shortener = Shortener()

    
    # Method to shorten a URL and optionally copy it to clipboard
    def shorten(self, long_url, copy=False):
        # Create a URL object
        url = URL(long_url)

        
        # Ensure "https://" is added to the URL
        url.add_https()
        
        # Remove unwanted characters from the URL
        url.remove_unwanted_characters()
        
        # Shorten the URL using the Shortener class
        short_url = self.shortener.shorten_url(url.long_url)


        
        # If copy parameter is True, copy the shortened URL to clipboard
        if copy:
            clipboard.copy(short_url)
            
        # Return the shortened URL
        return short_url
