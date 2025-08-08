# SafeStar Python Prototype

This prototype implements a hazard-aware pathfinding algorithm using a modified A* search strategy. It introduces safety heuristics and dynamic cost adjustments to compute optimal paths in risk-weighted environments.

Originally developed as part of an academic research project, the Python version serves as a logic prototype for future embedded deployment.

---

## Features

- Weighted 2D grid map with obstacles and exits
- Wavefront-based safety score propagation (higher score = farther from hazard, safer)
- Modified A* that balances proximity to exits and maximizes safety score
- Visualization with `pygame` to render paths, hazards, and environments

---

## Requirements

- `numpy`
- `pygame`

To install:

```bash
pip install numpy pygame
```

Or if using a virtual environment:

```bash
pip install -r requirements.txt
```

---

## Running the Demo

From the `python_prototype/` directory:

```bash
python draw_visualization.py
```

> Press **Q** or close the window to exit the visualization.

---

## Inputs and Parameters

- `size`: Integer grid size (square)
- `obstacles`: List of `[x, y], height, width` obstacle definitions
- `exits`: List of `[x, y]` coordinates for valid goal locations
- `hazard_sources`: List of `[x, y]` coordinates to simulate risk zones
- `start`: `[x, y]` coordinate for the starting point

You can toggle between test scenarios by commenting/uncommenting the “FIGURE” blocks in `draw_visualization.py`.

---

## Grid Visualization Output

- **Black** → Obstacles
- **Red** → Hazard sources
- **Blue** → Start location
- **Green** → Exits
- **Purple** → Safe* path (hazard-aware: seeks the closest exit while maximizing safety score—i.e., distance from hazard)
- **Orange** → Standard A* path (shortest path to any exit, ignores hazards; if overlapping, A* overwrites purple)

The Safe* algorithm demonstrates routing that prioritizes both minimal path length and maximal safety from hazard zones. Standard A* is included as a baseline for comparison.

---

## Algorithm Summary

- A wavefront search calculates a **safety score** for each grid cell.
    - Safety score is `0` on a hazard, increases with distance from hazard.
    - Pathfinding prefers cells with higher safety scores.
- Each node stores both `d_exit` (distance to nearest exit) and `safety_score`.
- Modified A* prioritizes reducing exit distance and maximizing safety score.
- Multiple scenarios demonstrate the effects of competing risk fields on routing.

---

## Notes

- This prototype is archived and frozen for reference.
- A portable C++ implementation for embedded deployment is available in the main repo under `apps/`.
