# Robotics Lab — Humanoid Robot Motion Control with PyBullet

機器人概論與實作｜Python 人形機器人模擬與動作控制

## Overview

This project explores introductory humanoid robot motion control
using Python and PyBullet.

The main topics include:

- Joint identification and joint-angle control
- Action frames and motion sequences
- GUI-based humanoid simulation
- Motion smoothing and observation
- Experimental recording and evidence review

## Project Structure

- `src/` — Humanoid joint and motion-control experiments
- `docs/` — Research notes, experiment records, and final report
- `experiments/little_apple_dance/` — Initial dance-study materials

## Environment

- Python 3
- PyBullet
- PyBullet bundled simulation data where applicable

Example environment setup on Windows:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install pybullet
```

The commands above are setup examples, not a verified
reproduction environment or a dependency lockfile.

## Source Files

The `src/` folder contains experiments related to
humanoid joints, action frames, and GUI simulation.

See individual Python files and the final report for
experiment-specific details.

## Simulation Scope and Limitations

This repository primarily documents fixed-base humanoid
robot simulation.

Simulation results do not demonstrate physical Alpha 1S
hardware compatibility or real-world robot safety.

Visual observations from recorded simulations do not
independently establish complete historical source-code
provenance or reproducibility.

Refer to the final report for the limitations of each
experiment and its supporting evidence.

## Evidence and Recordings

Experiment records and video indexes are provided in `docs/`.

Paths referring to `RecordFile錄影/` describe local evidence
locations. The original large video files are not included
in this public repository.

Some documentation paths have been normalized for public
presentation. The original experimental records are
preserved separately.

## Little Apple Experiment

The `experiments/little_apple_dance/` directory contains
initial exploration materials.

Later calibration scripts and evolving CSV evidence are
not included in this public release.

## Notes

This is a personal educational and simulation project.
Third-party course materials are not bundled in this
clean public release.

The repository does not claim to provide a complete
hardware deployment solution.
## PyBullet Model and Execution Notes

The main humanoid simulation scripts load the model
`humanoid/humanoid.urdf` using the search directory
provided by `pybullet_data.getDataPath()`.

The URDF model is provided by the installed PyBullet
simulation data package and is not copied into this
repository.

Scripts using PyBullet GUI require an appropriate
graphical desktop environment.

Some scripts in `src/` import
`humanoid_action_frames.py` from the same directory.
Keep these Python files together when running them.

The repository contains source code and experiment
documentation, but a fresh-environment end-to-end
reproduction test has not yet been completed.

No physical Alpha 1S robot compatibility is claimed.
