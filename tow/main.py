"""
This module contains tow `main` method.

`main` is executed as the command line ``tow`` program and takes care of
parsing options and commands, loading the user settings file
 and executing the commands given.

The other callables defined in this module are internal only.
"""

import sys
import os


def create_project(args):
    """
    Generate tow project structure
    """
    if len(args) < 2:
        raise "Specify project name"
    project_name = args[1]
    for dir_name in ["attributes", "files", "configs", "templates"]:
        os.makedirs(os.path.join(project_name, dir_name))
    for file_name in ["Dockerfile", "mapping.json"]:
        open(os.path.join(project_name, file_name), "a").close()  # TODO: create it form template


def main():
    """
    Main command-line execution loop
    """
    args = sys.argv[1:]
    if args:
        action = args[0]
        if action == "create":
            create_project(args)
    else:
        # TODO: show usage
        pass
    sys.exit(0)
