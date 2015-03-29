"""
TODO: add comments
"""
import imp
import sys
import os


def process_attrs(env, attributes_path, name="dafault"):
    """ This method load attrs files and process attributes """

    mod = imp.new_module(name)
    mod.__dict__.update({"env": env})
    sys.modules[name] = mod
    mod = imp.load_source(name, os.path.join(attributes_path, "%s.py" % name))
    attr_names = [var for var in dir(mod) if not var.startswith("__")]
    return {attr_name: getattr(mod, attr_name) for attr_name in attr_names}
