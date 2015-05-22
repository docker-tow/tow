"""
TODO: add comments
"""
from command import Command
from utils import init_tow
from utils import get_env_args
from utils import get_linked_container_variables


class ProcessCommand(Command):

    def add_parser(self, subparsers):
        super(ProcessCommand, self).add_parser(subparsers)
        parser = subparsers.add_parser("process",
                                       help="process configuration like in tow run but don't run docker")
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
