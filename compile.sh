#!/bin/bash

g++ -g -O3 quantum-computer.cpp \
evolutionary-algorithm-parallel.cpp \
 quantum-test-generator.cpp main-parallel.cpp -std=c++11 \
  -fopenmp -o quantum-algorithm-design-parallel.o

g++ -g -O3 quantum-computer.cpp \
evolutionary-algorithm.cpp quantum-test-generator.cpp \
main.cpp -std=c++11 -o quantum-algorithm-design.o
