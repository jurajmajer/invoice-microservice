import json
import logging
import os
from pathlib import Path

from jinja2 import Template

from app.bl import util

log = logging.getLogger(__name__)
template_root = util.read_env_var('TEMPLATE_ROOT')
output_folder = util.read_env_var('OUTPUT_FOLDER')


def render_html(template_id, template_params, lang, output_filename):
    template_folder = get_template_folder(template_id, lang)
    template_params = template_params | load_static_template_params(template_folder)
    html_content = render_template(os.path.join(template_folder, 'html.jinja2'),
                                   template_params)

    output_filepath = get_html_output_filename(output_filename)
    Path(os.path.dirname(output_filepath)).mkdir(parents=True, exist_ok=True)
    with open(output_filepath, 'w', encoding='utf-8') as f:
        f.write(html_content)

    return output_filepath


def render_template(template_file, template_params):
    if not os.path.isfile(template_file):
        return None
    with open(template_file, encoding='utf-8') as f:
        template = Template(f.read())
        if template_params is not None:
            return template.render(**template_params)
        return template.render()


def get_template_folder(template_id, lang):
    return os.path.join(template_root, lang, template_id)


def get_html_output_filename(output_filename):
    filename = output_filename + '.html'
    return os.path.join(output_folder, 'html', filename)


def load_static_template_params(template_folder):
    static_template_params_filename = os.path.join(template_folder, 'params.json')
    if not os.path.isfile(static_template_params_filename):
        return {}
    with open(static_template_params_filename, encoding='utf-8') as static_template_params_file:
        return json.load(static_template_params_file)
