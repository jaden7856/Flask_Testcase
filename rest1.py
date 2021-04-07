from flask import Flask, jsonify
import flask_restful
from flask_restful import reqparse


app = Flask(__name__)
# app.config["DEBUG"] = True
# $ flask app <- app.py
# 실행 파일을 변경하려면, set FLASK_APP=new_file.py
# 디버그 모드 실행, set FLASK_DEBUG=True -> auto refresh

api = flask_restful.Api(app)


def multipy(param1, param2):
    return param1 * param2


@app.route('/')
def index():
    return "Hello, Flask!"


class HelloWorld(flask_restful.Resource):
    def get(self):
        parser = reqparse.RequestParser()

        # GET /api/multiply?param1=3&param2=4
        parser.add_argument('param1')
        parser.add_argument('param2')
        args = parser.parse_args()

        param1 = args['param1']
        param2 = args['param2']

        if (not param1) or (not param2):
            return {
                'state' : 0,
                'response' : None
            }
    
        param1 = int(param1)
        param2 = int(param2)

        result = multipy(param1, param2)
        return {
            'state' : 1,
            'response' : result
        }
        

# GET, POST, PUT, DELETE ...
# /api/multiply -> GET, POST
# 주문 목록 /orders (GET)
# 주문 하기 /orders (POST)
# 주문 상세보기 /orders/id (GET)
# 주문 수정하기 /orders/id (PUT)
# 주문 삭제하기 /orders/id (DELETE)

api.add_resource(HelloWorld, '/api/multiply')


if __name__ == '__main__':
    app.run()