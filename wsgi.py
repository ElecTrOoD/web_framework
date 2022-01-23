from waitress import serve

from verse import Application
from settings import HOST, PORT
from urls import urlpatterns

app = Application(urlpatterns)

if __name__ == '__main__':
    print(f'Serving on http://{HOST}:{PORT}...\n')
    serve(app, host=HOST, port=PORT)
