import unittest
from httmock import all_requests, HTTMock
from apihelper import Api, UnacceptedMethod

url = 'http://cool-site.com'

@all_requests
def response_content(url, request):
    return {'status_code': 200,
            'content': 'Oh hai'}


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

    def test_that_bad_verb_raises_exception(self):
        with self.assertRaises(UnacceptedMethod):
            self.test_api.request('jump', '/around', {})

    def test_that_get_request_succeeds(self):
        with HTTMock(response_content):
            self.test_api.request('get', '/', {})

    def test_that_post_request_succeeds(self):
        with HTTMock(response_content):
            self.test_api.request('post', '/', {})

    def test_that_head_request_succeeds(self):
        with HTTMock(response_content):
            self.test_api.request('head', '/', {})

    def test_that_put_request_succeeds(self):
        with HTTMock(response_content):
            self.test_api.request('put', '/', {})

    def test_that_delete_request_succeeds(self):
        with HTTMock(response_content):
            self.test_api.request('delete', '/', {})

if __name__ == '__main__':
    unittest.main(warnings='ignore')