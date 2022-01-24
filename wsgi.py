from os import getcwd
from waitress import serve

from verse import Application
from settings import HOST, PORT
from urls import urlpatterns

TEMPLATES_PATH = f'{getcwd()}\\templates\\'

app = Application(routes=urlpatterns, templates_path=TEMPLATES_PATH)

if __name__ == '__main__':
    print(f'Serving on http://{HOST}:{PORT}\n')
    serve(app, host=HOST, port=PORT)
