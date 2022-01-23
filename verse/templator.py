import os
from jinja2 import Template

path = os.getcwd()
if 'settings.py' in os.listdir(path):
    from settings import TEMPLATES_PATH
else:
    TEMPLATES_PATH = path + '\\templates\\'


def render(request, template_name, context):
    request['context'].update(context)
    with open(f'{TEMPLATES_PATH}{template_name}', encoding='utf-8') as file:
        template = Template(file.read())

    return bytes(template.render(request['context']), 'utf-8')
