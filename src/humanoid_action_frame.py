
import math
import time
import pybullet as p
import pybullet_data

FPS = 240
STEPS = 480
HOLD_STEPS = 120
JOINT_ID = 4


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
            useFixedBase=True
        )

        name = p.getJointInfo(robot, JOINT_ID)[1].decode()
        if name != "right_elbow":
            raise RuntimeError(f"Unexpected joint: {name}")

        p.resetDebugVisualizerCamera(
            cameraDistance=7.0,
            cameraYaw=45,
            cameraPitch=-15,
            cameraTargetPosition=[0, 0, 3.0]
        )

        def actual_angle():
            return math.degrees(
                p.getJointState(robot, JOINT_ID)[0]
            )

        def command(angle_deg):
            p.setJointMotorControl2(
                robot,
                JOINT_ID,
                p.POSITION_CONTROL,
                targetPosition=math.radians(angle_deg)
            )

        def move_frame(start_deg, end_deg, label):
            print(f"\n=== {label} ===", flush=True)

            for i in range(STEPS):
                u = (i + 1) / STEPS
                target = start_deg + (
                    end_deg - start_deg
                ) * smoothstep(u)

                command(target)
                p.stepSimulation()
                time.sleep(1.0 / FPS)

            before = actual_angle()
            print(f"Before hold: {before:.6f} deg", flush=True)

            command(end_deg)

            for _ in range(HOLD_STEPS):
                p.stepSimulation()
                time.sleep(1.0 / FPS)

            after = actual_angle()
            error = abs(end_deg - after)

            print(
                f"After hold: {after:.6f} deg | "
                f"Error: {error:.6f} deg",
                flush=True
            )

        print("=== Humanoid Action Frame Simulation ===", flush=True)
        print(f"Joint: {name} (ID {JOINT_ID})", flush=True)
        print("Interpolation: Smoothstep", flush=True)
        print("Motion: 0 -> 45 -> 0 deg", flush=True)
        print("Force: API default", flush=True)

        print("Initial pose: 0 degrees", flush=True)
        time.sleep(3)

        move_frame(0, 45, "Frame 1 -> Frame 2")
        move_frame(45, 0, "Frame 2 -> Frame 3")

        print("Demonstration completed.", flush=True)
        time.sleep(3)

    finally:
        p.disconnect()
        print("GUI closed.", flush=True)


if __name__ == "__main__":
    main()
