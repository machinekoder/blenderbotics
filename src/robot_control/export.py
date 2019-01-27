# -*- coding: utf-8 -*-
import copy
from math import pi

import bpy

from .joint import Joint


current_joints = [
    Joint(offset=0.0, axis=2, scale=1.0),
    Joint(offset=0.0, axis=1, scale=1.0),
    Joint(offset=(pi / 2), axis=1, scale=1.0),
    Joint(offset=0.0, axis=2, scale=1.0),
    Joint(offset=0.0, axis=1, scale=1.0),
    Joint(offset=0.0, axis=2, scale=1.0),
]


def get_pose_bone_matrix(pose_bone):
    local_matrix = pose_bone.matrix_channel.to_3x3()
    if pose_bone.parent is None:
        return local_matrix
    else:
        return pose_bone.parent.matrix_channel.to_3x3().inverted() @ local_matrix


def read_bone_positions(joints):
    armature = bpy.data.objects["Armature"]
    for i, joint in enumerate(joints):
        pose_bone = armature.pose.bones['Joint {}'.format(i + 1)]
        matrix = get_pose_bone_matrix(pose_bone)
        joint.raw_position = (matrix.to_euler()[joint.axis]) * joint.scale
    # link rotation
    # bpy.data.objects['Link 6'].rotation_euler


def write_bone_positions(joints):
    armature = bpy.data.objects["Armature"]
    for i, joint in enumerate(joints):
        pose_bone = armature.pose.bones['Joint {}'.format(i + 1)]
        for j in range(3):
            if pose_bone.lock_rotation[j]:
                continue
            pose_bone.rotation_euler[j] = joint.raw_position


def calculate_velocities(current, last, t):
    for i, joint in enumerate(current):
        joint.velocity = (joint.position - last[i].position) / t


def print_joints(joints, timestamp):
    print(
        '{:.2f} '.format(timestamp)
        + ' '.join('{:.2f},{:.2f}'.format(j.position, j.velocity) for j in joints)
    )


def export_animation():
    scene = bpy.context.scene
    previous_frame = scene.frame_current

    def add_data(joints):
        data.append(
            dict(
                time_from_start=current_time,
                joints=[dict(pos=j.position, vel=j.velocity) for j in joints],
            )
        )

    fps = scene.render.fps
    t = 1 / fps
    data = []
    for frame in range(scene.frame_end + 1):
        current_time = frame / fps
        scene.frame_set(frame)
        last_joints = copy.deepcopy(current_joints)
        read_bone_positions(current_joints)
        calculate_velocities(current_joints, last_joints, t)
        add_data(current_joints)

    # velocity of first and last trajectory point must be 0.0
    for j in data[0]['joints']:
        j['vel'] = 0.0
    for j in data[-1]['joints']:
        j['vel'] = 0.0

    # restore context
    scene.frame_set(previous_frame)

    return data
