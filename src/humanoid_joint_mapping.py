
"""Robotics Lab - 16 Logical Joint Control Mapping.

This is a software-level mapping for PyBullet humanoid.urdf.
It is NOT the physical servo layout of Alpha 1S.

Axes X/Y/Z represent local Euler rotation components.
Revolute joints use a single scalar joint angle.

This file defines metadata only; it does not command motors.
"""

LOGICAL_JOINT_MAPPING = [
    {"id": 1, "name": "chest_x", "joint_id": 1,
     "joint_name": "chest", "type": "SPHERICAL", "axis": "X"},

    {"id": 2, "name": "neck_z", "joint_id": 2,
     "joint_name": "neck", "type": "SPHERICAL", "axis": "Z"},

    {"id": 3, "name": "right_shoulder_x", "joint_id": 3,
     "joint_name": "right_shoulder", "type": "SPHERICAL", "axis": "X"},

    {"id": 4, "name": "right_shoulder_z", "joint_id": 3,
     "joint_name": "right_shoulder", "type": "SPHERICAL", "axis": "Z"},

    {"id": 5, "name": "right_elbow", "joint_id": 4,
     "joint_name": "right_elbow", "type": "REVOLUTE", "axis": "SINGLE"},

    {"id": 6, "name": "left_shoulder_x", "joint_id": 6,
     "joint_name": "left_shoulder", "type": "SPHERICAL", "axis": "X"},

    {"id": 7, "name": "left_shoulder_z", "joint_id": 6,
     "joint_name": "left_shoulder", "type": "SPHERICAL", "axis": "Z"},

    {"id": 8, "name": "left_elbow", "joint_id": 7,
     "joint_name": "left_elbow", "type": "REVOLUTE", "axis": "SINGLE"},

    {"id": 9, "name": "right_hip_x", "joint_id": 9,
     "joint_name": "right_hip", "type": "SPHERICAL", "axis": "X"},

    {"id": 10, "name": "right_hip_y", "joint_id": 9,
     "joint_name": "right_hip", "type": "SPHERICAL", "axis": "Y"},

    {"id": 11, "name": "right_knee", "joint_id": 10,
     "joint_name": "right_knee", "type": "REVOLUTE", "axis": "SINGLE"},

    {"id": 12, "name": "right_ankle_x", "joint_id": 11,
     "joint_name": "right_ankle", "type": "SPHERICAL", "axis": "X"},

    {"id": 13, "name": "left_hip_x", "joint_id": 12,
     "joint_name": "left_hip", "type": "SPHERICAL", "axis": "X"},

    {"id": 14, "name": "left_hip_y", "joint_id": 12,
     "joint_name": "left_hip", "type": "SPHERICAL", "axis": "Y"},

    {"id": 15, "name": "left_knee", "joint_id": 13,
     "joint_name": "left_knee", "type": "REVOLUTE", "axis": "SINGLE"},

    {"id": 16, "name": "left_ankle_x", "joint_id": 14,
     "joint_name": "left_ankle", "type": "SPHERICAL", "axis": "X"},
]


def get_logical_joint(name):
    """Find a logical control field by its name."""
    for item in LOGICAL_JOINT_MAPPING:
        if item["name"] == name:
            return item
    raise ValueError(f"Unknown logical joint: {name}")


if __name__ == "__main__":
    print("=== Robotics Lab Logical Joint Mapping ===")

    for item in LOGICAL_JOINT_MAPPING:
        print(
            f"Logical={item['id']:02d} | "
            f"Name={item['name']:<20} | "
            f"Joint ID={item['joint_id']:02d} | "
            f"Type={item['type']:<9} | "
            f"Axis={item['axis']}"
        )

    print("Total Logical Fields:", len(LOGICAL_JOINT_MAPPING))
    print("=== Joint Mapping Loaded ===")
