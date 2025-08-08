#include <catch2/catch_test_macros.hpp>
#include "safeStar.hpp"
#include <algorithm>

static int safety_at(const std::vector<Node>& nodes, int x, int y) {
    for (auto& n : nodes) if (n.x == x && n.y == y) return n.safety_score;
    return -1; // not found / obstacle
}

TEST_CASE("Wavefront safety increases with distance from hazard") {
    int size = 5;
    Grid grid;
    std::vector<Node> nodes;
    std::vector<std::tuple<int,int,int,int>> obstacles = {}; // none
    std::vector<std::pair<int,int>> exits = {{0,4}};
    std::vector<std::pair<int,int>> hazards = {{0,0}};

    grid_construct(grid, nodes, size, obstacles);
    node_get_neighbors(grid, nodes);
    node_set_d_exit(nodes, exits);
    hazard_wavefront(nodes, hazards);

    REQUIRE(safety_at(nodes, 0, 0) == 0);   // on hazard
    REQUIRE(safety_at(nodes, 0, 1) == 1);   // neighbors grow
    REQUIRE(safety_at(nodes, 1, 0) == 1);
    REQUIRE(safety_at(nodes, 1, 1) == 2);
    REQUIRE(safety_at(nodes, 2, 2) >= safety_at(nodes, 1, 1));
}

TEST_CASE("SafeStar avoids hazard-adjacent cells when an equal-length route exists") {
    // Map forces a tie on path length; one route hugs hazard, the other detours safely.
    int size = 5;
    Grid grid;
    std::vector<Node> nodes;
    // Put a small wall to create two equal-length corridors
    std::vector<std::tuple<int,int,int,int>> obstacles = {
        {2,1,1,3} // vertical wall at x=2, y=1..3
    };
    std::vector<std::pair<int,int>> exits = {{0,4}};     // exit top-right row end
    std::vector<std::pair<int,int>> hazards = {{1,2}};   // hazard next to left corridor
    std::pair<int,int> start = {4,0};                    // bottom-left

    grid_construct(grid, nodes, size, obstacles);
    node_get_neighbors(grid, nodes);
    node_set_d_exit(nodes, exits);
    hazard_wavefront(nodes, hazards);

    // Run SafeStar then Classic
    auto safe = safeStar_path(nodes, grid, start, exits);

    // reset node state before second search
    for (auto& n : nodes) { n.cost = std::numeric_limits<double>::infinity(); n.backpointer = -1; }

    auto classic = classic_a_star(nodes, grid, start, exits);

    // Helper: min safety along a path
    auto min_safety = [&](const std::vector<int>& path) {
        int m = std::numeric_limits<int>::max();
        for (int id : path) m = std::min(m, nodes[id-1].safety_score);
        return m;
    };

    REQUIRE_FALSE(safe.empty());
    REQUIRE_FALSE(classic.empty());

    // Both should reach the exit
    REQUIRE(safe.front() != 0);
    REQUIRE(classic.front() != 0);

    // SafeStar should have strictly higher worst-case safety along its path
    REQUIRE(min_safety(safe) > min_safety(classic));
}
