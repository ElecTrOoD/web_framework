from verse import TemplateController, FormController


class IndexPage(TemplateController):
    context = {'title': 'Main'}
    template_name = 'main/index.html'


class AboutPage(TemplateController):
    context = {'title': 'About'}
    template_name = 'main/about.html'


class ContactsPage(FormController):
    context = {'title': 'Contacts'}
    template_name = 'main/contacts.html'
    success_template = 'main/user_message.html'
    form_fields = ['title', 'text', 'email']
