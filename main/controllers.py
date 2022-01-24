from verse import render


def index_page(request, template_dir):
    context = {'title': 'Main'}
    return '200 OK', render(request, f'{template_dir}main\\index.html', context)


def about_page(request, template_dir):
    context = {'title': 'About'}
    if request['method'] == 'POST':
        context['message'] = request['form']
    return '200 OK', render(request, f'{template_dir}main\\about.html', context)
