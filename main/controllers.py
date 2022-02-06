from verse import TemplateController, FormController, Layout

main = Layout('/')


@main.route('/')
class IndexPage(TemplateController):
    template_name = 'main/index.html'

    def set_context(self):
        self.context = {'title': 'Main'}


@main.route('/about')
class AboutPage(TemplateController):
    template_name = 'main/about.html'

    def set_context(self):
        self.context = {'title': 'About'}


@main.route('/contacts', methods=('GET', 'POST'))
class ContactsPage(FormController):
    template_name = 'main/contacts.html'
    success_template = 'main/user_message.html'
    form_fields = ['title', 'text', 'email']

    def set_context(self):
        self.context = {'title': 'Contacts'}
