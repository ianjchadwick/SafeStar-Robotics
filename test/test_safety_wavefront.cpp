#include <catch2/catch_test_macros.hpp>
#include "safeStar.hpp"
#include <algorithm>
#include <limits>

static int safety_at(const std::vector<Node>& nodes, int x, int y) {
    for (const auto& n : nodes) if (n.x == x && n.y == y) return n.safety_score;
    return -1;
}

TEST_CASE("Wavefront safety increases with distance from hazard") {
    int size = 5;
    Grid grid; std::vector<Node> nodes;
    std::vector<std::tuple<int,int,int,int>> obstacles;
    std::vector<std::pair<int,int>> exits = {{0,4}};
    std::vector<std::pair<int,int>> hazards = {{0,0}};

    grid_construct(grid, nodes, size, obstacles);
    node_get_neighbors(grid, nodes);
    node_set_d_exit(nodes, exits);
    hazard_wavefront(nodes, hazards);

    REQUIRE(safety_at(nodes, 0, 0) == 0);
    REQUIRE(safety_at(nodes, 0, 1) == 1);
    REQUIRE(safety_at(nodes, 1, 0) == 1);
    REQUIRE(safety_at(nodes, 1, 1) == 2);
    REQUIRE(safety_at(nodes, 2, 2) >= safety_at(nodes, 1, 1));
}

TEST_CASE("SafeStar avoids hazard-adjacent cells when equal-length detour exists") {
    int size = 5;
    Grid grid; std::vector<Node> nodes;
    std::vector<std::tuple<int,int,int,int>> obstacles = { {2,1,1,3} };
    std::vector<std::pair<int,int>> exits = {{0,4}};
    std::vector<std::pair<int,int>> hazards = {{1,2}};
    std::pair<int,int> start = {4,0};

    grid_construct(grid, nodes, size, obstacles);
    node_get_neighbors(grid, nodes);
    node_set_d_exit(nodes, exits);
    hazard_wavefront(nodes, hazards);

    auto safe = safeStar_path(nodes, grid, start, exits);

    for (auto& n : nodes) { n.cost = std::numeric_limits<double>::infinity(); n.backpointer = -1; }
    auto classic = classic_a_star(nodes, grid, start, exits);

    auto min_safety = [&](const std::vector<int>& path) {
        int m = std::numeric_limits<int>::max();
        for (int id : path) m = std::min(m, nodes[id-1].safety_score);
        return m;
    };

    REQUIRE_FALSE(safe.empty());
    REQUIRE_FALSE(classic.empty());
    REQUIRE(min_safety(safe) > min_safety(classic));
}
