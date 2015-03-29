"""
This module contains tow process template method and templates itself.

"""

import jinja2
import os


def process(template_path, template_name, result_file_path, context):
    """
    Process template
    """
    loader = jinja2.FileSystemLoader(template_path)
    jinja_env = jinja2.Environment(loader=loader)
    template = jinja_env.get_template(template_name)
    result = template.render(context)

    with open(result_file_path, "w+") as f:
        f.write(result)


def process_template(template_name, result_file_path, context):
    """
    Process template form templates folder
    """
    template_path = os.path.dirname(os.path.abspath(__file__))
    process(template_path, template_name, result_file_path, context)
