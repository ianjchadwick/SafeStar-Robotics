# SafeStar-Robotics

**Hazard-aware pathfinding system** designed for emergency egress and motion planning.  
Implements a modular C++ engine using A* with safety-weighted heuristics and real-time hazard inputs.

## Status: Work in Progress

This project is under active development. Current focus areas:
- Adapting the core C++ engine for deployment on a Kinetis K64 microcontroller
- Refining safety heuristics and hazard update models
- Adding test cases and MCU integration demos

Expect incomplete features, evolving architecture, and stubbed modules.  
A high-level architecture overview will be added to `docs/architecture.md`.

---

## Features (planned and in progress)

- A* pathfinding with dynamic safety cost mapping
- Modular hazard input and reactive updates
- Real-time path recalculation for constrained embedded environments
- Microcontroller deployment (target: Kinetis K64)

---

## Goals

- Demonstrate embedded robotics motion planning without ROS
- Serve as a portfolio project for real-time, safety-aware control logic
- Highlight firmware-to-algorithm integration on low-power hardware
