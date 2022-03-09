import json
import falcon


class Home:
    def on_get(self, req, resp):
        data = req.media
        # print(data['data'])
        # content ={
        #     "name" : "mohtashim",
        #     "app" : "falcon"
        # }
        content ={
            "name" : data['data'],
            "app" : "falcon"
        }

        resp.body = json.dumps(content)
        return resp

api = falcon.App()
api.add_route('/',Home())