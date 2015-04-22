"""
TODO: add comments
"""
from command import Command
from utils import init_tow
from utils import get_env_args
from tow import templates
import subprocess
from utils import TOW_VOLUME


class RunCommand(Command):

    def add_parser(self, subparsers):
        super(RunCommand, self).add_parser(subparsers)
        parser = subparsers.add_parser("run",
                                       help="run docker container if tow build was without --tow-run option than call docker run else process attributes and tempaltes mount /tow volume and run docker run with DOCKER-OPTIONS")
        return parser

    def command(self, namespace, args):
        env_args = get_env_args(args)
        (file_mapping, dockerfile, envs, attrs, workingdir) = init_tow(env_args)

        try:
            subprocess.call(["docker", "run", "-v", "%s:%s" % (workingdir, TOW_VOLUME)] + args)
        except OSError as e:
            if e.errno == os.errno.ENOENT:
                print "ERORR: Please install docker and run tow again"
