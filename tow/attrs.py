"""
TODO: add comments
"""
from modules import load_module


def process_attrs(env, attributes_path, name="default"):
    """ This method load attrs files and process attributes """
    mod = load_module(env, attributes_path, name)
    if mod:
        attr_names = [var for var in dir(mod) if not var.startswith("__")]
        return {attr_name: getattr(mod, attr_name) for attr_name in attr_names}
    return {}
