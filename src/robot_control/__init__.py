# -*- coding: utf-8 -*-
from robot_control import panel

try:
    import bpy
except ModuleNotFoundError:
    pass


def list_objects():
    for o in bpy.data.objects:
        print(o)


# def timer_task():
#     read_bone_positions(current_joints)
#     return 0.1


def register():
    print('register')
    panel.register()
    # bpy.app.timers.register(timer_task)


def unregister():
    print('unregister')
    try:
        panel.unregister()
    except RuntimeError as e:
        print('error during unregistering {}'.format(e))
    # bpy.app.timers.unregister(timer_task)


def main():
    pass
