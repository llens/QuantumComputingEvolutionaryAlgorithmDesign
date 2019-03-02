#include <vector>
#include <cstdlib>
#include <complex>
#include <complex.h>
#include <math.h>
#include "quantum-test-generator.h"
using namespace std;

void QuantumTestGenerator::Init (int nQBits) {
	numQBits = nQBits;
};

void QuantumTestGenerator::GenerateInput () {
	for(int i = 0; i < numQBits; i++)
	{
		double a = (rand() - RAND_MAX / 2.0) / (RAND_MAX / 2.0 + 1.);
		double b = (rand() - RAND_MAX / 2.0) / (RAND_MAX / 2.0 + 1.);
		input.push_back({a, b});    
	}
};

void QuantumTestGenerator::QuantumFourierTransform () {
	double n = log2(numQBits);
	for (int i = 0; i < numQBits; i++) {
		output.push_back(0.0);
		for (int j = 0; j < numQBits; j++) {
			complex<double> root = cexp(2 * M_PI * sqrt(-1) * i * j / n);
			output[i] += root * input[i];
		}
	}
};

void QuantumTestGenerator::Next () {
	input.clear();
	output.clear();
	GenerateInput();
	QuantumFourierTransform();
	input = Normalise(input);
	output = Normalise(output);
};

vector <complex <double> > QuantumTestGenerator::Normalise (vector <complex <double> > vec) {
		double sum;
	for (unsigned int i = 0; i < vec.size(); i++) {
		sum += norm(vec[i]);
	}

	if (sum != 0) {
		for (unsigned int i = 0; i < vec.size(); i++) {
			vec[i] /= sum;
		}
	}
	return vec;
}
