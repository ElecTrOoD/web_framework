from verse import render


def index_page(request):
    context = {'title': 'Main'}
    return '200 OK', render(request, 'main\\index.html', context)


def about_page(request):
    context = {'title': 'About'}
    return '200 OK', render(request, 'main\\about.html', context)
