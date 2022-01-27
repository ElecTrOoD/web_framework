import datetime
from urllib.parse import parse_qs

from .default_front_controllers import default_fronts
from .extensions import MethodNotAllowed, NotFoundPage, Redirect


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
        headers = [('Content-Type', 'text/html')]
        for front in self.fronts:
            front(environ, request)
        if not request['path'].endswith('/'):
            controller = Redirect()
            headers.append(('Location', f'{request["path"]}/'))
        elif request['path'] in self.routes:
            if request['method'] in self.routes[request['path']]['allowed_methods']:
                controller = self.routes[request['path']]['controller']
            else:
                controller = MethodNotAllowed()
        else:
            controller = NotFoundPage()
        request['controller'] = controller.__name__
        code, body = controller(request)

        print(
            f'{environ["REMOTE_ADDR"]} [{datetime.datetime.now()}] {environ["REQUEST_METHOD"]} {request["path"]} {code}')

        start_response(code, headers)
        return [body]

    @staticmethod
    def get_qs_data(environ):
        if environ['QUERY_STRING']:
            query_string = parse_qs(environ['QUERY_STRING'])
            parsed_data = dict(
                map(lambda x: (x[0], x[1][0]), query_string.items()))
            return parsed_data
        return {}

    @staticmethod
    def get_post_data(environ):
        content_length = int(environ.get('CONTENT_LENGTH', 0))
        if content_length:
            content_data = environ['wsgi.input'].read(content_length)
            parsed_data = dict(map(lambda x: (x[0].decode(
                'utf-8'), x[1][0].decode('utf-8')), parse_qs(content_data).items()))
            return parsed_data
        return {}
