"""
TODO: add comments
"""
from command import Command


class BuildCommand(Command):

    def add_parser(self, subparsers):
        super(BuildCommand, self).add_parser(subparsers)
        parser = subparsers.add_parser("build",
                                       help="process attributes and tamplates path Dockerfile according mapping and run docker build with DOCKER-OPTIONS")
        parser.add_argument("--tow-run", action="store_true",
                            help="patch docker file in order to use configuration in run phase")

    def command(self, namespace, args):
        print "Build", namespace, args
