from os import getcwd
from waitress import serve

from courses.controllers import courses, categories
from main.controllers import main
from users.controllers import users
from verse import Application
from settings import HOST, PORT

# TEMPLATES_PATH = f'{getcwd()}\\templates\\'

app = Application()
app.register_urls((main, courses, categories, users))

if __name__ == '__main__':
    print(f'Serving on http://{HOST}:{PORT}\n')
    serve(app, host=HOST, port=PORT)
