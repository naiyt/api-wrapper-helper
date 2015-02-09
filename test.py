import unittest
from httmock import all_requests, HTTMock
from apihelper import Api

url = 'http://cool-site.com'

@all_requests
def response_content(url, request):
    if request.method == 'GET':
        return get_response
    elif request.method == 'POST':
        return post_response
    elif request.method == 'HEAD':
        return head_response
    elif request.method == 'PUT':
        return put_response
    elif request.method == 'DELETE':
        return delete_response

class TestApi(unittest.TestCase):
    def setUp(self):
        self.url = url
        self.test_api = Api(self.url)

    def test_that_base_url_is_set(self):
        self.assertEqual(self.test_api.base_url, self.url)

    def test_that_headers_are_set(self):
        headers = {'Authorization': 'Super secret OAuth'}
        api_with_headers = Api(self.url, headers=headers)
        self.assertDictEqual(api_with_headers.headers, {
                                'ACCEPT': 'application/json',
                                'User-Agent': 'ApiHelper v{}'.format(api_with_headers._version),
                                'Authorization': 'Super secret OAuth'
                            })

    def test_that_user_agent_is_set(self):
        user_agent = 'Super cool user agent'
        api_with_agent = Api(self.url, user_agent=user_agent)
        self.assertEqual(api_with_agent.headers['User-Agent'], user_agent)

    def test_route_with_leading_slash(self):
        with HTTMock(response_content):
            res = self.test_api.get('/url')
        self.assertEqual(res.url, '{}/url'.format(self.url))

    def test_route_without_leading_slash(self):
        with HTTMock(response_content):
            res = self.test_api.get('url')
        self.assertEqual(res.url, '{}/url'.format(self.url))

    def test_that_get_request_succeeds(self):
        with HTTMock(response_content):
            res = self.test_api.get('/', {'user': 'nate'})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.request.method, 'GET')
        self.assertDictEqual(res.json(), {
            'success': True,
            'message': get_message
        })

    def test_that_post_request_succeeds(self):
        with HTTMock(response_content):
            res = self.test_api.post('/', {'password': 'new_pass'})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.request.method, 'POST')
        self.assertDictEqual(res.json(), {
            'success': True,
            'message': post_message
        })

    def test_that_head_request_succeeds(self):
        with HTTMock(response_content):
            res = self.test_api.head('/', {'person': 'john'})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.request.method, 'HEAD')
        self.assertDictEqual(res.json(), {
            'success': True,
            'message': head_message
        })


    def test_that_put_request_succeeds(self):
        with HTTMock(response_content):
            res = self.test_api.put('/', {'new_user': 'naiyt'})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.request.method, 'PUT')
        self.assertDictEqual(res.json(), {
            'success': True,
            'message': put_message
        })


    def test_that_delete_request_succeeds(self):
        with HTTMock(response_content):
            res = self.test_api.delete('/', {'user': 'nate'})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.request.method, 'DELETE')
        self.assertDictEqual(res.json(), {
            'success': True,
            'message': delete_message
        })

get_message = 'You gat!'
get_response = {
    'status_code': 200,
    'content': {
        'success': True,
        'message': get_message
    }
}

post_message = 'You post!'
post_response = {
    'status_code': 200,
    'content': {
        'success': True,
        'message': post_message
    }
}

head_message = 'You head!'
head_response = {
    'status_code': 200,
    'content': {
        'success': True,
        'message': head_message
    }
}

put_message = 'You put!'
put_response = {
    'status_code': 200,
    'content': {
        'success': True,
        'message': put_message
    }
}

delete_message = 'You delete!'
delete_response = {
    'status_code': 200,
    'content': {
        'success': True,
        'message': delete_message
    }
}

if __name__ == '__main__':
    unittest.main()
