"""
TODO: add comments
"""
import os
import shutil
from tow.modules import load_module
from tow.dockerfile import Dockerfile
from tow.attrs import process_attrs
from tow import templates


TOW_VOLUME = "/tow"


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


def dequote(s):
    """
    If a string has single or double quotes around it, remove them.
    Make sure the pair of quotes match.
    If a matching pair of quotes is not found, return the string unchanged.
    """
    if (s[0] == s[-1]) and s.startswith(("'", '"')):
        return s[1:-1]
    return s


def parse_env_arg(env_arg):
    if env_arg:
        env_pair = env_arg.split("=")
        if len(env_pair) < 2:
            return (env_pair[0], os.getenv(env_pair[0], ""))
        else:
            return (env_pair[0], dequote("".join(env_pair[1:])))


def parse_envfile(env_file_name):
    envs = []
    with open(env_file_name, "r") as envfile:
        for envfile_line in envfile.readlines():
            if not envfile_line.strip().startswith("#"):
                envs.append(parse_env_arg(envfile_line.strip()))
    return envs


def get_env_args(args):
    envs = {}

    i = 0
    while i < len(args):
        arg = args[i]
        if arg == "-e":
            i = i + 1
            (env_name, env_var) = parse_env_arg(args[i].strip())
            envs[env_name] = env_var
            i = i + 1
        elif arg == "--env":
            i = i + 1
            while i < len(args) and not args[i].startswith("-"):
                (env_name, env_var) = parse_env_arg(args[i].strip())
                envs[env_name] = env_var
                i = i + 1
        elif arg == "--env-file":
            i = i + 1
            env_file_name = args[i].strip()
            env_vars = parse_envfile(env_file_name)
            envs.update({env_var: env_name for (env_name, env_var) in env_vars})
            i = i + 1
        else:
            i = i + 1
    return envs


def copy_files(workingdir, files_path, file_mapping):
    for fm in file_mapping.mapping.get("files", []):
        src = fm[0]
        src_file_path = os.path.join(files_path, src)
        if os.path.exists(src_file_path):
            dst_file_path = os.path.join(workingdir, src)
            file_path_dir = os.path.dirname(dst_file_path)
            if not os.path.exists(file_path_dir):
                os.makedirs(file_path_dir)
            shutil.copy2(src_file_path, dst_file_path)


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
    for fm in file_mapping.mapping.get("templates", []):
        src = fm[0]
        src_template_path = os.path.join(templates_path, src)
        if os.path.exists(src_template_path):
            processed_template_path = os.path.join(workingdir, src)
            template_path_dir = os.path.dirname(processed_template_path)
            if not os.path.exists(template_path_dir):
                os.makedirs(template_path_dir)

            templates.process(os.path.dirname(src_template_path),
                              os.path.basename(src_template_path),
                              processed_template_path, attrs)

    copy_files(workingdir, files_path, file_mapping)

    # Transform dict with mapping to list of file tuples that exists in .tow dir
    handled_file_mapping = [fm for fm_list in file_mapping.mapping.values()
                            for fm in fm_list
                            if os.path.exists(os.path.join(workingdir, fm[0]))]

    # Init mapping file
    templates.process_template("mapping.sh.tmpl",
                            os.path.join(workingdir, "mapping.sh"),
                            {"mapping": handled_file_mapping,
                                "volume_name": TOW_VOLUME})

    return (handled_file_mapping, dockerfile, envs, attrs, workingdir)
