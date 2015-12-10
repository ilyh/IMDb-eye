from tornado.options import define

token = "5a01f13a-f9e4-4df6-bab8-da15354d16eb"
define("port", default=8888, help="run on the given port", type=int)
