from abc import abstractmethod

from .templator import render


class BaseController:
    _headers = [('Content-Type', 'text/html')]
    context = {}

    def __call__(self, request, template_dir='templates'):
        self.request = request
        self.template_dir = template_dir

    def get_logic(self):
        pass

    @abstractmethod
    def set_context(self):
        pass


class TemplateController(BaseController):
    template_name = None
    redirect_url = None

    def __call__(self, request, template_dir='templates'):
        super().__call__(request, template_dir)
        self.set_context()
        self.get_logic()
        if not self.redirect_url:
            return '200 OK', self._headers, render(request, self.get_template_name(), self.get_context_data())
        else:
            controller = RedirectTemporary()
            return controller(request, self.redirect_url)

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
        super(TemplateController, self).__call__(request, template_dir)
        controller = RedirectTemporary()
        if request['method'] == 'POST':
            if self.form_is_valid():
                self.set_context()
                self.post_logic()
                if self.success_template:
                    return '200 OK', self._headers, render(request, self.success_template, self.get_context_data())
                return controller(request, self.redirect_url)
            else:
                return controller(request, self.redirect_url)
        else:
            self.set_context()
            self.get_logic()
            return '200 OK', self._headers, render(request, self.get_template_name(), self.get_context_data())

    def form_is_valid(self):
        return all(True if field in self.form_fields else False for field in self.request['form'].keys())

    def post_logic(self):
        pass


class NotFoundPage:
    def __call__(self, request, template_dir='templates'):
        return '404 Not Found', [('Content-Type', 'text/html')], b'404 page not found'


class RedirectPermanent:
    def __call__(self, request, template_dir='templates'):
        return '301 Moved Permanently', [('Content-Type', 'text/html'),
                                         ('Location', f'{request["path"]}/')], b'Redirected'


class RedirectTemporary:
    def __call__(self, request, url, template_dir='templates'):
        return '302 Moved Temporarily', [('Content-Type', 'text/html'),
                                         ('Location', f'{url}')], b'Redirected'


class MethodNotAllowed:
    def __call__(self, request, template_dir='templates'):
        return '405 Method Not Allowed', [('Content-Type', 'text/html')], \
               bytes(f'405 {request["method"]} Method Not Allowed', 'utf-8')
