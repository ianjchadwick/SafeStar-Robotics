#pragma once

#include "node.hpp"
#include "bitgrid.hpp"
#include <vector>
#include <array>
#include <cstdint>

constexpr uint8_t MAX_WIDTH{50};
constexpr uint8_t MAX_HEIGHT{50};
constexpr int MAX_GRID{MAX_WIDTH*MAX_HEIGHT};


class Graph
{
using obstacle_bitmap = BitGrid<MAX_WIDTH,MAX_HEIGHT>;
using exit_vect_t = std::vector<std::array<std::int16_t, 2>>;
using node_vect_t = std::vector<Node>;
private:
    int size{0};
    exit_vect_t exits;
    node_vect_t nodes;
    obstacle_bitmap obstacles;
public:
    Graph(int size, 
          const obstacle_bitmap& obstacle_list, 
          const exit_vect_t& exit_list);
    void initialize_state();
    void update_neighbors();
    void find_d_exit();
    void hazard_wavefront();
    void next_move_cost();
};
