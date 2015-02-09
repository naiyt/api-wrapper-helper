# from urllib import request, error, parse
import requests
import json
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
                 user_agent=None,
                 verify=True):
        self.base_url = base_url
        self.headers = self._headers(headers, user_agent)
        self.verify = verify
        self.client = requests
        self._version = __version__

    @set_up
    def get(self, route, params={}, pretty=True):
        data = self.client.get(route, params=params, headers=self.headers, verify=self.verify)
        if pretty:
            data.pretty_json = self._prettify(data.json())
        return data

    @set_up
    def post(self, route, params={}, pretty=True):
        data = self.client.post(route, params=params, headers=self.headers, verify=self.verify)
        if pretty:
            data.pretty_json = self._prettify(data.json())
        return data

    @set_up
    def head(self, route, params={}, pretty=True):
        data = self.client.head(route, params=params, headers=self.headers, verify=self.verify)
        if pretty:
            data.pretty_json = self._prettify(data.json())
        return data

    @set_up
    def put(self, route, params={}, pretty=True):
        data = self.client.put(route, params=params, headers=self.headers, verify=self.verify)
        if pretty:
            data.pretty_json = self._prettify(data.json())
        return data

    @set_up
    def delete(self, route, params={}, pretty=True):
        data = self.client.delete(route, params=params, headers=self.headers, verify=self.verify)
        if pretty:
            data.pretty_json = self._prettify(data.json())
        return data

    def _headers(self, user_headers, user_agent):
        if user_agent is None:
            user_agent = 'ApiHelper v{}'.format(__version__)
        if user_headers is None:
            user_headers = {}
        headers =  {'User-Agent': user_agent,
                    'ACCEPT': 'application/json'}
        return dict(headers, **user_headers)

    def _prettify(self, data):
        return json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
