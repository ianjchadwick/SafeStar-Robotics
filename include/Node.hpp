#pragma once

#include <vector>
#include <array> 
#include <limits>

struct Node
{
    int node_id;
    int backpointer = -1;
    int d_exit = std::numeric_limits<int>::max();
    int safety = std::numeric_limits<int>::max();
    double cost;
    std::array<int, 2> coords;
    std::vector<int> neighbors;
};
