# -*- coding: utf-8 -*-
# https://blender.stackexchange.com/q/57306/3710
# https://blender.stackexchange.com/q/79779/3710

#
# modified for blender 2.80
import bpy

from bpy.props import (
    StringProperty,
    BoolProperty,
    IntProperty,
    FloatProperty,
    FloatVectorProperty,
    EnumProperty,
    PointerProperty,
)
from bpy.types import Panel, PropertyGroup


bl_info = {
    "name": "Add-on Template",
    "description": "",
    "author": "",
    "version": (0, 0, 2),
    "blender": (2, 80, 0),
    "location": "3D View > Tools",
    "warning": "",  # used for warning icon and text in addons panel
    "wiki_url": "",
    "tracker_url": "",
    "category": "Development",
}


# ------------------------------------------------------------------------
#    store properties in the active scene
# ------------------------------------------------------------------------


class RobotControlProperties(PropertyGroup):

    my_bool: BoolProperty(
        name="Enable or Disable", description="A bool property", default=False
    )

    my_int: IntProperty(
        name="Int Value", description="A integer property", default=23, min=10, max=100
    )

    my_float: FloatProperty(
        name="Float Value",
        description="A float property",
        default=23.7,
        min=0.01,
        max=30.0,
    )

    my_float_vector: FloatVectorProperty(
        name="Float Vector Value",
        description="Something",
        default=(0.0, 0.0, 0.0),
        min=0.0,  # float
        max=0.1,
    )

    my_string: StringProperty(
        name="User Input", description=":", default="", maxlen=1024
    )

    my_enum: EnumProperty(
        name="Dropdown:",
        description="Apply Data to attribute.",
        items=[
            ('OP1', "Option 1", ""),
            ('OP2', "Option 2", ""),
            ('OP3', "Option 3", ""),
        ],
    )


# ------------------------------------------------------------------------
#    operators
# ------------------------------------------------------------------------


class HelloWorldOperator(bpy.types.Operator):
    bl_idname = "wm.hello_world"
    bl_label = "Print Values Operator"

    def execute(self, context):
        scene = context.scene
        mytool = scene.my_tool

        # print the values to the console
        print("Hello World")
        print("bool state:", mytool.my_bool)
        print("int value:", mytool.my_int)
        print("float value:", mytool.my_float)
        print("string value:", mytool.my_string)
        print("enum state:", mytool.my_enum)

        return {'FINISHED'}


# ------------------------------------------------------------------------
#    menus
# ------------------------------------------------------------------------


class BasicMenu(bpy.types.Menu):
    bl_idname = "OBJECT_MT_select_test"
    bl_label = "Select"

    def draw(self, context):
        layout = self.layout

        # built-in example operators
        layout.operator(
            "object.select_all", text="Select/Deselect All"
        ).action = 'TOGGLE'
        layout.operator("object.select_all", text="Inverse").action = 'INVERT'
        layout.operator("object.select_random", text="Random")


# ------------------------------------------------------------------------
#    my tool in objectmode
# ------------------------------------------------------------------------


class OBJECT_PT_my_panel(Panel):
    bl_idname = "OBJECT_PT_robot_control_panel"
    bl_label = "My Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Tools"
    #    bl_category = 'View'
    bl_context = "objectmode"

    @classmethod
    def poll(cls, context):
        return context.object is not None

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool

        layout.prop(mytool, "my_bool")
        layout.prop(mytool, "my_enum", text="")
        layout.prop(mytool, "my_int")
        layout.prop(mytool, "my_float")
        layout.prop(mytool, "my_float_vector", text="")
        layout.prop(mytool, "my_string")
        layout.operator("wm.hello_world")
        layout.menu("OBJECT_MT_select_test", text="Presets", icon="SCENE")


# ------------------------------------------------------------------------
# register and unregister
# ------------------------------------------------------------------------


def register():
    bpy.utils.register_class(RobotControlProperties)
    bpy.types.Scene.my_tool = PointerProperty(type=RobotControlProperties)
    #
    bpy.utils.register_class(OBJECT_PT_my_panel)
    bpy.utils.register_class(HelloWorldOperator)
    bpy.utils.register_class(BasicMenu)


def unregister():
    bpy.utils.unregister_class(BasicMenu)
    bpy.utils.unregister_class(HelloWorldOperator)
    bpy.utils.unregister_class(OBJECT_PT_my_panel)
    #
    bpy.utils.unregister_class(RobotControlProperties)
    del bpy.types.Scene.my_tool


if __name__ == "__main__":
    register()
