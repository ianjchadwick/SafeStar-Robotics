cmake_minimum_required(VERSION 3.10)
project(SafeStar-Robotics)

set(CMAKE_CXX_STANDARD 17)

# If you still want to build your MCU/main demo:
# add_executable(SafeStar-Robotics src/main.cpp)

# C++ Demo Library (point to new src path)
add_library(safestar STATIC apps/src/safeStar.cpp)
target_include_directories(safestar PUBLIC ${CMAKE_SOURCE_DIR}/apps/include)

# C++ Demo Executable (point to new src path)
add_executable(safeStar_demo apps/src/safeStar_demo.cpp)
target_link_libraries(safeStar_demo PRIVATE safestar)
target_compile_features(safeStar_demo PRIVATE cxx_std_17)

# Add unit tests
enable_testing()
add_subdirectory(test)
