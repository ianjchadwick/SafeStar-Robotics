#define CATCH_CONFIG_MAIN
#include <catch2/catch_test_macros.hpp>
#include "../include/bitgrid.hpp"

TEST_CASE("BitGrid basic functionality", "[BitGrid]") {
    constexpr std::size_t W = 8;
    constexpr std::size_t H = 8;
    BitGrid<W, H> grid;

    SECTION("Initial state is all false") {
        for (std::size_t y = 0; y < H; ++y) {
            for (std::size_t x = 0; x < W; ++x) {
                REQUIRE(grid.get(x, y) == false);
            }
        }
    }

    SECTION("Set and get work correctly") {
        grid.set(3, 2, true);
        REQUIRE(grid.get(3, 2) == true);

        grid.set(3, 2, false);
        REQUIRE(grid.get(3, 2) == false);

        grid.set(0, 0, true);
        grid.set(7, 7, true);
        REQUIRE(grid.get(0, 0) == true);
        REQUIRE(grid.get(7, 7) == true);
    }

    SECTION("Does not affect neighboring bits") {
        grid.set(4, 4, true);
        for (std::size_t y = 0; y < H; ++y) {
            for (std::size_t x = 0; x < W; ++x) {
                if (x == 4 && y == 4) continue;
                REQUIRE(grid.get(x, y) == false);
            }
        }
    }

    SECTION("width() and height() return correct values") {
        REQUIRE(grid.width() == W);
        REQUIRE(grid.height() == H);
    }
}
