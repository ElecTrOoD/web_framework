from .templator import render


class TemplateController:
    _headers = [('Content-Type', 'text/html')]
    template_name = None
    context = None

    def __call__(self, request, template_dir='templates'):
        self.request = request
        self.template_dir = template_dir
        return '200 OK', self._headers, render(request, self.get_template_name(), self.get_context_data())

    def get_template_name(self):
        if self.template_name:
            return self.template_name
        else:
            raise ValueError('incorrect template name')

    def get_context_data(self):
        if isinstance(self.context, dict):
            return self.context
        return {}


class FormController(TemplateController):
    form_fields = None
    success_template = None

    def __call__(self, request, template_dir='templates'):
        self.request = request
        self.template_dir = template_dir
        if request['method'] == 'POST':
            if self.form_is_valid():
                return '200 OK', self._headers, render(request, self.get_success_template_name(),
                                                       self.get_context_data())
            else:
                return Redirect()
        else:
            return '200 OK', self._headers, render(request, self.get_template_name(), self.get_context_data())

    def get_success_template_name(self):
        if self.success_template:
            return self.success_template
        else:
            raise ValueError('incorrect success template name')

    def form_is_valid(self):
        return all(True if field in self.form_fields else False for field in self.request['form'].keys())


class NotFoundPage:
    def __call__(self, request, template_dir='templates'):
        return '404 Not Found', [('Content-Type', 'text/html')], b'404 page not found'


class Redirect:
    def __call__(self, request, template_dir='templates'):
        return '301 Moved Permanently', [('Content-Type', 'text/html'),
                                         ('Location', f'{request["path"]}/')], b'Redirected'


class MethodNotAllowed:
    def __call__(self, request, template_dir='templates'):
        return '405 Method Not Allowed', [('Content-Type', 'text/html')], \
               bytes(f'405 {request["method"]} Method Not Allowed', 'utf-8')
