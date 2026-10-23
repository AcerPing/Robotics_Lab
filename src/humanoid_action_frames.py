
"""Robotics Lab - Humanoid Action Frame definitions.

Data definitions only.
No GUI or physics simulation is executed by this file.
"""

ACTION_FRAMES = [
    {
        "frame_id": 1,
        "name": "Initial Pose",
        "duration": 2.0,
        "hold": 0.5,
        "joints": {
            "right_shoulder": {
                "joint_id": 3,
                "type": "SPHERICAL",
                "euler_deg": [0.0, 0.0, 0.0],
            },
            "right_elbow": {
                "joint_id": 4,
                "type": "REVOLUTE",
                "angle_deg": 0.0,
            },
        },
    },
    {
        "frame_id": 2,
        "name": "Raise Right Arm",
        "duration": 2.0,
        "hold": 0.5,
        "joints": {
            "right_shoulder": {
                "joint_id": 3,
                "type": "SPHERICAL",
                "euler_deg": [0.0, 0.0, 45.0],
            },
            "right_elbow": {
                "joint_id": 4,
                "type": "REVOLUTE",
                "angle_deg": 0.0,
            },
        },
    },
    
    {
        "frame_id": 3,
        "name": "Wave Right Arm - Bend",
        "duration": 1.0,
        "hold": 0.3,
        "joints": {
            "right_shoulder": {
                "joint_id": 3,
                "type": "SPHERICAL",
                "euler_deg": [0.0, 0.0, 45.0],
            },
            "right_elbow": {
                "joint_id": 4,
                "type": "REVOLUTE",
                "angle_deg": 30.0,
            },
        },
    },
    
    {
        "frame_id": 4,
        "name": "Wave Right Arm - Extend",
        "duration": 1.0,
        "hold": 0.3,
        "joints": {
            "right_shoulder": {
                "joint_id": 3,
                "type": "SPHERICAL",
                "euler_deg": [0.0, 0.0, 45.0],
            },
            "right_elbow": {
                "joint_id": 4,
                "type": "REVOLUTE",
                "angle_deg": 0.0,
            },
        },
    },
]


def get_action_frame(frame_id):
    """Return an Action Frame by its numeric ID."""
    for frame in ACTION_FRAMES:
        if frame["frame_id"] == frame_id:
            return frame

    raise ValueError(f"Unknown Action Frame ID: {frame_id}")


if __name__ == "__main__":
    print("=== Robotics Lab Action Frame Definitions ===")

    for frame in ACTION_FRAMES:
        print(
            f"Frame {frame['frame_id']:02d} | "
            f"{frame['name']} | "
            f"Duration={frame['duration']:.1f}s | "
            f"Hold={frame['hold']:.1f}s"
        )

    print("=== Action Frame Definitions Loaded ===")
