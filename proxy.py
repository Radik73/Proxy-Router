import tornado.web
import tornado.ioloop
import tornado.websocket
import tornado.gen
import tornado.escape
import tornado.httpclient
import proxy.proxy_main as prx

if __name__ == "__main__":
    try:
        print('Server Running...')
        print('Press ctrl + c to close')
        prx.application.listen(8889)
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        print('Server is finished')