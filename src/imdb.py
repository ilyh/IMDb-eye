import requests
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')

API_URL = "http://www.myapifilms.com/imdb"

fetchApiByParams = lambda x: requests.get(API_URL, params=x).json()


def getMoviesByidName(idName):
    params = {
        "idName": idName,
        "format": "JSON",
        "lang": "en-us",
        "filmography": "1"
    }
    return fetchApiByParams(params)["filmographies"]


def getMoviesByName(name):
    params = {
        "name": name,
        "format": "JSON",
        "lang": "en-us",
        "filmography": "1"
    }
    return fetchApiByParams(params)[0]["filmographies"]


def getArtistsByMovieid(movieid):
    pass


print(getMoviesByidName("nm2244205"))
print(getMoviesByName("Léa Seydoux"))
