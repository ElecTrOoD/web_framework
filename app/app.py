import datetime

from app.extensions import get_routes, get_fronts, Redirect, NotFoundPage


class Application:
    def __init__(self):
        self.routes = get_routes()
        self.fronts = get_fronts()

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']
        request = {'path': path, 'context': {}}
        headers = [('Content-Type', 'text/html')]
        for front in self.fronts:
            front(request)
        if path[-1] != '/':
            controller = Redirect()
            headers.append(('Location', f'{path}/'))
        elif path in self.routes:
            controller = self.routes[path]
        else:
            controller = NotFoundPage()
        code, body = controller(request)

        print(f'{environ["REMOTE_ADDR"]} [{datetime.datetime.now()}] {environ["REQUEST_METHOD"]} {path} {code}')

        start_response(code, headers)
        return [body]
