# shortl

*A Python module for simple link shortening.*

## Description

"shortl" is a Python module that allows you to easily shorten long URLs using various shortening services. It also provides error correction and automatic copying of the shortened URL.

## Usage

#### Using the copy feature
```python
import shortl

very_long_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
short_url = shortl.Shorten(long_url=very_long_url, copy=True)

print(short_url)
```
#### Without using the copy feature
```python
import shortl

very_long_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
short_url = shortl.Shorten(long_url=very_long_url, copy=False)

print(short_url)
```


## Installation
- Download the repository.
- Run ```setup.py``` file.


## Features
- Simple and easy to use.
- Link shortening with TinyURL.
- Error correction (e.g., removing quotes, correcting http(s) spelling).
- Automatic copying.


## To Do
- Add more link shortening services.
- Include additional setting options.
- Improve code readability and documentation.


## License
This project is licensed under the [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.en.html) 
