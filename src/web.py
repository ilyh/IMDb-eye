#!/usr/bin/env python3

from collections import namedtuple
import json

import tornado.httpserver
import tornado.ioloop
import tornado.web

import conf
import imdb


class BaseHandler(tornado.web.RequestHandler):

    def write_json(self, obj):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.finish(json.dumps(obj, default=str, ensure_ascii=False, indent=4,
                               sort_keys=True, separators=(",", ": ")))

    def body_s(self):
        if not hasattr(self, "_body_s"):
            self._body_s = self.request.body.decode()
        return self._body_s


class ArtistIdHandler(BaseHandler):

    def get(self, q):
        all_works = imdb.getMoviesByidName(q)
        movie_list = sum([x['filmography'] for x in all_works], [])
        relations = {}
        for x in movie_list[:5]:
            relations[x["imdbid"]] = {"title": x[
                "title"], "artists": imdb.getArtistsByMovieid(x["imdbid"])[:5]}
        self.write_json(relations)


class MovieHandler(BaseHandler):

    def get(self, q):
        self.write("hello,world")
        # pass

handlers = [
    (r"/api/artist/id/(.+)", ArtistIdHandler),
    (r"/api/movie/(.+)", MovieHandler),
]

if __name__ == "__main__":
    from tornado.options import options, parse_command_line
    parse_command_line()
    app = tornado.web.Application(handlers, debug=__debug__)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
