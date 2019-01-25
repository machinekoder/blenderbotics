# -*- coding: utf-8 -*-
from .export import export_animation
from .zmq_export import send_data

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
    # bpy.app.timers.register(timer_task)


def unregister():
    print('unregister')
    # bpy.app.timers.unregister(timer_task)


def main():
    data = export_animation()
    send_data(data)
