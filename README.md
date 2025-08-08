# SafeStar Robotics

SafeStar is a hazard-aware pathfinding system designed for embedded deployment.  
It implements a modular C++ engine that extends A* pathfinding with safety-weighted heuristics, dynamic cost mapping, and configurable hazard sources.

---

## Overview

This project explores how embedded systems can make real-time navigation decisions in the presence of environmental risks.  
The SafeStar algorithm combines standard A* pathfinding with a **safety score** model that steers paths away from hazards as well as toward the nearest exit.

System components include:
- A desktop C++ demo for safety-augmented pathfinding on weighted grids
- A Python prototype for logic exploration and algorithm development
- Ongoing work targeting deployment on a Kinetis K64 microcontroller

The architecture is portable, modular, and ROS-independent.

---

## How Safety Works

- SafeStar uses a **wavefront propagation algorithm** to assign a *safety score* to each grid cell.
    - Cells directly on a hazard have a safety score of `0` (maximally unsafe).
    - Safety score increases with distance from the nearest hazard.
    - Pathfinding strongly prefers routes through cells with higher safety scores, balancing safety and exit proximity.
- The classic A* baseline considers only shortest path to exit, ignoring hazard locations.

**Grid legend:**
- `S`: SafeStar path (safety-aware, multi-objective)
- `A`: Classic A* path (distance only)
- `@`: Both paths overlap
- `H`: Hazard
- `E`: Exit
- `X`: Start
- `#`: Obstacle

---

## Project Layout

```
├── apps/                   # Runnable desktop demos (C++)
│   ├── astar_demo.cpp      # Basic A* on hazard-weighted grid
│   └── hazard_demo.cpp     # Custom cost function using safety and goal heuristics
├── python_prototype/       # Archived Python logic prototype and visualization
│   ├── hazard_pathfinder.py
│   ├── draw_visualization.py
│   └── README.md
├── include/                # Shared headers (optional)
├── src/                    # Embedded-targeted logic modules (optional)
├── CMakeLists.txt
└── README.md               # Top-level overview
```

---

## Building the C++ Demo

```bash
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build -j
./build/hazard_demo
```

---

## Python Visualization

The archived Python prototype includes full grid rendering with multiple test cases.

```bash
cd python_prototype
python draw_visualization.py
```

---

## Features

- Custom A* implementation with safety-weighted multi-objective heuristics
- Wavefront propagation to assign safety scores
- Configurable obstacle, hazard, and exit locations
- Tunable cost model combining exit proximity and safety score
- Designed for embedded systems with deterministic behavior

---

## Development Goals

- Implement hazard-aware path planning for microcontroller environments
- Demonstrate real-time, safety-oriented control logic without ROS
- Provide a portfolio-grade example of algorithm-to-firmware integration

---

## Status

- Desktop C++ demo complete
- Python prototype archived for reference
- Embedded port in progress (target: Kinetis K64)
- Documentation and benchmarks to follow
