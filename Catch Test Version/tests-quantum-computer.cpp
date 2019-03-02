#include <math.h>
#include <complex>
#include <vector>
#include <iostream>
#include <cstdlib>
#include "catch.hpp"
#include "quantum-computer.h"
#include <Eigen/Dense>

int QBITMIN = 2;
int QBITMAX = 5;
int NTEST = 5;
double TOL = 1E-15;

double random_double() {
    return (rand() - RAND_MAX / 2.0) / (RAND_MAX / 2.0 + 1.);
}

int random_int(int l_lim, int u_lim) {
    return l_lim + rand() % (u_lim - l_lim);
}

vector< complex<double> > normalise(vector< complex<double> > input_state) {
        double sum = 0;
        for (unsigned int i = 0; i < input_state.size(); i++) {
            sum += abs(input_state[i]);
        }

        if (sum != 0) {
            for (unsigned int i = 0; i < input_state.size(); i++) {
                input_state[i] /= sum;
            }
        }
        return input_state;
}

TEST_CASE("1: Set quantum computer Qbits", "[quantum computer]") {
    for (int i = QBITMIN; i <= QBITMAX; i++) {
            QuantumComputer* quant_comp = new QuantumComputer();
            quant_comp -> SetNumQBits(i);
            REQUIRE(quant_comp -> numQBits == i);
            delete quant_comp;
    }
}


/*TEST_CASE("3: Quantum computer input states mapped correctly", "[quantum computer]" ) {
    double a;
    double b;
    double diff;
    int n = 0;
    
    while (n < NTEST) {
        n++;
        for (int i = QBITMIN; i <= QBITMAX; i++) {
            int num_states = pow(2, i);
            vector< complex<double> > input_state = generate_random_vector(num_states);

            input_state = normalise(input_state);

            QuantumComputer* quant_comp = new QuantumComputer();
            quant_comp -> SetNumQBits(i);
            quant_comp -> InputStates(input_state);

            diff = 0;
            for (unsigned int j = 0; j < num_states; j++) {
                diff += abs(quant_comp -> states[j] - input_state[j]);
            }

            REQUIRE(abs(diff) <= TOL);
            delete quant_comp;
        }
    }
} */
