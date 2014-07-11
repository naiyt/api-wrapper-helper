# from urllib import request, error, parse
import requests
__version__ = "0.01"

class UnacceptedMethod(Exception):
    pass

class Api:
    def __init__(self,
                 base_url,
                 headers=None,
                 user_agent=None):
        self.base_url = base_url
        self.headers = self._headers(headers, user_agent)
        self.accepted_methods = {'GET': requests.get,
                                 'POST': requests.post,
                                 'HEAD': requests.head,
                                 'PUT': requests.put,
                                 'DELETE': requests.delete}
        self._version = __version__

    def request(self, verb, route, params):
        verb = verb.upper()
        if verb not in self.accepted_methods:
            raise UnacceptedMethod('{} not an accepted method. Use one of {}'.format(verb, ', '.join(self.accepted_methods)))
        full_route = '{}{}'.format(self.base_url, route)
        return self.accepted_methods[verb](
            full_route,
            params=params,
            headers=self.headers)

    def _headers(self, user_headers, user_agent):
        if user_agent is None:
            user_agent = 'ApiHelper v{}'.format(__version__)
        if user_headers is None:
            user_headers = {}
        headers =  {'User-Agent': user_agent,
                    'ACCEPT': 'application/json'}
        return dict(headers, **user_headers)