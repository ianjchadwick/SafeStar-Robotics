# test/CMakeLists.txt

include(FetchContent)

FetchContent_Declare(
  Catch2
  GIT_REPOSITORY https://github.com/catchorg/Catch2.git
  GIT_TAG v3.5.4
)
FetchContent_MakeAvailable(Catch2)

add_executable(test_node test_node.cpp)
target_include_directories(test_node PRIVATE ../include)
target_link_libraries(test_node PRIVATE Catch2::Catch2WithMain)

include(CTest)
include(Catch)
catch_discover_tests(test_node)
