import json
import falcon
from addfile import adder
from database import init_session, Session, engine
from models import UserTable

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

class UserSignup:
    def on_get(self, req, resp):
        args = req.media
        username = args.get('username')

        connected= engine.raw_connection()
        connection = connected.cursor()
        connection.execute("""SELECT * FROM users WHERE username= '%s'"""%str(username))
        print(connection)
        user = connection.fetchall()

        print(user)
        resp.body = json.dumps(user)
        resp.status = falcon.HTTP_OK

        return resp

    def on_post(self, req, resp):
        args = req.media
        username = args.get('username')
        password = args.get('password')

        connection = engine.connect()
        connection.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        connection.close()
        responses = 'Done'

        resp.status = falcon.HTTP_OK
        resp.body = json.dumps(responses)
        return resp




init_session()
api = falcon.App()
api.add_route('/',Home())
api.add_route('/users',UserSignup())