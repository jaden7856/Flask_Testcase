from flask import Flask, jsonify, request
from flask_restful import reqparse
import flask_restful
import json
import pymysql

pp = Flask(__name__)
# app.config["DEBUG"] = True
api = flask_restful.Api(app)

config = {
    'host': '172.0.0.1',
    'port': 13306,
    'user': 'root',
    'database': 'mydb'
}

@app.route('/')
def index():
    return "Welcome to ORDER Microservice!"


class Order(flask_restful.Resource):
    def __init__(self):
        self.conn = pymysql.connect(**config)
        self.cursor = self.conn.cursor()

    
    def get(self, order_id):
        sql = '''SELECT total_qty, total_price from orders a 
                    INNER JOIN order_detail b ON a.order_id = b.order_id WHERE a.order_id=%s;       
                SELECT menu_name, menu_price FROM order_detail a 
                    INNER JOIN menu b ON a.menu_id = b.menu_id WHERE a.order_id=%s;
        '''
        self.cursor.execute(sql, [order_id])
        
        result_set = self.cursor.fetchall()

        row_headers = [x[0] for x in self.cursor.description]

        json_data = []
        for result in result_set:
            json_data.append(dict(zip(row_headers, result)))

        return jsonify(json_data)

    def post(self, order_id):
        json_data = request.get_json()
        json_data['order_id'] = order_id

        # DB INSERT
        sql = '''INSERT INTO orders(requests) VALUES(%s);
                INSERT INTO users(phone_number) VALUES(%S);
        '''
        self.cursor.execute(sql, [order_id, 
                            json_data['requests'],
                            json_data['phone_number']
                            ])
        self.conn.commit()

        # producer 인스턴스의 send() 메소드로 json 데이터 전송
        self.producer.send('new_orders', value=json.dumps(json_data).encode())
        self.producer.flush()


        response = jsonify(json_data)
        response.status_code = 201

        return response


api.add_resource(Order, '/order-ms/<string:order_id>/orders')


if __name__ == '__main__':
    app.run()