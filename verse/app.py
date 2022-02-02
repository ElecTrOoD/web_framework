import datetime
from types import FunctionType
from urllib.parse import parse_qs

from .default_front_controllers import default_fronts
from .default_page_controllers import MethodNotAllowed, NotFoundPage, RedirectPermanent


class Application:
    def __init__(self, routes={}, fronts=[], templates_path='templates'):
        self.routes = routes
        self.fronts = default_fronts + fronts
        self.templates_path = templates_path

    def __call__(self, environ, start_response):
        request = {
            'form': self.get_post_data(environ),
            'request_params': self.get_qs_data(environ)
        }

        for front in self.fronts:
            front(environ, request)
        if not request['path'].endswith('/'):
            controller = RedirectPermanent()
        elif request['path'] in self.routes:
            if request['method'] in self.routes[request['path']]['allowed_methods']:
                if isinstance(self.routes[request['path']]['controller'], FunctionType):
                    controller = self.routes[request['path']]['controller']
                else:
                    controller = self.routes[request['path']]['controller']()
            else:
                controller = MethodNotAllowed()
        else:
            controller = NotFoundPage()

        if hasattr(controller, '__name__'):
            request['controller'] = controller.__name__
        elif hasattr(controller.__class__, '__name__'):
            request['controller'] = controller.__class__.__name__

        code, headers, body = controller(request)

        print(
            f'{environ["REMOTE_ADDR"]} [{datetime.datetime.now()}] {environ["REQUEST_METHOD"]} {request["path"]} {code}')

        start_response(code, headers)
        return [body]

    @staticmethod
    def get_qs_data(environ):
        if environ['QUERY_STRING']:
            query_string = parse_qs(environ['QUERY_STRING'])
            parsed_data = dict(map(lambda x: (x[0], x[1][0]), query_string.items()))
            return parsed_data
        return {}

    @staticmethod
    def get_post_data(environ):
        content_length = int(environ.get('CONTENT_LENGTH', 0))
        if content_length:
            content_data = environ['wsgi.input'].read(content_length)
            parsed_data = dict(map(lambda x: (x[0], x[1][0]) if len(x[1]) == 1 else x,
                                   parse_qs(content_data.decode('utf-8'), True).items()))
            return parsed_data
        return {}
