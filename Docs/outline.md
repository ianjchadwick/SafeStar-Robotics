# SafeStar Project Outline

---

### Objective

* Implement a hazard-aware pathfinding algorithm (SafeStar) that combines standard A* and safety-weighted cost functions.
* Deploy on an MCU platform with real-time visual output.
* Integrate simulated hazard source data to enable dynamic pathfinding adjustments using a grid-based safety score.

---

### Hardware Selection

* **Primary MCU:** FRDM K64F – 120 MHz ARM Cortex-M4, suitable for pathfinding and visualization.
* **Backup Options:**
  * Renesas RA0E1 – Cortex-M0, low-cost, low-power.
  * FRDM MCXC444 – Cortex-M4, additional GPIOs.
  * FRDM MCXA-153 – Cortex-M7, high-performance for advanced visualization.

---

### Development Phases

1. **Algorithm Implementation:** A* and SafeStar (hazard-aware, multi-objective) pathfinding, memory-optimized.
2. **MCU Integration:** Grid representation, node struct with safety score and exit distance, UART output for debugging and validation.
3. **Visualization:** OLED/LED matrix for real-time path and hazard output.
4. **Hazard Simulation:** Generate mock hazard data and safety scores to test dynamic response.
5. **Optimization:** Tune for memory usage, runtime efficiency, and potential sensor integration.

---

### Testing and Validation

* Pathfinding correctness on simulated grids.
* Dynamic hazard updates to verify SafeStar algorithm performance and safety scoring.
* UART logging for tracking path selection and algorithm decisions.

---

**SafeStar’s goal:**  
To compute a real-time path to the *closest safe exit*, balancing shortest path distance with maximum safety score (i.e., avoiding hazard proximity).
