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

        connected = engine.raw_connection()
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
    def on_put(self, req, resp):
        args = req.media
        userid = args.get('id')

        connected = engine.raw_connection()
        cursor  = connected.cursor()
        cursor.execute("""SELECT * from users where id='%s'"""%userid)
        user_before = cursor.fetchone()

        cursor.execute("""UPDATE users SET username='mohtashimk' where id='%s'"""%userid)
        cursor.execute("""SELECT * from users where id='%s'"""%userid)

        user_after = cursor.fetchone()
        connected.commit()
        cursor.close()

        resp.body = json.dumps([user_before,user_after])
        resp.status = falcon.HTTP_OK

    

        return resp
        

    def on_delete(self, req, resp):
        args = req.media

        username = args.get('username')
        connection = engine.raw_connection()
        cursor = connection.cursor()
        
        cursor.execute('SELECT count (*) from users')

        total = cursor.fetchone()[0]
        cursor.close()
        cursor = connection.cursor()
        cursor.execute("""SELECT count (*) from users where username='%s'"""%username)


        count = cursor.fetchone()[0]

        if not count:
            d ={
                "msg":"No user found with given id"
            }
            resp.body= json.dumps(d)
            resp.status = falcon.HTTP_NOT_FOUND
            return resp
        else:
            
            cursor.execute("""delete from users where username='%s'"""%username)
            connection.commit()
            
            d = {
                "msg":"User deleted",
                "total_before_deletion":total,
                "total_with_username":count,
            }

            resp.body= json.dumps(d)
            resp.status = falcon.HTTP_OK
            
            return resp
            


init_session()
api = falcon.App()
api.add_route('/',Home())
api.add_route('/users',UserSignup())