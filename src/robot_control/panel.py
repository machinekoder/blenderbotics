# -*- coding: utf-8 -*-
# https://blender.stackexchange.com/q/57306/3710
# https://blender.stackexchange.com/q/79779/3710

#
# modified for blender 2.80
import bpy

from bpy.props import StringProperty, BoolProperty, FloatProperty, PointerProperty
from bpy.types import Panel, Operator, PropertyGroup

from .export import (
    export_animation,
    current_joints,
    write_bone_positions,
    read_bone_positions,
)
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
# Timer
# ------------------------------------------------------------------------


def read_joint_positions():
    read_bone_positions(current_joints)
    robot_tool = bpy.context.scene.robot_tool

    for i, joint in enumerate(current_joints):
        setattr(robot_tool, 'joint_{}_position'.format(i + 1), joint.position)

    if not robot_tool.enable_ik:
        return None
    else:
        return 0.1


def start_reading_joint_positions():
    bpy.app.timers.register(read_joint_positions)


def stop_reading_joint_positions():
    try:
        bpy.app.timers.unregister(read_joint_positions)
    except ValueError:
        pass


# ------------------------------------------------------------------------
#    store properties in the active scene
# ------------------------------------------------------------------------


def ik_enable_property_update(group, context):
    pose = bpy.data.objects["Armature"].pose
    constraints = pose.bones["Gripper Core Bone"].constraints
    if not group.enable_ik:
        constraint = constraints["IK"]
        constraints.remove(constraint)
        stop_reading_joint_positions()
        # TODO: update panel joint limits
    else:
        constraint = constraints.new("IK")
        constraint.target = context.scene.objects['Target']
        constraint.use_rotation = True
        start_reading_joint_positions()


def open_gripper_update(group, context):
    pose = bpy.data.objects["Armature"].pose
    pose.bones["Gripper L Bone"].location[2] = 0.0 if group.open_gripper else 0.017


def joint_position_update(group, _context, index):
    current_joints[index - 1].position = getattr(
        group, 'joint_{}_position'.format(index)
    )
    write_bone_positions(current_joints)


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

    zmq_send_address: StringProperty(
        name="Send Address",
        description="Address of the blender2ros ZMQ service",
        default="tcp://127.0.0.1:12348",
        maxlen=1024,
    )

    zmq_recv_address: StringProperty(
        name="Receive Address",
        description="Address of the blender2ros ZMQ service",
        default="tcp://127.0.0.1:12349",
        maxlen=1024,
    )

    joint_1_position: FloatProperty(
        name="Joint 1",
        description="Position of Joint 1",
        default=0.0,
        unit='ROTATION',
        subtype='ANGLE',
        update=lambda group, context: joint_position_update(group, context, 1),
    )

    joint_2_position: FloatProperty(
        name="Joint 2",
        description="Position of Joint 2",
        default=0.0,
        unit='ROTATION',
        subtype='ANGLE',
        update=lambda group, context: joint_position_update(group, context, 2),
    )

    joint_3_position: FloatProperty(
        name="Joint 3",
        description="Position of Joint 3",
        default=0.0,
        unit='ROTATION',
        subtype='ANGLE',
        update=lambda group, context: joint_position_update(group, context, 3),
    )

    joint_4_position: FloatProperty(
        name="Joint 4",
        description="Position of Joint 4",
        default=0.0,
        unit='ROTATION',
        subtype='ANGLE',
        update=lambda group, context: joint_position_update(group, context, 4),
    )

    joint_5_position: FloatProperty(
        name="Joint 5",
        description="Position of Joint 5",
        default=0.0,
        unit='ROTATION',
        subtype='ANGLE',
        update=lambda group, context: joint_position_update(group, context, 5),
    )

    joint_6_position: FloatProperty(
        name="Joint 6",
        description="Position of Joint 6",
        default=0.0,
        unit='ROTATION',
        subtype='ANGLE',
        update=lambda group, context: joint_position_update(group, context, 6),
    )


# ------------------------------------------------------------------------
#    operators
# ------------------------------------------------------------------------


