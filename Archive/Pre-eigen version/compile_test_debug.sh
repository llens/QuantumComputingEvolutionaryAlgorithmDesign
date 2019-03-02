#!/bin/bash

g++ -g tests-quantum-computer.cpp quantum-computer.cpp \
evolutionary-algorithm.cpp \
 quantum-test-generator.cpp catch-main.cpp -std=c++11 \
  -I /usr/include -o catch-test.o

g++ -g tests-quantum-computer.cpp quantum-computer.cpp \
evolutionary-algorithm-parallel.cpp \
 quantum-test-generator.cpp catch-main.cpp -std=c++11 \
  -fopenmp -I /usr/include -o catch-test-parallel.o

g++ -g quantum-computer.cpp \
evolutionary-algorithm-parallel.cpp \
 quantum-test-generator.cpp main-parallel.cpp -std=c++11 \
  -fopenmp -o quantum-algorithm-design-parallel.o

g++ -g quantum-computer.cpp \
evolutionary-algorithm.cpp quantum-test-generator.cpp \
main.cpp -std=c++11 -o quantum-algorithm-design.o

 ./catch-test.o

 ./catch-test-parallel.o
