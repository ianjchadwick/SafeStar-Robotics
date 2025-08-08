cmake_minimum_required(VERSION 3.10)
project(SafeStar-Robotics)

set(CMAKE_CXX_STANDARD 17)

# WIP MCU Implementation
add_executable(SafeStar-Robotics src/main.cpp)

# C++ Demo APP
add_library(safestar STATIC src/safestar.cpp)
target_include_directories(safestar PUBLIC ${CMAKE_SOURCE_DIR}/include)

add_executable(hazard_demo apps/hazard_demo.cpp)
target_link_libraries(hazard_demo PRIVATE safestar)
target_compile_features(hazard_demo PRIVATE cxx_std_17)

# Add unit tests
enable_testing()
add_subdirectory(test)


