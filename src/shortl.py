#!/usr/bin/python3


# This is "shortl" app. This app can shorten the long URL's and copy it to clipboard
# Author: mdonmez


import requests
import clipboard




# This function does shorten the URL with API
def shorten_url(url):
    api_url = "http://tinyurl.com/api-create.php"
    query_params = {"url": url}
    response = requests.get(api_url, params=query_params)
    return response.text
    
# This function does copy short links to clipboard
def copy_to_clipboard(text):
    clipboard.copy(text)
    
# This function does add https to the URL if there are not
def add_https_to_url(url):
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url
    return url
    
# This function does remove unwanted characters from the URL
def remove_unwanted_characters(long_url):        
    long_url = long_url.strip('"')
    long_url = long_url.strip("'")
    long_url = long_url.strip(" ")
    return long_url





# This function does shorten the URL, this is the main function
def Shorten(long_url, copy: bool):
    short_url = ""  # Initialize short_url to an empty string
    try:
        short_url = shorten_url(long_url)
        if copy:
            copy_to_clipboard(short_url)
        return short_url
    except Exception as e: # If there is an error
        if isinstance(e, requests.exceptions.ConnectionError): # If there is a connection error
            print("Internet connection error.")
        else: # If there is any other error
            print("Error:", e)
