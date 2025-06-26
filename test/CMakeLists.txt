include(FetchContent)

FetchContent_Declare(
  Catch2
  GIT_REPOSITORY https://github.com/catchorg/Catch2.git
  GIT_TAG v3.5.4
)
FetchContent_MakeAvailable(Catch2)

include(Catch)  # <-- must be here, after FetchContent_MakeAvailable

# Node tests
add_executable(test_node test_node.cpp)
target_include_directories(test_node PRIVATE ../include)
target_link_libraries(test_node PRIVATE Catch2::Catch2WithMain)
catch_discover_tests(test_node)

# BitGrid tests
add_executable(test_bitgrid test_bitgrid.cpp)
target_include_directories(test_bitgrid PRIVATE ../include)
target_link_libraries(test_bitgrid PRIVATE Catch2::Catch2WithMain)
catch_discover_tests(test_bitgrid)
