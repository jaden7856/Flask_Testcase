import unittest
import json
import rest1


class FlaskTest(unittest.TestCase):
    def setUp(self):
        rest1.app.testing = True
        self.client = rest1.app.test_client()


    # /api/multiply?param1=3&param2=4
    # -> ? 12
    def test_index(self):
        response = self.client.get('/')

        # response code: 200
        self.assertEqual(response.status_code, 200)
        # content type: text/html; charset=utf-8
        self.assertIn("text/html", response.content_type)
        self.assertEqual(response.charset, 'utf-8')

        content = response.data
        # 반환 데이터 확인
        self.assertEqual(content.decode('utf-8'), 'Hello, Flask!')


    def test_multyfly(self):
        response = self.client.get('/api/multiply?param1=3&param2=4')

        self.assertEqual(response.status_code, 200)
        self.assertIn("application/json", response.content_type)
        
        # TDD(Test Driven Development)
        json_result = json.loads(response.data)
        self.assertEqual(json_result.get('state'), 1)
        self.assertEqual(json_result.get('response'), 12)
        

if __name__ == '__main__':
    unittest.main()