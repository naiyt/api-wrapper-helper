# from urllib import request, error, parse
import requests
from functools import wraps

__version__ = "0.02"

def set_up(func):
    wraps(func)
    def inner(self, route, params={}):
        route = route [1:] if route[0] == '/' else route
        full_route = '{}/{}'.format(self.base_url, route)
        return func(self, full_route, params)
    return inner

class Api:
    def __init__(self,
                 base_url,
                 headers=None,
                 user_agent=None):
        self.base_url = base_url
        self.headers = self._headers(headers, user_agent)
        self._version = __version__

    @set_up
    def get(self, route, params={}):
        return requests.get(route, params=params, headers=self.headers)

    @set_up
    def post(self, route, params={}):
        return requests.post(route, params=params, headers=self.headers)

    @set_up
    def head(self, route, params={}):
        return requests.head(route, params=params, headers=self.headers)

    @set_up
    def put(self, route, params={}):
        return requests.put(route, params=params, headers=self.headers)

    @set_up
    def delete(self, route, params={}):
        return requests.delete(route, params=params, headers=self.headers)

    def _headers(self, user_headers, user_agent):
        if user_agent is None:
            user_agent = 'ApiHelper v{}'.format(__version__)
        if user_headers is None:
            user_headers = {}
        headers =  {'User-Agent': user_agent,
                    'ACCEPT': 'application/json'}
        return dict(headers, **user_headers)