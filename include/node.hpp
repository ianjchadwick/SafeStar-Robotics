#pragma once

#include <vector>
#include <array> 
#include <limits>
#include <cstdint>

struct Node
{
    std::int16_t node_id;
    std::int16_t backpointer = -1;
    std::int16_t d_exit = std::numeric_limits<std::int16_t>::max();
    std::int16_t safety = std::numeric_limits<std::int16_t>::max();
    float cost = 0.0;
    // X, Y coordinates of Node
    std::array<int, 2> coords {};
    // Node Id of 4 N/E/S/W neigbors.    
    std::array<int16_t, 4> neighbors; 
};
