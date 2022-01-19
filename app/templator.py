from jinja2 import Template

from app.settings import TEMPLATES_PATH


def render(request, template_name, context):
    request['context'].update(context)
    with open(f'{TEMPLATES_PATH}\\{template_name}', encoding='utf-8') as file:
        template = Template(file.read())

    return bytes(template.render(request['context']), 'utf-8')
