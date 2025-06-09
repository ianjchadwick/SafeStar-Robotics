#define CATCH_CONFIG_MAIN
#include <catch2/catch_test_macros.hpp>
#include <catch2/catch_approx.hpp>
#include "../include/node.hpp"

#include <limits>

TEST_CASE("Node initializes with correct default values", "[Node]") {
    Node n{};

    SECTION("Default-initialized fields") {
        REQUIRE(n.backpointer == -1);
        REQUIRE(n.d_exit == std::numeric_limits<int>::max());
        REQUIRE(n.safety == std::numeric_limits<int>::max());
        REQUIRE(n.cost == 0.0);
        REQUIRE(n.coords[0] == 0);
        REQUIRE(n.coords[1] == 0);
        REQUIRE(n.neighbors.empty());
    }

    SECTION("Node can be assigned values") {
        n.node_id = 5;
        n.coords = {3, 4};
        n.cost = 12.5;
        n.neighbors = {1, 2, 3};

        REQUIRE(n.node_id == 5);
        REQUIRE(n.coords[0] == 3);
        REQUIRE(n.coords[1] == 4);
        REQUIRE(n.cost == Catch::Approx(12.5));
        REQUIRE(n.neighbors.size() == 3);
        REQUIRE(n.neighbors[2] == 3);
    }
}
