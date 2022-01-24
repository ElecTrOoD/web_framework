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
