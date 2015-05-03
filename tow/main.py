"""
This module contains tow `main` method.

`main` is executed as the command line ``tow`` program and takes care of
parsing options and commands, loading the user settings file
 and executing the commands given.

The other callables defined in this module are internal only.
"""

import sys
from version import version
from argparse import ArgumentParser
from commands.create import CreateCommand
from commands.build import BuildCommand
from commands.run import RunCommand

# don't create pyc files
sys.dont_write_bytecode = True


def main():
    """
    Main command-line execution loop
    """
    tow_parser = ArgumentParser(description="tow is configuration managment tool for docker containers", version=version)
    tow_subparsers = tow_parser.add_subparsers(help="tow commands", dest="command")

    commands = {}

    create_command = CreateCommand()
    create_command.add_parser(tow_subparsers)
    commands["create"] = create_command

    build_command = BuildCommand()
    build_command.add_parser(tow_subparsers)
    commands["build"] = build_command

    run_command = RunCommand()
    run_command.add_parser(tow_subparsers)
    commands["run"] = run_command

    if len(sys.argv) > 1:
        (namespace, args) = tow_parser.parse_known_args()

        if namespace.command not in commands:
                tow_parser.print_help()
        else:
            commands[namespace.command].command(namespace, args)
    else:
        tow_parser.print_help()
    sys.exit(0)
