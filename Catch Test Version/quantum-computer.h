#ifndef QUANTUM_COMPUTER
#define QUANTUM_COMPUTER

#include <iostream>
#include <vector>
#include <algorithm>
#include <complex>
#include <complex.h>
#include <cstdlib>
#include <Eigen/Dense>
#include <unsupported/Eigen/KroneckerProduct>

using namespace std;
using namespace Eigen;

void printDna(VectorXi dna);

class QuantumComputer {
	public:
	int numQBits;
	VectorXcd states;
	void SetNumQBits(int);
	void InputStates(VectorXcd);
	void Hadamard(int);
	void Fredkin(int, int);
	void ApplyAlgorithm(VectorXi);
	void ApplyGate(int, MatrixXcd);
	void ApplyTwoQBitGate(int, int, Matrix4cd);
};
#endif
