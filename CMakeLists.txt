cmake_minimum_required(VERSION 3.16)
project(SafeStar-Robotics LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Warnings
if (MSVC)
  add_compile_options(/W4)
else()
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Library: safestar
add_library(safestar STATIC
  apps/src/safeStar.cpp
)
target_include_directories(safestar PUBLIC
  ${CMAKE_SOURCE_DIR}/apps/include
)

# Demo executable
add_executable(safeStar_demo
  apps/src/safeStar_demo.cpp
)
target_link_libraries(safeStar_demo PRIVATE safestar)

# Tests
include(CTest)
enable_testing()
add_subdirectory(test)
