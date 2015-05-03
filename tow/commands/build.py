"""
TODO: add comments
"""
from command import Command
from utils import init_tow
from tow import templates
import subprocess
from utils import TOW_VOLUME
import os


class BuildCommand(Command):

    def add_parser(self, subparsers):
        super(BuildCommand, self).add_parser(subparsers)
        parser = subparsers.add_parser("build",
                                       help="process attributes and tamplates path Dockerfile according mapping and run docker build with DOCKER-OPTIONS")
        parser.add_argument("--tow-run", action="store_true",
                            help="patch docker file in order to use configuration in run phase")
        parser.add_argument("--tow-attrs", type=str, default="default",
                            help="specify name of attribute file in attributes folder. Default value: default. Example --tow-attrs prod")
        parser.add_argument("--tow-mapping", type=str, default="mapping",
                            help="specify name of mapping variable in mapping.py. Default value:mapping. Example --tow-mapping prod")

    def command(self, namespace, args):
        """
            This is build command. Prepare workingdir(.tow) and run docker build
        """
        (file_mapping, dockerfile, envs, attrs, workingdir) = init_tow(attributes_name=namespace.tow_attrs,
                                                                       mapping_name=namespace.tow_mapping)
        #  Check if you would like to patch Dockerfile in order to use
        #  reconfiguration on run phase
        if namespace.tow_run:
            (entrypoint, cmd) = dockerfile.find_entrypoint_or_cmd()
            templates.process_template("tow.sh.tmpl",
                                       os.path.join(workingdir, "tow.sh"),
                                       {"entrypoint": entrypoint,
                                        "cmd": cmd, "mapping": file_mapping,
                                        "volume_name": TOW_VOLUME})
            file_mapping.append(("tow.sh", "/tow.sh"))
            dockerfile.replace_entrypoint_or_cmd_by_tow_cmd("sh /tow.sh")
        dockerfile.add_copy(file_mapping)
        dockerfile.save(os.path.join(workingdir, "Dockerfile"))

        try:
            subprocess.call(["docker", "build"] + args + [workingdir])
        except OSError as e:
            if e.errno == os.errno.ENOENT:
                print "ERORR: Please install docker and run tow again"
