import requests
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')

API_URL = "http://api.myapifilms.com/imdb/idIMDB"
token = "5a01f13a-f9e4-4df6-bab8-da15354d16eb"

fetchApiByParams = lambda x: requests.get(API_URL, params=x).json()


def getMoviesByidName(idName):
    params = {
        "token": token,
        "idName": idName,
        "format": "json",
        "lang": "en-us",
        "filmography": "1"
    }
    return fetchApiByParams(params)["data"]["names"][0]["filmographies"]


def getMoviesByName(name):
    params = {
        "token": token,
        "name": name,
        "format": "json",
        "lang": "en-us",
        "filmography": "1"
    }
    return fetchApiByParams(params)["data"]["names"][0]["filmographies"]


def getArtistsByMovieid(movieid):
    pass


print(getMoviesByidName("nm2244205"))
print(getMoviesByName("Léa Seydoux"))
