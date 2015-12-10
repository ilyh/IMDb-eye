import requests
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')

API_URL = "http://www.myapifilms.com/imdb"


def searchByIdName(idName):
    params = {
        "idName": idName,
        "format": "JSON",
        "lang": "en-us",
        "filmography": "1"
    }
    r = requests.get(API_URL, params=params)
    
    print(r.json()["filmographies"]["filmography"])

searchByIdName("nm0000132")
