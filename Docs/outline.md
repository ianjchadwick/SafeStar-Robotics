# SafeStar Project Outline

---

### Objective:

* Implement a hazard-aware pathfinding algorithm for emergency evacuation using A\* and Safe\*.
* Deploy on MCU with real-time visual output.
* Integrate simulated hazard data for pathfinding adjustments.

---

### Hardware Selection:

* **Primary MCU:** FRDM K64F - 120 MHz ARM Cortex-M4, sufficient for pathfinding and visualization.
* **Backup Options:**

  * Renesas RA0E1 - Cortex-M0, low-cost and low-power.
  * FRDM MCXC444 - Cortex-M4, additional GPIOs.
  * FRDM MCXA-153 - Cortex-M7, high-performance for advanced visualization.

---

### Development Phases:

1. **Algorithm Implementation:** A\* and Safe\* algorithm in C, memory-optimized.
2. **MCU Integration:** Grid representation, node struct, UART output for debugging.
3. **Visualization:** OLED/LED matrix for visual path output.
4. **Hazard Simulation:** Mock hazard data for dynamic pathfinding.
5. **Optimization:** Memory usage, runtime efficiency, sensor integration.

---

### Testing and Validation:

* Pathfinding tests on simulated grids.
* Dynamic hazard updates to verify Safe\* algorithm.
* UART logging to track pathfinding decisions.
