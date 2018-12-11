#ifndef QUANTUM_TEST_GENERATOR
#define QUANTUM_TEST_GENERATOR

#include <vector>
#include <complex>

using namespace std;

class QuantumTestGenerator {
	public:
	int numQBits;
	vector <complex <double> > input;
	vector <complex <double> > output;
	
	void Init (int);
	void Next ();
	void GenerateInput ();
	void QuantumFourierTransform ();
	vector <complex <double> > Normalise (vector <complex <double> >);
};

#endif
