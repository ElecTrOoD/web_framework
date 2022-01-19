from datetime import date


def current_year(request):
    request['context']['current_year'] = date.today().year


