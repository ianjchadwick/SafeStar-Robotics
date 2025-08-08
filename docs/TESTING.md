# Testing

## Prereqs

- CTest + Catch2 (fetched in CMake)

## Run

```bash
cmake -S . -B build
cmake --build build -j
ctest --test-dir build --output-on-failure
```

## What’s covered

- **Wavefront monotonicity:** safety score increases with distance from hazards.
- **Planner behavior:** SafeStar’s worst-case safety along its path beats classic A* when an equal-length detour exists.
