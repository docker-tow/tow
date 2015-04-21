"""
TODO: add comments
"""
from command import Command
from tow import templates
import os
from datetime import date


class CreateCommand(Command):

    def add_parser(self, subparsers):
        super(CreateCommand, self).add_parser(subparsers)
        parser = subparsers.add_parser("create",
                                       help="Create tow project in current directory")
        parser.add_argument("project_name", type=str,
                            help="name of tow project")

    def command(self, namespace, args):
        project_name = namespace.project_name
        for dir_name in ["attributes", "files", "templates"]:
            os.makedirs(os.path.join(project_name, dir_name))
        for file_name in ["Dockerfile", "mapping.py", "attributes/default.py"]:
            templates.process_template("%s.tmpl" % os.path.basename(file_name),
                                    os.path.join(project_name, file_name),
                                    {"current_year": date.today().year,
                                        "project_name": project_name})
