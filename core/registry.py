import os
import sys
from importlib.machinery import SourceFileLoader

FUNCTIONS = {}


def get_base_path():
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    return os.path.abspath(".")


def load_plugins():
    base_path = get_base_path()
    plugin_dir = os.path.join(base_path, "plugins")

    for file in os.listdir(plugin_dir):
        if file.endswith(".py") and file != "__init__.py":

            key = file[:-3]
            file_path = os.path.join(plugin_dir, file)

            # ⭐ 关键：从文件直接加载
            module = SourceFileLoader(key, file_path).load_module()

            if hasattr(module, "run"):
                FUNCTIONS[key] = {
                    "name": getattr(module, "NAME", key),
                    "category": getattr(module, "CATEGORY", "uncategorized"),
                    "desc": getattr(module, "DESC", ""),
                    "func": module.run,
                    "meta": getattr(module, "META", {"params": []})
                }


                