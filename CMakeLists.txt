cmake_minimum_required(VERSION 3.10)
project(TestAgent)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

enable_testing()

include_directories(/usr/include)

add_executable(runTests
    tests/test_test.cpp
    app/test.c
)

target_link_libraries(runTests gtest gtest_main pthread)

