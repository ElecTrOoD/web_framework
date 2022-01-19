from waitress import serve

from app.app import Application
from app.settings import HOST, PORT

app = Application()

if __name__ == '__main__':
    serve(app, host=HOST, port=PORT)
