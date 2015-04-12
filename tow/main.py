"""
This module contains tow `main` method.

`main` is executed as the command line ``tow`` program and takes care of
parsing options and commands, loading the user settings file
 and executing the commands given.

The other callables defined in this module are internal only.
"""

import sys
import os
import subprocess
import templates
import shutil
from dockerfile import Dockerfile
from attrs import process_attrs
from modules import load_module
from utils import prepare_workingdir
from utils import copy_files
from utils import get_env_args
from utils import TOW_VOLUME
from utils import project_paths


def init_tow(env_args={}):
    (current_dir, dockerfile_path,
     mappingfile_path, templates_path,
     files_path, attributes_path) = project_paths()

    file_mapping = load_module({}, current_dir, "mapping")

    workingdir = os.path.join(current_dir, ".tow")

    prepare_workingdir(workingdir)

    dockerfile = Dockerfile(dockerfile_path)

    envs = dockerfile.envs()
    # envs passed as params has more priority then Dockerfile envs
    envs.update(env_args)
    attrs = process_attrs(envs, attributes_path)

    # process templates
    for (src, dst) in file_mapping.mapping:
        src_template_path = os.path.join(templates_path, src)
        if os.path.exists(src_template_path):
            processed_template_path = os.path.join(workingdir, src)
            template_path_dir = os.path.dirname(processed_template_path)
            if template_path_dir != workingdir:
                if os.path.exists(template_path_dir):
                    shutil.rmtree(template_path_dir, ignore_errors=True)

                os.mkdirs(template_path_dir)
            templates.process(os.path.dirname(src_template_path), os.path.basename(src_template_path), processed_template_path, attrs)

    copy_files(workingdir, files_path)

    handled_file_mapping = [(src, dst) for (src, dst) in file_mapping.mapping
                            if os.path.exists(os.path.join(workingdir, src))]

    return (handled_file_mapping, dockerfile, envs, attrs, workingdir)


def run_docker(args):
    if "--tow-help" in args:
        print "Usage: tow run [TOW-OPTIONS] [DOCKER-OPTIONS]"
        print "Run docker container. If you built it with --tow-run option all you new configurations will be applied to instance"
        print "All docker run agruments will be passed to docker run command"
        return

    env_args = get_env_args(args)
    (file_mapping, dockerfile, envs, attrs, workingdir) = init_tow(env_args)

    build_args = " ".join(args[1:])
    build_cmd = "docker run %s %s" % ("-v %s:/tow" % workingdir, build_args)
    try:
        subprocess.call([cmd for cmd in build_cmd.split(" ") if cmd])
    except OSError as e:
        if e.errno == os.errno.ENOENT:
            print "ERORR: Please install docker and run tow again"


def build_docker(args):
    if "--tow-help" in args:
        print "Usage: tow build <name of project> [TOW-OPTIONS] [DOCKER-OPTIONS]"
        print "Build command use for building docker container with processed configs and files by tow"
        print "All docker build agruments will be passed to docker buld command"
        print "\t--tow-run - patch docker file in order to use configuration in run phase"
        return

    (file_mapping, dockerfile, envs, attrs, workingdir) = init_tow()
    #  Check if you would like to patch Dockerfile in order to use reconfiguration on run phase
    if "--tow-run" in args:
        (entrypoint, cmd) = dockerfile.find_entrypoint_or_cmd()
        templates.process_template("tow.sh.tmpl",
                                   os.path.join(workingdir, "tow.sh"),
                                   {"entrypoint": entrypoint,
                                    "cmd": cmd, "mapping": file_mapping,
                                    "volume_name": TOW_VOLUME})
        file_mapping.append(("tow.sh", "/tow.sh"))
        dockerfile.replace_entrypoint_or_cmd_by_tow_cmd("sh /tow.sh")

    dockerfile.add_copy([(src, dst) for (src, dst) in file_mapping
                         if os.path.exists(os.path.join(workingdir, src))])
    dockerfile.save(os.path.join(workingdir, "Dockerfile"))

    build_args = " ".join([arg for arg in args[1:] if arg != "--tow-run"])
    build_cmd = "docker build %s %s" % (build_args, workingdir)
    try:
        subprocess.call([command for command in build_cmd.split(" ") if command])
    except OSError as e:
        if e.errno == os.errno.ENOENT:
            print "ERORR: Please install docker and run tow again"


def create_project(args):
    """
    Generate tow project structure
    """
    if len(args) < 2:
        raise "Specify project name"
    project_name = args[1]
    for dir_name in ["attributes", "files", "templates"]:
        os.makedirs(os.path.join(project_name, dir_name))
    for file_name in ["Dockerfile", "mapping.py"]:
        templates.process_template("%s.tmpl" % file_name,
                                   os.path.join(project_name, file_name), {})


def usage():
    """
        Print out how to use tow
    """
    print "tow is configuration managment tool for docker containers"
    print "Usage: tow COMMAND [TOW-OPTIONS] [DOCKER-OPTIONS]"
    print "Commands:"
    print """\tbuild - process attributes and tamplates path Dockerfile
            according mapping and run docker build with DOCKER-OPTIONS"""
    print """\trun - if tow build was without --tow-run option than call docker run
                else process attributes and tempaltes mount /tow volume and
                run docker run with DOCKER-OPTIONS"""
    print """TOW-OPTIONS - every tow command has it own options for more
            information run tow COMMAND --tow-help"""
    print """DOCKER-OPTIONS - options for docker buid or run command"""


def main():
    """
    Main command-line execution loop
    """
    args = sys.argv[1:]
    if args:
        action = args[0]
        if action == "create":
            create_project(args)
        elif action == "build":
            build_docker(args)
        elif action == "run":
            run_docker(args)
    else:
        usage()
    sys.exit(0)
