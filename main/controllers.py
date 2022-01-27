from verse import render


def index_page(request, template_dir='templates'):
    context = {'title': 'Main'}
    return '200 OK', render(request, 'main/index.html', context)


def about_page(request, template_dir='templates'):
    context = {'title': 'About'}
    return '200 OK', render(request, 'main/about.html', context)


def contacts(request, template_dir='templates'):
    context = {'title': 'Contacts'}
    if request['method'] == 'POST':
        context['message'] = request['form']
        return '200 OK', render(request, 'main/user_message.html', context)
    return '200 OK', render(request, 'main/contacts.html', context)
