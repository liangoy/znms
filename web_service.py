import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import json
from tornado.options import define, options

import fn

define("port", default=6677, help="run on the given port", type=int)

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        action=self.get_argument("action")
        value=self.get_argument("value")
        c=compile(r'''%s(json.loads(r'%s'))'''%(action,value),'','eval')
        data=eval(c)
        self.write({'data':data})



        
if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[(r"/", IndexHandler)])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
