from jinja2 import Environment, FileSystemLoader


def render(request, template_name, context, folder='templates'):
    env = Environment(loader=FileSystemLoader(folder), autoescape=True)
    template = env.get_template(template_name)

    request['context'].update(context)
    new_request = request.pop('context')
    new_request['request'] = request

    return bytes(template.render(new_request), 'utf-8')
