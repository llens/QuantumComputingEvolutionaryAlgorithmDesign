from QuantumComputer import Probability
from evolutionary_algorithm import evolve_algorithm
from quantum_computer_operations import invert_targets
import numpy as np


def print_quantum_states(quantum_computer, quantum_register):
    Probability.pretty_print_probabilities(
        quantum_computer.qubits.get_quantum_register_containing(quantum_register).get_state())


def underlined_output(string):
    print string
    print '----------------------'

if __name__ == "__main__":
    #Sum of probabilities exceeds ones as not yet entangled.
    input_set = np.asarray([[0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1,],
                            [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0,],
                            np.random.randint(0, 1, 2 ** 5)])

    targets = np.zeros(input_set.shape)

    for i in range(len(input_set)):
        targets[i, :] = invert_targets(input_set[i, :])
        targets[i, :] /= sum(targets[i, :])

    gates = ["q0", "q1", "q2", "q3", "q4"]

    evolve_algorithm(input_set, targets, gates)
