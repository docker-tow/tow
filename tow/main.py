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


def project_paths():
    current_dir = os.getcwd()
    return (current_dir,
            os.path.join(current_dir, "Dockerfile"),
            os.path.join(current_dir, "mapping.py"),
            os.path.join(current_dir, "templates"),
            os.path.join(current_dir, "files"),
            os.path.join(current_dir, "attributes"))


def prepare_workingdir(workingdir):
    if os.path.exists(workingdir):
        shutil.rmtree(workingdir, ignore_errors=True)

    os.mkdir(workingdir)


def copy_files(workingdir, files_path):
    for f in os.listdir(files_path):
        src_path = os.path.join(files_path, f)
        dst_path = os.path.join(workingdir, f)
        if os.isfile(src_path):
            shutil.copy2(src_path, dst_path)
        else:
            shutil.copytree(src_path, dst_path)


def init_tow():
    (current_dir, dockerfile_path,
     mappingfile_path, templates_path,
     files_path, attributes_path) = project_paths()

    mapping = __import__("mapping", {}, {}, ["mapping"])

    workingdir = os.path.join(current_dir, ".tow")

    prepare_workingdir(workingdir)

    dockerfile = Dockerfile(dockerfile_path)

    envs = dockerfile.envs()

    attrs = process_attrs(envs, attributes_path)

    print attrs
    # process templates
    for (src, dst) in mapping.mapping:
        src_tempalte_path = os.path.join(templates_path, src)
        processed_tempalte_path = os.path.join(workingdir, src)
        tempalte_path_dir = os.path.dirname(processed_tempalte_path)
        if os.path.exists(tempalte_path_dir):
            shutil.rmtree(tempalte_path_dir, ignore_errors=True)

        templates.process_template(src_tempalte_path, processed_tempalte_path, attrs)

    copy_files(workingdir, files_path)

    return (mapping, dockerfile, envs, attrs, workingdir)


def build_docker(args):
    (mapping, dockerfile, envs, attrs, workingdir) = init_tow()

    dockerfile.add_copy(mapping)
    dockerfile.save(os.path.join(workingdir, "Dockerfile"))

    build_args = " ".join(args[1:])
    subprocess.call("docker build %s %s" % (build_args, workingdir))


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
    else:
        # TODO: show usage
        pass
    sys.exit(0)
