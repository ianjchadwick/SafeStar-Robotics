cmake_minimum_required(VERSION 3.10)
project(SafeStar-Robotics)

set(CMAKE_CXX_STANDARD 17)

add_executable(SafeStar-Robotics src/main.cpp)

# Add unit tests
enable_testing()
add_subdirectory(test)
