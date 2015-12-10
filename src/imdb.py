import requests
import sys
import io

import conf

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')

API_URL = "http://api.myapifilms.com/imdb/idIMDB"

fetchApiByParams = lambda x: requests.get(API_URL, params=x).json()


def getMoviesByidName(idName):
    params = {
        "token": conf.token,
        "idName": idName,
        "format": "json",
        "lang": "en-us",
        "filmography": "1"
    }
    return fetchApiByParams(params)["data"]["names"][0]["filmographies"]


def getMoviesByName(name):
    params = {
        "token": conf.token,
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
