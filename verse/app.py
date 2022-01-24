import datetime
from urllib.parse import parse_qs

from .default_front_controllers import default_fronts
from .extensions import MethodNotAllowed, NotFoundPage, Redirect


class Application:
    def __init__(self, routes={}, fronts=[], templates_path=''):
        self.routes = routes
        self.fronts = default_fronts + fronts
        self.templates_path = templates_path

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']
        request = {
            'path': path,
            'method': environ['REQUEST_METHOD'],
            'context': {},
            'form': self.get_post_data(environ),
            'request_params': self.get_qs_data(environ)
        }
        headers = [('Content-Type', 'text/html')]
        for front in self.fronts:
            front(request)
        if path[-1] != '/':
            controller = Redirect()
            headers.append(('Location', f'{path}/'))
        elif path in self.routes:
            if request['method'] in self.routes[path]['allowed_methods']:
                controller = self.routes[path]['controller']
            else:
                controller = MethodNotAllowed()
        else:
            controller = NotFoundPage()
        code, body = controller(request, self.templates_path)

        print(
            f'{environ["REMOTE_ADDR"]} [{datetime.datetime.now()}] {environ["REQUEST_METHOD"]} {path} {code}')

        start_response(code, headers)
        return [body]
    
    @staticmethod
    def get_qs_data(environ):
        query_string = parse_qs(environ['QUERY_STRING'])
        parsed_data = dict(map(lambda x: (x[0], x[1][0]), query_string.items()))
        return parsed_data

    @staticmethod
    def get_post_data(environ):
        content_length = int(environ.get('CONTENT_LENGTH', 0))
        content_data = environ['wsgi.input'].read(content_length)
        parsed_data = dict(map(lambda x: (x[0].decode(
            'utf-8'), x[1][0].decode('utf-8')), parse_qs(content_data).items()))
        return parsed_data
