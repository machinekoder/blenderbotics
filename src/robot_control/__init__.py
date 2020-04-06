# -*- coding: utf-8 -*-

try:
    import bpy
    from . import panel
    from . import zmq_export
except ModuleNotFoundError:
    pass


def list_objects():
    for o in bpy.data.objects:
        print(o)


def register():
    print('register')
    panel.register()
    zmq_export.register()


def unregister():
    print('unregister')
    try:
        panel.unregister()
    except RuntimeError as e:
        print('error during unregistering {}'.format(e))
    zmq_export.unregister()


def main():
    pass
