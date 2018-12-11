#include <iostream>
#include <vector>
#include <algorithm>
#include <complex>
#include <complex.h>
#include <cstdlib>
#include "quantum-computer.h"
using namespace std;

const double prf = 1 / sqrt(2);

vector< vector< complex<double> > > kroneckerProduct (vector< vector< complex<double> > > A, vector< vector< complex<double> > > B) {
	unsigned int dim = A.size() * B.size();
	vector< vector< complex<double> > > C(
    dim,
    vector< complex<double> >(dim));

    for (unsigned int i = 0; i < A.size(); i++) { 
		for (unsigned int k = 0; k < B.size(); k++) {
			for (unsigned int l = 0; l < A[0].size(); l++) {			 
				for (unsigned int j = 0; j < B[0].size(); j++) {	
					C[i + l][j + k] = (A[i][j] * B[k][l]);
                } 
            } 
        } 
    } 
    return C;
}

vector< vector< complex<double> > > hadamardMatrix () {
	vector< vector< complex<double> > >  hMat(
    2,
    vector< complex<double> >(2));
	hMat[0][0] = hMat[0][1] = hMat[1][0] = prf;
	hMat[1][1] = -prf;
	return hMat;
}

vector< vector< complex<double> > > rzMatrix () {
	vector< vector< complex<double> > >  rzMat(
    2,
    vector< complex<double> >(2));
	rzMat[0][0] = 1;
	rzMat[1][1] = cexp(1i * M_PI_4);
	return rzMat;
}

vector< vector< complex<double> > > cNotMatrix () {
	vector< vector< complex<double> > >  cNMat(
    4,
    vector< complex<double> >(4));
    cNMat[0][0] = cNMat[1][1] = cNMat[2][3] = cNMat[3][2] = 1;
    return cNMat;
}

vector< vector< complex<double> > > identity () {
	vector< vector< complex<double> > >  iMat(
    2,
    vector< complex<double> >(2));
	iMat[0][0] = iMat[1][1] = 1;
	return iMat;
}

void QuantumComputer::SetNumQBits (int qbits) {
	numQBits = qbits;
}

void QuantumComputer::InputStates (vector< complex<double> > input) {
	states.clear();
	for(int i = 0; i < pow(2, numQBits); i++)
	{
		states.push_back(input[i]);    
	}
	Normalise();
}

void QuantumComputer::Normalise () {
	double sum;
	for (unsigned int i = 0; i < states.size(); i++) {
		sum += norm(states[i]);
	}

	if (sum != 0) {
		for (unsigned int i = 0; i < states.size(); i++) {
			states[i] /= sum;
		}
	}
}

void QuantumComputer::ApplyOneQBitGate (int position, vector< vector< complex<double> > > gate) {
	vector< vector< complex<double> > > circuit;
	vector< vector< complex<double> > > factor;
	for (int i; i < numQBits; i++) {
		if (i == position) {
			factor = gate;
		} else {
			factor = identity();
		}
		
		if (i == 0) {
			circuit = factor;
		} else {
			circuit = kroneckerProduct(circuit, factor);
		};
	}	
	
	vector< complex<double> > temp = states;
	for (unsigned int i = 0; i < circuit.size(); i++) {
        for (unsigned int j = 0; j < circuit[0].size(); j++) {
			states[i] += ( circuit[i][j] * temp[j]);
        }
    }
	Normalise();
}

void QuantumComputer::ApplyTwoQBitGate (int pos_a, int pos_b, vector< vector< complex<double> > > gate) {
	vector< vector< complex<double> > > circuit;
	vector< vector< complex<double> > > factor;
	
	if (pos_a > pos_b) {
		int t = pos_a;
		pos_a = pos_b;
		pos_b = t;
		
		reverse(gate.begin(), gate.end());
	}
	
	int i = 0;
	while (i < numQBits) {
		if (i == pos_a) {
			factor = gate;
			i++;
		} else {
			factor = identity();
		}
		
		if (i == 0) {
			circuit = factor;
		} else {
			circuit = kroneckerProduct(circuit, factor);
		};
		i++;
	}	
	
	vector< complex<double> > temp = states;
	for (unsigned int i = 0; i < circuit.size(); i++) {
        for (unsigned int j = 0; j < circuit[0].size(); j++) {
            states[i]+=( circuit[i][j] * temp[j]);
        }
    }
	Normalise();
}

void QuantumComputer::ApplyAlgorithm (vector<int> algorithm) {
	/* Quantum Gate representations:
	 * 0: Idenity Gate
	 * 1: Hadamard
	 * 2: RZ Pi / 4
	 * 3: CNot
	 */
	
	for (unsigned int i; i < algorithm.size(); i++) {
		int q = i % numQBits;
		if (algorithm[i] == 1) {
			ApplyOneQBitGate(q, hadamardMatrix());
		} else if (algorithm[i] == 2) {
			ApplyOneQBitGate(q, rzMatrix());
		} else if (algorithm[i] == 3) {
			if (q < numQBits - 1) {
				int a = rand() % 2;
				if (a == 0) {
					ApplyTwoQBitGate(q, q + 1, cNotMatrix());
				} else {
					ApplyTwoQBitGate(q + 1, q, cNotMatrix());
				}
				continue;
			}
		}
	}	
}
