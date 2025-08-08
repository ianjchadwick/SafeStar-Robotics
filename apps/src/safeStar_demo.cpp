#include "safeStar.hpp"
#include <vector>
#include <tuple>
#include <utility>
#include <iostream>

void print_safety_score(const Grid& grid, const std::vector<Node>& nodes) {
    int size = grid.size();
    std::vector<std::vector<int>> hd_map(size, std::vector<int>(size, -1));
    for (const auto& node : nodes) {
        hd_map[node.x][node.y] = node.safety_score;
    }
    std::cout << "Hazard distance map:\n";
    for (int x=0; x<size; ++x) {
        for (int y=0; y<size; ++y) {
            if (grid[x][y] == 0)
                std::cout << "## ";
            else
                std::cout << hd_map[x][y] << "  ";
        }
        std::cout << "\n";
    }
}


int main() {
    int size = 9;
    std::vector<std::tuple<int,int,int,int>> obstacles = {
        {1, 1, 1, 3}, {1, 1, 4, 1}, {3, 3, 2, 1}, {1, 5, 4, 1},
        {1, 7, 1, 2}, {4, 7, 1, 2}, {6, 0, 1, 5}, {6, 4, 2, 1},
        {6, 6, 1, 3}, {8, 6, 1, 1}
    };
    std::vector<std::pair<int,int>> exits = {{3, 8}, {8, 0}};
    std::vector<std::pair<int,int>> hazard_sources = {{0, 6}};
    std::pair<int,int> start = {1, 4};

    Grid grid;
    std::vector<Node> nodes;
    grid_construct(grid, nodes, size, obstacles);
    node_get_neighbors(grid, nodes);
    node_set_d_exit(nodes, exits);
    hazard_wavefront(nodes, hazard_sources);

    print_safety_score(grid, nodes);

    // Paths
    auto safeStar = safeStar_path(nodes, grid, start, exits);

    for (auto& node : nodes) {
    node.cost = std::numeric_limits<double>::infinity();
    node.backpointer = -1;
    }

    auto classic = classic_a_star(nodes, grid, start, exits);

    // Print ASCII grid
    print_grid(grid, nodes, safeStar, classic, start, exits, hazard_sources);

    // Print path lengths
    std::cout << "SafeStar path length: " << safeStar.size() << "\n";
    std::cout << "Classic A* path length: " << classic.size() << "\n";

    return 0;
}
