#!/usr/bin/env python3
# coding=utf-8
import json
import os
from concurrent.futures import ThreadPoolExecutor

import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.gen

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

    @tornado.gen.coroutine
    def get(self, q):
        executor = ThreadPoolExecutor(max_workers=5)
        all_works = yield executor.submit(imdb.getMoviesByidName, q)

        # 调试时只返回前10部作品
        movie_list = sum([x['filmography'] for x in all_works], [])[:10]

        future_artists = {}
        for x in movie_list:
            future_artists[x["imdbid"]] = executor.submit(
                imdb.getArtistsByMovieid, x["imdbid"])
        artists = yield {x["imdbid"]: future_artists[x["imdbid"]] for x in movie_list}
        executor.shutdown()

        relations = {}
        for x in movie_list:
            relations[x["imdbid"]] = {"title": x[
                "title"], "artists": artists[x["imdbid"]][:]}
        self.write_json(relations)


class MovieHandler(BaseHandler):

    def get(self, q):
        self.write("hello,world")


class IndexHandler(BaseHandler):

    def get(self):
        self.render("index.html")

handlers = [
    (r"/api/artist/id/(.+)", ArtistIdHandler),
    (r"/api/movie/(.+)", MovieHandler),
    (r"/", IndexHandler),
]

if __name__ == "__main__":
    from tornado.options import options, parse_command_line
    parse_command_line()
    app = tornado.web.Application(
        handlers,
        template_path=os.path.join(
            os.path.dirname(__file__), "templates"),
        static_path=os.path.join(
            os.path.dirname(__file__), "static"),
        debug=__debug__)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
