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

# def contacts(request, template_dir='templates'):
#     context = {'title': 'Contacts'}
#     if request['method'] == 'POST':
#         context['message'] = request['form']
#         return '200 OK', render(request, 'main/user_message.html', context)
#     return '200 OK', render(request, 'main/contacts.html', context)
