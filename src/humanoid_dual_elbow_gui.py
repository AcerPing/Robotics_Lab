
import math
import time
import pybullet as p
import pybullet_data

FPS = 240
STEPS = 480
HOLD_STEPS = 120

RIGHT_ID = 4
LEFT_ID = 7

JOINTS = [
    (RIGHT_ID, "right_elbow"),
    (LEFT_ID, "left_elbow"),
]


def smoothstep(u):
    return 3 * u * u - 2 * u * u * u


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
            useFixedBase=True,
        )

        p.resetDebugVisualizerCamera(
            cameraDistance=7.0,
            cameraYaw=45,
            cameraPitch=-15,
            cameraTargetPosition=[0, 0, 3.0],
        )

        for joint_id, expected_name in JOINTS:
            info = p.getJointInfo(robot, joint_id)
            actual_name = info[1].decode("utf-8")

            if actual_name != expected_name:
                raise RuntimeError(
                    f"Joint {joint_id}: expected {expected_name}, "
                    f"got {actual_name}"
                )

            if info[2] != p.JOINT_REVOLUTE:
                raise RuntimeError(
                    f"Joint {joint_id} is not REVOLUTE"
                )

            p.resetJointState(robot, joint_id, 0.0)

        def command_both(target_deg):
            for joint_id, _ in JOINTS:
                p.setJointMotorControl2(
                    robot,
                    joint_id,
                    p.POSITION_CONTROL,
                    targetPosition=math.radians(target_deg),
                )

        def measure(label, target_deg):
            right = math.degrees(
                p.getJointState(robot, RIGHT_ID)[0]
            )
            left = math.degrees(
                p.getJointState(robot, LEFT_ID)[0]
            )

            difference = abs(right - left)
            right_error = abs(target_deg - right)
            left_error = abs(target_deg - left)

            print(
                f"{label} | Target: {target_deg:.3f} deg | "
                f"Right: {right:.6f} deg | "
                f"Left: {left:.6f} deg | "
                f"Difference: {difference:.6f} deg | "
                f"Errors: R={right_error:.6f}, "
                f"L={left_error:.6f} deg",
                flush=True,
            )

        def move_frame(start_deg, end_deg, label):
            print(f"\n=== {label} ===", flush=True)

            max_difference = 0.0

            for i in range(STEPS):
                u = (i + 1) / STEPS
                target = start_deg + (
                    end_deg - start_deg
                ) * smoothstep(u)

                command_both(target)
                p.stepSimulation()

                right = math.degrees(
                    p.getJointState(robot, RIGHT_ID)[0]
                )
                left = math.degrees(
                    p.getJointState(robot, LEFT_ID)[0]
                )
                max_difference = max(
                    max_difference,
                    abs(right - left),
                )

                time.sleep(1.0 / FPS)

            measure("Before Hold", end_deg)

            command_both(end_deg)

            for _ in range(HOLD_STEPS):
                p.stepSimulation()
                time.sleep(1.0 / FPS)

            measure("After Hold", end_deg)
            print(
                f"Maximum Motion Difference: "
                f"{max_difference:.6f} deg",
                flush=True,
            )

        print(
            "=== Dual Elbow GUI Smoothstep Simulation ===",
            flush=True,
        )

        measure("Initial", 0.0)

        time.sleep(3)

        move_frame(0.0, 45.0, "Frame 1 -> Frame 2")
        move_frame(45.0, 0.0, "Frame 2 -> Frame 3")

        print(
            "\n=== Dual Elbow GUI Demonstration Completed ===",
            flush=True,
        )

        time.sleep(3)

    finally:
        p.disconnect()
        print("GUI closed.", flush=True)


if __name__ == "__main__":
    main()
