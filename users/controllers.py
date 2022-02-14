from sitedata import site
from verse import Layout, TemplateController, FormController

users = Layout('/users')


@users.route('/')
class UsersListPage(TemplateController):
    template_name = 'users/users_list.html'

    def set_context(self):
        self.context = {'title': 'Users', 'users': site.get_users()}


@users.route('/user')
class UserPage(TemplateController):
    template_name = 'users/user.html'

    def set_context(self):
        self.context = {'title': 'User Page', 'user': site.get_user(self.request['request_params']['id'])}


@users.route('/create', methods=('GET', 'POST'))
class UserCreatePage(FormController):
    template_name = 'users/create_user.html'
    redirect_url = '/users/'
    form_fields = ['first_name', 'last_name', 'email', 'type']

    def set_context(self):
        self.context = {'title': 'Create User', 'types': site.user_types}

    def post_logic(self):
        data = self.request['form']
        site.create_user(data['type'], data['first_name'], data['last_name'], data['email'])


@users.route('/delete')
class UserDelete(TemplateController):
    redirect_url = '/users/'

    def set_context(self):
        pass

    def get_logic(self):
        site.delete_user(self.request['request_params']['id'])
