# MCU Notes (FRDM-K64F plan)

## Goal

Minimal end-to-end demo on K64F:
- Build a small grid in flash/const.
- Run safety wavefront + SafeStar A* on button press.
- Output ASCII grid and path over UART @ 115200.
- Optional: drive an LED matrix or OLED for a 10×10 map.

## Constraints

- RAM: keep grid modest (e.g., 16×16 → ~256 nodes).
- Deterministic timing: single pass planning under ~10–20 ms at 120 MHz for 16×16.
- No dynamic allocation in steady state (preallocate node array).

## Proposed layout

- `mcu/`
  - `src/main.c` (startup + board init)
  - `src/safestar_shim.cpp` (C wrappers if using C startup)
  - `include/board_uart.h` (printf-lite)
  - `CMakeLists.txt` or vendor project files

## Demo flow

1. Initialize UART and GPIO.
2. Precompute neighbors for a fixed grid.
3. On button press:
   - compute `d_exit`
   - run `hazard_wavefront`
   - run `safeStar_path`
   - print grid with `S/A/@/H/E/X/#` over UART
4. Repeat with a different hazard set.

## Timing/Memory checklist

- Node struct trimmed for MCU:
  - Use `uint16_t` for ids/coords where possible.
  - Consider `int16_t` for distances on small grids.
- Avoid recursion and STL in the MCU build (or replace with fixed-size heaps/queues).

## Next steps

- Create `mcu/` skeleton with a UART “hello grid”.
- Port `grid_construct`, `node_get_neighbors`, `hazard_wavefront`, `safeStar_path`.
- Replace `std::vector` with fixed arrays for the first MCU pass.
