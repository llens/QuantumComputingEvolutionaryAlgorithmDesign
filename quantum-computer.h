#ifndef QUANTUM_COMPUTER
#define QUANTUM_COMPUTER

#include <vector>
#include <complex>

using namespace std;

class QuantumComputer {
	public:
	int numQBits;
	vector< complex<double> > states;
	void SetNumQBits (int);
	void InputStates (vector< complex<double> >);
	void Hadamard (int);
	void Fredkin (int, int);
	void ApplyAlgorithm (vector<int> algorithm);
	void ApplyOneQBitGate (int, vector< vector< complex<double> > >);
	void ApplyTwoQBitGate (int, int, vector< vector< complex<double> > >);
	void Normalise ();
};
#endif
