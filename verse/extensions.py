from urllib.parse import parse_qs


class NotFoundPage:
    def __call__(self, request, template_dir):
        return '404 Not Found', b'404 page not found'


class Redirect:
    def __call__(self, request, template_dir):
        return '301 Moved Permanently', b'Redirected'


class MethodNotAllowed:
    def __call__(self, request, template_dir):
        return '405 Method Not Allowed', bytes(f'405 {request["method"]} Method Not Allowed', 'utf-8')


def get_qs_data(environ):
    query_string = parse_qs(environ['QUERY_STRING'])
    parsed_data = dict(map(lambda x: (x[0], x[1][0]), query_string.items()))
    return parsed_data


def get_post_data(environ):
    content_length = int(environ.get('CONTENT_LENGTH', 0))
    content_data = environ['wsgi.input'].read(content_length)
    parsed_data = dict(map(lambda x: (x[0].decode(
        'utf-8'), x[1][0].decode('utf-8')), parse_qs(content_data).items()))
    return parsed_data
