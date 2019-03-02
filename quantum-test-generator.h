#ifndef QUANTUM_TEST_GENERATOR
#define QUANTUM_TEST_GENERATOR

#include <vector>
#include <complex>
#include <Eigen/Dense>

using namespace std;
using namespace Eigen;

class QuantumTestGenerator {
	public:
	int numQBits;
	VectorXcd input;
	VectorXcd output;
	
	void Init (int);
	void Next ();
	void GenerateInput ();
	void QuantumFourierTransform ();
};

#endif
