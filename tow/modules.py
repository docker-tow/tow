"""
TODO: add comments
"""
import imp
import sys
import os


def load_module(env, module_path, name):
    """ This method load module file """
    module_file = os.path.join(module_path, "%s.py" % name)
    mod = None
    if os.path.exists(module_file):
        mod = imp.new_module(name)
        mod.__dict__.update({"env": env})
        sys.modules[name] = mod
        mod = imp.load_source(name, module_file)
    return mod
