import sys
import importlib
import time
from types import ModuleType

import robot_control


def deep_reload(m: ModuleType):
    name = m.__name__  # get the name that is used in sys.modules
    name_ext = name + '.'  # support finding sub modules or packages

    def compare(loaded: str):
        return (loaded == name) or loaded.startswith(name_ext)

    all_mods = tuple(sys.modules)  # prevent changing iterable while iterating over it
    sub_mods = filter(compare, all_mods)
    for pkg in sorted(sub_mods, key=lambda item: item.count('.'), reverse=True):
        importlib.reload(sys.modules[pkg])  # reload packages, beginning with the most deeply nested


if __name__ == '__main__':
    while True:
        deep_reload(robot_control)
        print(robot_control.FOO)
        time.sleep(3.0)
