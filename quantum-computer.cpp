#include "quantum-computer.h"

const double prf = 1 / sqrt(2);
const complex<double>  rf(prf, prf);
const Matrix2cd hadamardMatrix((Matrix2cd() << prf, prf, prf, -prf).finished());
const Matrix2cd rzMatrix((Matrix2cd() << 1, 0, 0, rf).finished());
const Matrix4cd cNotMatrix((Matrix4cd() << 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0).finished());
const Matrix2cd identity((Matrix2cd() << 1, 0, 0, 1).finished());

void printDna(VectorXi dna) {
	for (unsigned int i = 0; i < dna.size(); i++)
	{
		cout << dna[i];
	}
	cout << endl;
}

void QuantumComputer::SetNumQBits(int qbits) {
	numQBits = qbits;
}

void QuantumComputer::ApplyGate(int position, MatrixXcd gate) {
	MatrixXcd circuit;
	MatrixXcd factor;
	int i = 0;
	while (circuit.rows() < states.size()) { 
		if (i == position) {
			factor = gate;
		} else {
			factor = identity;
		}
		
		if (i == 0) {
			circuit = factor;
		} else {
			circuit = kroneckerProduct(circuit, factor).eval();
		};
		i++;
	}	
	
	VectorXcd temp = states;
	for (unsigned int i = 0; i < states.size(); i++) {
        for (unsigned int j = 0; j < circuit.cols(); j++) {
			states[i] += (circuit(i, j) * temp[i]);
        }
    }
	states.normalize();
}

void QuantumComputer::ApplyTwoQBitGate(int pos_a, int pos_b, Matrix4cd gate) {
	MatrixXcd circuit;
	MatrixXcd factor;
	
	if (pos_a > pos_b) {
		int t = pos_a;
		pos_a = pos_b;
		pos_b = t;
		
		gate = gate.rowwise().reverse();
	}
	
	ApplyGate(pos_a, gate);
}

void QuantumComputer::ApplyAlgorithm (VectorXi algorithm) {
	/* Quantum Gate representations:
	 * 0: Idenity Gate
	 * 1: Hadamard
	 * 2: RZ Pi / 4
	 * 3: CNot
	 */
	
	for (unsigned int i; i < algorithm.size(); i++) {
		int q = i % numQBits;
		if (algorithm[i] == 1) {
			ApplyGate(q, hadamardMatrix);
		} else if (algorithm[i] == 2) {
			ApplyGate(q, rzMatrix);
		} else if (algorithm[i] == 3) {
			if (q < numQBits - 1) {
				int a = rand() % 2;
				if (a == 0) {
					ApplyTwoQBitGate(q, q + 1, cNotMatrix);
				} else {
					ApplyTwoQBitGate(q + 1, q, cNotMatrix);
				}
				continue;
			}
		}
	}	
}
