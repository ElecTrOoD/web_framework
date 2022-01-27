from datetime import datetime


def initial_formation(environ, request):
    default_request = {
        'path': environ['PATH_INFO'],
        'method': environ['REQUEST_METHOD'],
        'context': {}
    }
    request.update(default_request)

def now(environ, request):
    request['context']['now'] = datetime.now()


default_fronts = [
        initial_formation,
        now
        ]
