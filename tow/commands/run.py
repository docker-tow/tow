"""
TODO: add comments
"""
from command import Command
from tow.utils import TOW_VOLUME


class RunCommand(Command):

    def add_parser(self, subparsers):
        super(RunCommand, self).add_parser(subparsers)
        parser = subparsers.add_parser("run",
                                       help="run docker container if tow build was without --tow-run option than call docker run else process attributes and tempaltes mount /tow volume and run docker run with DOCKER-OPTIONS")
        return parser

    def command(self, namespace, args):
        print "Run", namespace, args
        print "Volume", TOW_VOLUME
