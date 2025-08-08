cmake_minimum_required(VERSION 3.16)

if (NOT BUILD_TESTING)
  return()
endif()


find_package(Catch2 3 CONFIG QUIET)
if (NOT Catch2_FOUND)
  include(FetchContent)
  FetchContent_Declare(
    catch2
    GIT_REPOSITORY https://github.com/catchorg/Catch2.git
    GIT_TAG v3.5.3
  )
  FetchContent_MakeAvailable(catch2)
endif()

add_executable(test_safeStar
  ${CMAKE_SOURCE_DIR}/test/test_safety_wavefront.cpp
)

target_link_libraries(test_safeStar PRIVATE
  safestar
  Catch2::Catch2WithMain
)


target_include_directories(test_safeStar PRIVATE
  ${CMAKE_SOURCE_DIR}/apps/include
)

target_compile_features(test_safeStar PRIVATE cxx_std_17)

include(Catch)
catch_discover_tests(test_safeStar)
