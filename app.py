import json
import falcon
from addfile import adder

class Home:
    def on_get(self, req, resp):
        data = req.media
        content ={
            "name" : data['data'],
            "app" : "falcon"
        }

        resp.body = json.dumps(content)
        resp.status = falcon.HTTP_OK
        return resp

    def on_post(self, req, resp):
        request = req.media
        content = {
            "sum is" :  adder(request['a'], request['b'])
        }

        resp.body = json.dumps(content)
        resp.status = falcon.HTTP_OK
        return resp

api = falcon.App()
api.add_route('/',Home())