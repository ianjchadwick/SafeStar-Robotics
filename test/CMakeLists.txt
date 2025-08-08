cmake_minimum_required(VERSION 3.16)

find_package(Catch2 3 REQUIRED CONFIG)

add_executable(test_safeStar
  ${CMAKE_SOURCE_DIR}/test/test_safety_wavefront.cpp
)
target_link_libraries(test_safeStar PRIVATE
  safestar
  Catch2::Catch2WithMain
)
target_compile_features(test_safeStar PRIVATE cxx_std_17)

include(Catch)
catch_discover_tests(test_safeStar)
