cmake_minimum_required(VERSION 3.13)  # CMake version check
project(quantum-computing-evolutionary-algorithm-design)
set(CMAKE_CXX_STANDARD 14)

set(CMAKE_MODULE_PATH ${PROJECT_SOURCE_DIR})
find_package(Eigen3 REQUIRED 3.4)
include_directories(${EIGEN3_INCLUDE_DIR})

add_library(evolutionary-algorithm STATIC evolutionary-algorithm.cpp evolutionary-algorithm.h)
target_compile_features(evolutionary-algorithm PUBLIC cxx_std_14)

add_library(quantum-computer STATIC quantum-computer.cpp quantum-computer.h)
target_compile_features(quantum-computer PUBLIC cxx_std_14)

add_library(quantum-test-generator STATIC quantum-test-generator.cpp quantum-test-generator.h)
target_compile_features(quantum-test-generator PUBLIC cxx_std_14)

# Add main.cpp file of project root directory as source file
set(SOURCE_FILES main.cpp)

# Add executable target with source files listed in SOURCE_FILES variable
add_executable(quantum-computing-evolutionary-algorithm-design ${SOURCE_FILES})
target_link_libraries(quantum-computing-evolutionary-algorithm-design PUBLIC evolutionary-algorithm)
target_link_libraries(quantum-computing-evolutionary-algorithm-design PUBLIC quantum-computer)
target_link_libraries(quantum-computing-evolutionary-algorithm-design PUBLIC quantum-test-generator)