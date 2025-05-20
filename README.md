# SafeStar - Pathfinding for Emergency Egress in Robotics

SafeStar is a real-time pathfinding system that calculates optimal escape routes using a modified A\* algorithm. Originally developed in Python, this version is implemented in C for embedded MCUs like FRDM K64F, focusing on hazard avoidance and emergency evacuation.

---

### Hardware and Tools:

* FRDM K64F, Renesas RA0E1, FRDM MCXC444, FRDM MCXA-153
* OLED/LED matrix for visual output
* C/C++, UART, FreeRTOS (optional)

---

### Project Structure:

* `algorithm/` - A\* and Safe\* implementations
* `mcu/` - MCU drivers and integration
* `visualization/` - Display and output handling
* `testing/` - Test cases and validation scripts
* `docs/` - Documentation and technical details

---

### Installation:

1. Clone the repository:

   ```bash
   git clone https://github.com/ianjchadwick/SafeStar-Robotics.git
   ```
2. Open the project in an IDE (MCUXpresso, IAR).
3. Compile and flash to the target MCU.
4. Connect UART for debugging.

---

### Usage:

* Configure parameters in `config.h`.
* Monitor pathfinding output via UART.
* Adjust hazard data to simulate real-world conditions.

---

### Future Work:

* Sensor integration for dynamic hazard updates.
* Enhanced heuristics for multi-agent pathfinding.
* Memory optimization for constrained MCUs.
