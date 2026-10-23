
"""Robotics Lab - Action Frame GUI Controller.

Frame 01 -> Frame 02
Initial Pose -> Raise Right Arm

PyBullet GUI simulation with Smoothstep interpolation.
"""

import math
import time

import pybullet as p
import pybullet_data

from humanoid_action_frames import get_action_frame


FPS = 240
RIGHT_SHOULDER = 3
RIGHT_ELBOW = 4

SHOULDER_FORCE = [100.0, 100.0, 100.0]


def smoothstep(u):
    return 3.0 * u * u - 2.0 * u * u * u


def shoulder_z_deg(frame):
    return frame["joints"]["right_shoulder"]["euler_deg"][2]


def elbow_deg(frame):
    return frame["joints"]["right_elbow"]["angle_deg"]


def main():
    cid = p.connect(p.GUI)

    if cid < 0:
        raise RuntimeError("PyBullet GUI connection failed")

    try:
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setTimeStep(1.0 / FPS)

        orientation = p.getQuaternionFromEuler(
            [math.pi / 2, 0, 0]
        )

        robot = p.loadURDF(
            "humanoid/humanoid.urdf",
            basePosition=[0, 0, 4.0],
            baseOrientation=orientation,
            useFixedBase=True
        )

        p.resetDebugVisualizerCamera(
            cameraDistance=6.0,
            cameraYaw=90,
            cameraPitch=-10,
            cameraTargetPosition=[0, 0, 3.7]
        )

        expected_joints = [
            (RIGHT_SHOULDER, "right_shoulder", p.JOINT_SPHERICAL),
            (RIGHT_ELBOW, "right_elbow", p.JOINT_REVOLUTE),
        ]

        for joint_id, expected_name, expected_type in expected_joints:
            info = p.getJointInfo(robot, joint_id)

            if info[1].decode("utf-8") != expected_name:
                raise RuntimeError(
                    f"Joint {joint_id} name mismatch"
                )

            if info[2] != expected_type:
                raise RuntimeError(
                    f"Joint {joint_id} type mismatch"
                )

        frame_01 = get_action_frame(1)
        frame_02 = get_action_frame(2)

        # Set the initial pose directly before animation begins.
        initial_shoulder = shoulder_z_deg(frame_01)
        initial_elbow = elbow_deg(frame_01)

        initial_quaternion = p.getQuaternionFromEuler(
            [0.0, 0.0, math.radians(initial_shoulder)]
        )

        p.resetJointStateMultiDof(
            robot,
            RIGHT_SHOULDER,
            targetValue=initial_quaternion
        )

        p.resetJointState(
            robot,
            RIGHT_ELBOW,
            targetValue=math.radians(initial_elbow)
        )

        def command_pose(shoulder_angle, elbow_angle):
            shoulder_quaternion = p.getQuaternionFromEuler(
                [0.0, 0.0, math.radians(shoulder_angle)]
            )

            p.setJointMotorControlMultiDof(
                robot,
                RIGHT_SHOULDER,
                p.POSITION_CONTROL,
                targetPosition=shoulder_quaternion,
                force=SHOULDER_FORCE
            )

            p.setJointMotorControl2(
                robot,
                RIGHT_ELBOW,
                p.POSITION_CONTROL,
                targetPosition=math.radians(elbow_angle)
            )

        def measure(label, target_shoulder, target_elbow):
            shoulder_quaternion = p.getJointStateMultiDof(
                robot, RIGHT_SHOULDER
            )[0]

            actual_shoulder = math.degrees(
                p.getEulerFromQuaternion(shoulder_quaternion)[2]
            )

            actual_elbow = math.degrees(
                p.getJointState(robot, RIGHT_ELBOW)[0]
            )

            shoulder_error = abs(
                target_shoulder - actual_shoulder
            )

            elbow_error = abs(
                target_elbow - actual_elbow
            )

            print(
                f"{label} | "
                f"Shoulder Target={target_shoulder:.3f} | "
                f"Actual={actual_shoulder:.6f} | "
                f"Error={shoulder_error:.6f} deg",
                flush=True
            )

            print(
                f"{label} | "
                f"Elbow Target={target_elbow:.3f} | "
                f"Actual={actual_elbow:.6f} | "
                f"Error={elbow_error:.6f} deg",
                flush=True
            )

        start_shoulder = shoulder_z_deg(frame_01)
        end_shoulder = shoulder_z_deg(frame_02)

        start_elbow = elbow_deg(frame_01)
        end_elbow = elbow_deg(frame_02)

        duration = frame_02["duration"]
        hold_duration = frame_02["hold"]

        steps = round(duration * FPS)
        hold_steps = round(hold_duration * FPS)

        if steps <= 0 or hold_steps < 0:
            raise ValueError("Invalid frame timing")

        print(
            "=== Robotics Lab Action Frame GUI ===",
            flush=True
        )

        print(
            f"Frame {frame_01['frame_id']:02d}: "
            f"{frame_01['name']}",
            flush=True
        )

        measure(
            "Initial",
            start_shoulder,
            start_elbow
        )

        time.sleep(3)

        print(
            f"=== Frame {frame_01['frame_id']:02d} -> "
            f"Frame {frame_02['frame_id']:02d} ===",
            flush=True
        )

        for i in range(steps):
            u = (i + 1) / steps
            s = smoothstep(u)

            target_shoulder = start_shoulder + (
                end_shoulder - start_shoulder
            ) * s

            target_elbow = start_elbow + (
                end_elbow - start_elbow
            ) * s

            command_pose(target_shoulder, target_elbow)

            p.stepSimulation()
            time.sleep(1.0 / FPS)

        measure(
            "Before Hold",
            end_shoulder,
            end_elbow
        )

        command_pose(end_shoulder, end_elbow)

        for _ in range(hold_steps):
            p.stepSimulation()
            time.sleep(1.0 / FPS)

        measure(
            "After Hold",
            end_shoulder,
            end_elbow
        )

        print(
            "=== Action Frame GUI Completed ===",
            flush=True
        )

        time.sleep(3)

    finally:
        p.disconnect()
        print("GUI closed.", flush=True)


if __name__ == "__main__":
    main()
