"""
TODO: add comments
"""
from command import Command
from utils import init_tow
from utils import get_env_args
from utils import get_linked_container_variables
import subprocess
import os
from utils import TOW_VOLUME


class RunCommand(Command):

    def add_parser(self, subparsers):
        super(RunCommand, self).add_parser(subparsers)
        parser = subparsers.add_parser("run",
                                       help="run docker container if tow build was without --tow-run option than call docker run else process attributes and tempaltes mount /tow volume and run docker run with DOCKER-OPTIONS")
        parser.add_argument("--tow-attrs", type=str, default="default",
                            help="specify name of attribute file in attributes folder. Default value: default. Example --tow-attrs prod")
        parser.add_argument("--tow-mapping", type=str, default="mapping",
                            help="specify name of mapping variable in mapping.py. Default value:mapping. Example --tow-mapping prod")

    def command(self, namespace, args):
        linked_envs = get_linked_container_variables(args)
        env_args = get_env_args(args)
        env_args.update(linked_envs)
        (file_mapping, dockerfile, envs, attrs, workingdir) = init_tow(env_args=env_args,
                                                                       attributes_name=namespace.tow_attrs,
                                                                       mapping_name=namespace.tow_mapping)

        try:
            subprocess.call(["docker", "run", "-v", "%s:%s" % (workingdir, TOW_VOLUME)] + args)
        except OSError as e:
            if e.errno == os.errno.ENOENT:
                print "ERORR: Please install docker and run tow again"
