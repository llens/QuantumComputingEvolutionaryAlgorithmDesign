#include <complex>
#include <math.h>
#include "quantum-test-generator.h"
using namespace std;

void QuantumTestGenerator::Init (int nQBits) {
	numQBits = nQBits;
}

void QuantumTestGenerator::QuantumFourierTransform () {
	output = VectorXcd::Zero(pow(2, numQBits));
	double n = log2(numQBits);
		complex<double> operand;
		complex<double> root;

	for (int i = 0; i < numQBits; i++) {
		for (int j = 0; j < numQBits; j++) {
			operand = {0, (2 * M_PI * i * j) / n};
			root = exp(operand);
			output[i] += root * input[i];
		}
	}
}

void QuantumTestGenerator::Next () {
	input = VectorXcd::Random(pow(2, numQBits));
	input.normalize();
	QuantumFourierTransform();
}
