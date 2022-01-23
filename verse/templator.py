from os import getcwd

from jinja2 import Template

try:
    from settings import TEMPLATES_PATH
except ImportError:
    path = getcwd()
    TEMPLATES_PATH = path + '\\templates\\'


def render(request, template_name, context):
    request['context'].update(context)
    with open(f'{TEMPLATES_PATH}{template_name}', encoding='utf-8') as file:
        template = Template(file.read())

    return bytes(template.render(request['context']), 'utf-8')
