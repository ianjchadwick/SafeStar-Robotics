# SafeStar Robotics

[![CI](https://github.com/ianjchadwick/SafeStar-Robotics/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/ianjchadwick/SafeStar-Robotics/actions/workflows/ci.yml)

# SafeStar Robotics

SafeStar is a hazard-aware pathfinding system for embedded deployment. It extends A* with a wavefront-based **safety score** (0 at hazards; higher = safer) to find the **closest safe exit** rather than the merely shortest path.

- C++ desktop demo (safety-aware A*)
- Python prototype (logic + visualization)
- MCU port in progress (FRDM-K64F)

---

## Quickstart (C++)

```bash
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build -j
./build/safeStar_demo
```

> Add a screenshot or GIF at `docs/images/safestar_demo.png` and reference it below:

![SafeStar demo](docs/images/safestar_demo.png)

---

## How it works (one minute)

- **Wavefront safety score:** BFS from hazards sets `safety_score` per cell (0 at hazard; increases with distance).
- **SafeStar planner:** multi-objective A* that favors higher safety *and* reduced distance-to-exit.
- **Baseline:** classic A* ignores hazards for comparison.

Legend: `S` SafeStar, `A` A*, `@` overlap, `H` hazard, `E` exit, `X` start, `#` obstacle.

---

## Project Layout

```
├── apps/                       # Runnable desktop demos (C++)
│   ├── include/            
|   |   └──safeStar.hpp
|   ├── src/
|   |   ├──safeStar_demo.cpp    # Safety-aware pathfinding demo
|   |   └──safeStar.cpp
├── python_prototype/           # Archived Python prototype + visualization
│   ├── hazard_pathfinder.py
│   ├── draw_visualization.py
│   └── README.md
├── include/                    # MCU Port Includes (WIP)
├── src/                        # MCU Port Source (WIP)
├── test/                       # Unit tests (ctest/Catch2)
├── CMakeLists.txt
└── README.md
```

---

## Docs

- Usage: [`docs/USAGE.md`](docs/USAGE.md)
- Architecture: [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)
- Testing: [`docs/TESTING.md`](docs/TESTING.md)
- MCU notes: [`docs/MCU_NOTES.md`](docs/MCU_NOTES.md)

---

## Status

- Desktop C++ demo: complete
- Python prototype: archived
- MCU port (FRDM-K64F): in progress

## License

MIT
