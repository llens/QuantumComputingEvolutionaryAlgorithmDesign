from QuantumComputerModified import QuantumComputer, Gate, Probability
from evolutionary_algorithm import evolve_algorithm
from quantum_computer_operations import invert_targets
import numpy as np


def output_all_quantum_gates(quantum_computer_local, gates_local):
    for gate in gates_local:
        underlined_output(gate)
        print_quantum_states(quantum_computer_local, "q1")
        print "\n"


def print_quantum_states(quantum_computer, quantum_register):
    Probability.pretty_print_probabilities(
        quantum_computer.qubits.get_quantum_register_containing(quantum_register).get_state())


def underlined_output(string):
    print string
    print '----------------------'

if __name__ == "__main__":
    #Sum of probabilities exceeds ones as not yet entangled.
    input_set = np.asarray([[0, 1, 1, 0],
                            [1, 0, 0, 1]])

    targets = np.zeros(input_set.shape)

    for i in range(len(input_set)):
        targets[i, :] = invert_targets(input_set[i, :])
        targets[i, :] /= sum(targets[i, :])

    gates = ["q1", "q2"]

    evolve_algorithm(input_set, targets, gates)





