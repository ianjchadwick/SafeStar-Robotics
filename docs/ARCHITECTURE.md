# Architecture

## Components

- **Grid & Nodes**
  - `Grid` is a 2D int map (0 = obstacle, >0 = node id).
  - `Node` stores `(id, x, y, d_exit, safety_score, neighbors, cost, backpointer)`.

- **Safety wavefront**
  - BFS from each hazard sets `safety_score`: `0` at hazards, increasing by 1 per step.
  - Higher score = safer (farther from any hazard).
  - Unreached cells stay at `max()` (treated as “unknown” / effectively very safe depending on usage).

- **Distance-to-exit**
  - `d_exit` per node = Manhattan distance to the nearest exit.

- **Planners**
  - **SafeStar (multi-objective A*):** favors moves that increase safety and reduce `d_exit`.
  - **Classic A*:** distance-only baseline.

## Cost / Priority

- **Move cost (C++ mirrors original Python):**

  Preference order:
  1. `Δsafety > 0` **and** `Δexit < 0` → cost = `0.0`
  2. `Δsafety ≥ 0` **and** `Δexit ≤ 0` → cost = `1.0`
  3. `Δsafety < 0` **and** `Δexit ≥ 0` → cost = `1.5`
  4. `Δsafety < 0` **and** `Δexit < 0` → cost = `2.0`

- **A* priority (SafeStar):**
  ```
  priority = new_cost + (d_exit - safety_score)
  ```

## Data flow

1. Construct grid → assign node ids.
2. Build neighbors (N/E/S/W).
3. Compute `d_exit` per node.
4. Run safety wavefront to fill `safety_score`.
5. Run planner(s) → path ids → render/print.

## Complexity (typical)

- Wavefront BFS: `O(V + E)` on grid (≈ `O(n^2)`).
- A* (4-neighborhood): `O(E log V)`; fast on demo sizes.