class ExecuteTrajectoryOperator(Operator):
    bl_idname = "wm.execute_trajectory"
    bl_label = "Execute Trajectory"

    def execute(self, context):
        scene = context.scene

        # print the values to the console
        print("Executing trajectory")
        data = export_animation()
        send_data(data)

        # play the animation
        scene.frame_set(0)
        bpy.ops.screen.animation_play()

        return {'FINISHED'}


class SetHomePoseOperator(Operator):
    bl_idname = "wm.set_home_pose"
    bl_label = "Set Home Pose"

    def execute(self, context):
        robot_tool = context.scene.robot_tool

        for j in current_joints:
            j.position = 0.0
        write_bone_positions(current_joints)
        for i, joint in enumerate(current_joints):
            setattr(robot_tool, 'joint_{}_position'.format(i + 1), joint.position)

        marker = bpy.data.objects['Target Marker']
        local_pose = bpy.data.objects["Armature"].pose.bones["Gripper Core Bone"].tail
        marker.location = bpy.data.objects["Armature"].matrix_world @ local_pose

        return {'FINISHED'}


# ------------------------------------------------------------------------
#    menus
# ------------------------------------------------------------------------


# ------------------------------------------------------------------------
#    my tool in objectmode
# ------------------------------------------------------------------------


class OBJECT_PT_robot_control_panel(Panel):
    bl_idname = "OBJECT_PT_robot_control_panel"
    bl_label = "Joints"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Robot Control"
    bl_context = "objectmode"

    @classmethod
    def poll(cls, context):
        return context.object is not None

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        robot_tool = scene.robot_tool

        # flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=True, align=False)
        # col = flow.column()

        layout.prop(robot_tool, "enable_ik")
        layout.label(text="Joint Positions")
        for i in range(6, 0, -1):
            layout.prop(robot_tool, "joint_{}_position".format(i))
        layout.operator("wm.set_home_pose")
        layout.label(text="Actions")
        layout.operator("wm.execute_trajectory")


class OBJECT_PT_gripper_panel(Panel):
    bl_idname = "OBJECT_PT_gripper_panel"
    bl_label = "Gripper"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Robot Control"
    bl_context = "objectmode"

    @classmethod
    def poll(cls, context):
        return context.object is not None

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        robot_tool = scene.robot_tool

        layout.prop(robot_tool, "open_gripper")


class OBJECT_PT_connection_panel(Panel):
    bl_idname = "OBJECT_PT_connection_panel"
    bl_label = "ZMQ Connection"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Robot Control"
    bl_context = "objectmode"

    @classmethod
    def poll(cls, context):
        return context.object is not None

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        robot_tool = scene.robot_tool

        layout.prop(robot_tool, "zmq_send_address")
        layout.prop(robot_tool, "zmq_recv_address")


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


# ------------------------------------------------------------------------
# register and unregister
# ------------------------------------------------------------------------


def register():
    bpy.utils.register_class(RobotControlProperties)
    bpy.types.Scene.robot_tool = PointerProperty(type=RobotControlProperties)
    #
    bpy.utils.register_class(OBJECT_PT_robot_control_panel)
    bpy.utils.register_class(OBJECT_PT_gripper_panel)
    bpy.utils.register_class(OBJECT_PT_connection_panel)
    bpy.utils.register_class(ExecuteTrajectoryOperator)
    bpy.utils.register_class(SetHomePoseOperator)
    # stop at last frame
    # bpy.app.handlers.frame_change_pre.append(stop_playback)


def unregister():
    bpy.utils.unregister_class(ExecuteTrajectoryOperator)
    bpy.utils.unregister_class(SetHomePoseOperator)
    bpy.utils.unregister_class(OBJECT_PT_robot_control_panel)
    bpy.utils.unregister_class(OBJECT_PT_gripper_panel)
    bpy.utils.unregister_class(OBJECT_PT_connection_panel)
    #
    bpy.utils.unregister_class(RobotControlProperties)
    del bpy.types.Scene.robot_tool
    # stop at last frame
    # if stop_playback in bpy.app.handlers.frame_change_pre:
    #     bpy.app.handlers.frame_change_pre.remove(stop_playback)


if __name__ == "__main__":
    register()
