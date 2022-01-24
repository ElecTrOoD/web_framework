from jinja2 import Template


def render(request, template_path, context):
    request['context'].update(context)
    with open(template_path, encoding='utf-8') as file:
        template = Template(file.read())

    return bytes(template.render(request['context']), 'utf-8')
