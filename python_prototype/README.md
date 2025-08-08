# SafeStar Python Prototype

This prototype implements a hazard-aware pathfinding algorithm using a modified A* search strategy. It introduces safety heuristics and dynamic cost adjustments to compute optimal paths in risk-weighted environments.

Originally developed as part of an academic research project, the Python version serves as a logic prototype for future embedded deployment.

---

## Features

- Weighted 2D grid map with obstacles and exits
- Wavefront-based hazard propagation
- Modified A* that balances proximity to exits and distance from hazards
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
- **Purple** → Safe* path (hazard-aware: seeks the exit that is closest while avoiding hazard proximity)
- **Orange** → Standard A* path (shortest path to any exit, ignores hazards; if overlapping, A* overwrites purple)

The Safe* algorithm demonstrates routing that prioritizes both minimal path length and maximal safety from hazard zones. Standard A* is included as a baseline for comparison.

---

## Algorithm Summary

- A wavefront search calculates a "hazard distance" from danger zones.
- Each node stores both `d_exit` (distance to nearest exit) and `hazard_distance`.
- A* is modified to prefer paths that both reduce exit distance and increase hazard distance.
- Multiple scenarios demonstrate the effects of competing risk fields on routing.

---

## Notes

- This prototype is archived and frozen for reference.
- A portable C++ implementation for embedded deployment is available in the main repo under `apps/`.
