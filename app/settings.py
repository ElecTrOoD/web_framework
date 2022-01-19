import os

from app.front_controllers import current_year

HOST = '127.0.0.1'
# HOST = '0.0.0.0'
PORT = 8080
TEMPLATES_PATH = f'{os.getcwd()}\\templates\\'

fronts = [
    current_year
]
