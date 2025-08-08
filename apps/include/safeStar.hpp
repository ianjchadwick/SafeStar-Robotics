#pragma once

#include <vector>
#include <tuple>
#include <utility>
#include <limits>

struct Node {
    int id;
    int x, y;
    int d_exit = std::numeric_limits<int>::max();
    int safety_score = std::numeric_limits<int>::max();
    std::vector<int> neighbors;
    double cost = std::numeric_limits<double>::infinity();
    int backpointer = -1;
};

using Grid = std::vector<std::vector<int>>;

// Grid and node initialization
void grid_construct(Grid& grid, std::vector<Node>& nodes, int size,
                    const std::vector<std::tuple<int, int, int, int>>& obstacles);

void node_get_neighbors(const Grid& grid, std::vector<Node>& nodes);

void node_set_d_exit(std::vector<Node>& nodes, const std::vector<std::pair<int,int>>& exits);

void hazard_wavefront(std::vector<Node>& nodes, const std::vector<std::pair<int,int>>& hazard_sources);

// SafeStar pathfinding (hazard-aware)
std::vector<int> safeStar_path(std::vector<Node>& nodes, const Grid& grid,
                               std::pair<int,int> start, const std::vector<std::pair<int,int>>& exits);

// Classic A* baseline
std::vector<int> classic_a_star(std::vector<Node>& nodes, const Grid& grid,
                                std::pair<int,int> start, const std::vector<std::pair<int,int>>& exits);

// Grid print for console visualization
void print_grid(const Grid& grid, const std::vector<Node>& nodes,
                const std::vector<int>& safeStar_path, const std::vector<int>& classic_path,
                std::pair<int,int> start, const std::vector<std::pair<int,int>>& exits,
                const std::vector<std::pair<int,int>>& hazard_sources);
