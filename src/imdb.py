import requests
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')

API_URL = "http://www.myapifilms.com/imdb"

fetchApiByParams = lambda x: requests.get(API_URL, params=x).json()


def searchByIdName(idName):
    params = {
        "idName": idName,
        "format": "JSON",
        "lang": "en-us",
        "filmography": "1"
    }
    return fetchApiByParams(params)["filmographies"]


def searchByName(name):
    params = {
        "name": name,
        "format": "JSON",
        "lang": "en-us",
        "filmography": "1"
    }
    return fetchApiByParams(params)[0]["filmographies"]

print(searchByIdName("nm2244205"))
print(searchByName('Léa Seydoux'))
