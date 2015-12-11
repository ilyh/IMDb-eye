#!/usr/bin/env python3
#coding=utf-8
import requests
import sys
import io

import conf

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')

API_URL = "http://api.myapifilms.com/imdb/idIMDB"

fetchApiByParams = lambda x: requests.get(API_URL, params=x, timeout=10).json()


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
    params = {
        "token": conf.token,
        "idIMDB": movieid,
        "format": "json",
        "lang": "en-us",
        "actors": "2"
    }
    return fetchApiByParams(params)["data"]["movies"][0]["actors"]


def getArtistsByMovieTitle(movieTitle):
    params = {
        "token": conf.token,
        "title": movieTitle,
        "format": "json",
        "lang": "en-us",
        "actors": "2"
    }
    return fetchApiByParams(params)["data"]["movies"][0]["actors"]

if __name__ == '__main__':
    print(getMoviesByidName("nm2244205"))
    print(getMoviesByName("Léa Seydoux"))
    print(getArtistsByMovieid("tt0111920"))
    print(getArtistsByMovieTitle("Cinema 3"))
