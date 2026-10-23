"""Robotics Lab Step 8 / Phase 1-A: URDF static inspection only.
New branch only. No motors, simulation stepping, or existing project edits.
"""
from pathlib import Path
import csv
import sys

try:
    import pybullet as p
    import pybullet_data
except ImportError as exc:
    raise SystemExit(f"FAIL: PyBullet unavailable: {exc}")

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "evidence"
TARGETS = ("left_shoulder", "left_elbow", "right_shoulder", "right_elbow")
TYPE_NAMES = {
    p.JOINT_REVOLUTE: "REVOLUTE",
    p.JOINT_PRISMATIC: "PRISMATIC",
    p.JOINT_SPHERICAL: "SPHERICAL",
    p.JOINT_PLANAR: "PLANAR",
    p.JOINT_FIXED: "FIXED",
}


def decode(raw):
    return raw.decode("utf-8", errors="replace") if isinstance(raw, bytes) else str(raw)


def main():
    client = p.connect(p.DIRECT)
    if client < 0:
        raise RuntimeError("DIRECT connection failed")
    try:
        p.setAdditionalSearchPath(pybullet_data.getDataPath(), physicsClientId=client)
        robot = p.loadURDF("humanoid/humanoid.urdf", useFixedBase=True,
                           physicsClientId=client)
        count = p.getNumJoints(robot, physicsClientId=client)
        rows = []
        print(f"MODEL=humanoid/humanoid.urdf FIXED_BASE=True JOINT_COUNT={count}")
        print("Note: JOINT_SPHERICAL axes/limits are not fully characterized by getJointInfo.")
        for jid in range(count):
            info = p.getJointInfo(robot, jid, physicsClientId=client)
            row = {
                "joint_id": jid,
                "joint_name": decode(info[1]),
                "joint_type": TYPE_NAMES.get(info[2], str(info[2])),
                "q_index": info[3],
                "u_index": info[4],
                "lower_limit_raw": info[8],
                "upper_limit_raw": info[9],
                "max_force_raw": info[10],
                "max_velocity_raw": info[11],
                "joint_axis_local_raw": tuple(info[13]),
                "parent_frame_pos": tuple(info[14]),
                "parent_frame_orn_xyzw": tuple(info[15]),
                "parent_link_index": info[16],
                "child_link_name": decode(info[12]),
            }
            rows.append(row)
            print(f"ID={jid:02d} name={row['joint_name']} type={row['joint_type']} "
                  f"axis={row['joint_axis_local_raw']} limits_raw="
                  f"({row['lower_limit_raw']}, {row['upper_limit_raw']}) "
                  f"parent={row['parent_link_index']}")
        matches = {}
        for target in TARGETS:
            found = [r for r in rows if r["joint_name"] == target]
            matches[target] = found
            print(f"TARGET {target}: " + (
                f"ID={found[0]['joint_id']}, type={found[0]['joint_type']}"
                if len(found) == 1 else f"MATCH_COUNT={len(found)} (not uniquely mapped)"))
        OUT.mkdir(parents=True, exist_ok=True)
        path = OUT / "phase1a_joint_inventory.csv"
        with path.open("x", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0]) if rows else ["joint_id"])
            writer.writeheader()
            writer.writerows(rows)
        print(f"CSV_CREATED={path}")
        expected = {"left_shoulder": "SPHERICAL", "right_shoulder": "SPHERICAL",
                    "left_elbow": "REVOLUTE", "right_elbow": "REVOLUTE"}
        passed = all(len(matches[k]) == 1 and matches[k][0]["joint_type"] == t
                     for k, t in expected.items())
        print("STATIC_MAPPING=" + ("PASS" if passed else "FAIL / REVIEW REQUIRED"))
        print("MOTION_COMMANDS=NONE SIMULATION_STEPS=0")
        return 0 if passed else 2
    finally:
        p.disconnect(physicsClientId=client)


if __name__ == "__main__":
    sys.exit(main())
