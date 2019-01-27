# -*- coding: utf-8 -*-
# https://blender.stackexchange.com/q/57306/3710
# https://blender.stackexchange.com/q/79779/3710

#
# modified for blender 2.80
import bpy

from bpy.props import StringProperty, BoolProperty, PointerProperty
from bpy.types import Panel, Operator, PropertyGroup

from .export import export_animation
from .zmq_export import send_data

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


def ik_enable_property_update(group, context):
    pose = bpy.data.objects["Armature"].pose
    constraints = pose.bones["Gripper Core Bone"].constraints
    if not group.enable_ik:
        constraint = constraints["IK"]
        constraints.remove(constraint)
    else:
        constraint = constraints.new("IK")
        constraint.target = context.scene.objects['Target 2 Helper']
        constraint.use_rotation = True
    # pose.bones["Gripper Core Bone"].constraints["IK"].mute = not group.enable_ik
    context.scene.update()


def open_gripper_update(group, context):
    pose = bpy.data.objects["Armature"].pose
    pose.bones["Gripper L Bone"].location[2] = 0.025 if group.open_gripper else 0.0
    context.scene.update()


class RobotControlProperties(PropertyGroup):

    enable_ik: BoolProperty(
        name="Enable IK",
        description="Enables Inverse Kinematics",
        default=True,
        update=ik_enable_property_update,
    )

    open_gripper: BoolProperty(
        name="Open Gripper",
        description="Opens the robot gripper",
        default=True,
        update=open_gripper_update,
    )

    zmq_address: StringProperty(
        name="ZMQ Address",
        description="Address of the blender2ros ZMQ service",
        default="tcp://127.0.0.1:12348",
        maxlen=1024,
    )


# ------------------------------------------------------------------------
#    operators
# ------------------------------------------------------------------------


class ExecuteTrajectoryOperator(Operator):
    bl_idname = "wm.execute_trajectory"
    bl_label = "Execute Trajectory"

    def execute(self, context):
        scene = context.scene
        robot_tool = scene.robot_tool

        # print the values to the console
        print("Executing trajectory")
        data = export_animation()
        send_data(data, address=robot_tool.zmq_address)

        # play the animation
        scene.frame_set(0)
        bpy.ops.screen.animation_play()

        return {'FINISHED'}


# ------------------------------------------------------------------------
#    menus
# ------------------------------------------------------------------------


# ------------------------------------------------------------------------
#    my tool in objectmode
# ------------------------------------------------------------------------


class OBJECT_PT_robot_control_panel(Panel):
    bl_idname = "OBJECT_PT_robot_control_panel"
    bl_label = "Robot Control"
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
        robot_tool = scene.robot_tool

        layout.prop(robot_tool, "enable_ik")
        layout.prop(robot_tool, "open_gripper")
        layout.prop(robot_tool, "zmq_address")
        layout.operator("wm.execute_trajectory")
        # layout.menu("OBJECT_MT_select_test", text="Presets", icon="SCENE")


# ------------------------------------------------------------------------
# Playback
# ------------------------------------------------------------------------


def stop_playback(scene):
    if scene.frame_current == scene.frame_end:
        bpy.ops.screen.animation_cancel(restore_frame=False)


# or restore frames:
def stop_playback_restore(scene):
    if scene.frame_current == scene.frame_end:
        bpy.ops.screen.animation_cancel(restore_frame=True)


# add one of these functions to frame_change_pre handler:
bpy.app.handlers.frame_change_pre.append(stop_playback)

# ------------------------------------------------------------------------
# register and unregister
# ------------------------------------------------------------------------


def register():
    bpy.utils.register_class(RobotControlProperties)
    bpy.types.Scene.robot_tool = PointerProperty(type=RobotControlProperties)
    #
    bpy.utils.register_class(OBJECT_PT_robot_control_panel)
    bpy.utils.register_class(ExecuteTrajectoryOperator)
    # stop at last frame
    # bpy.app.handlers.frame_change_pre.append(stop_playback)


def unregister():
    bpy.utils.unregister_class(ExecuteTrajectoryOperator)
    bpy.utils.unregister_class(OBJECT_PT_robot_control_panel)
    #
    bpy.utils.unregister_class(RobotControlProperties)
    del bpy.types.Scene.robot_tool
    # stop at last frame
    # if stop_playback in bpy.app.handlers.frame_change_pre:
    #     bpy.app.handlers.frame_change_pre.remove(stop_playback)


if __name__ == "__main__":
    register()
