# SafeStar – Usage (C++)

## Minimal example

```cpp
#include "safestar.hpp"

int main() {
    int size = 9;
    Grid grid;
    std::vector<Node> nodes;

    std::vector<std::tuple<int,int,int,int>> obstacles = {
        {1,1,1,3}, {1,1,4,1} /* … */
    };
    std::vector<std::pair<int,int>> exits   = {{3,8}, {8,0}};
    std::vector<std::pair<int,int>> hazards = {{0,6}};
    std::pair<int,int> start = {1,4};

    grid_construct(grid, nodes, size, obstacles);
    node_get_neighbors(grid, nodes);
    node_set_d_exit(nodes, exits);
    hazard_wavefront(nodes, hazards);  // fills Node::safety_score (0 at hazard; higher = safer)

    auto safe = safeStar_path(nodes, grid, start, exits);

    // Reset state if running another search
    for (auto& n : nodes) { n.cost = std::numeric_limits<double>::infinity(); n.backpointer = -1; }
    auto classic = classic_a_star(nodes, grid, start, exits);

    print_grid(grid, nodes, safe, classic, start, exits, hazards);
}
```

## Build & run

```bash
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build -j
./build/safeStar_demo
```

## Python visualization (prototype)

```bash
cd python_prototype
python draw_visualization.py
```

Press **Q** or close the window to exit.

## Legend

`S` SafeStar, `A` A*, `@` overlap, `H` hazard, `E` exit, `X` start, `#` obstacle.
