from QuantumComputer import QuantumComputer, Gate, Probability
import numpy as np

# Quantum Gate to Number Map:
# Identity: 0
# T: 1
# Hadamard: 2
# CNOT: 3


def quantum_gate_switch(quantum_computer, gates, array_value, index):
    if array_value == 1:
        quantum_computer.apply_gate(Gate.T, gates[index])
    elif array_value == 2:
        quantum_computer.apply_gate(Gate.H, gates[index])
    elif array_value == 3:
        if index < len(gates):
            quantum_computer.apply_two_qubit_gate_CNOT(gates[index], gates[index + 1])
    elif array_value == 4:
        if index > 0:
            quantum_computer.apply_two_qubit_gate_CNOT(gates[index - 1], gates[index])

    return quantum_computer


def apply_quantum_gates(quantum_computer, gates, gate_array):
    gate_array = cnot_two_gate_operation(gate_array)

    for k in range(len(gate_array)):
        for i in range(len(gate_array[k])):
            quantum_computer = quantum_gate_switch(quantum_computer, gates, gate_array[k][i], i)

    return quantum_computer


def quantum_gate_output_switch(gates, array_value, index):
    if array_value == 0:
        output_string = '|'
    elif array_value == 1:
        output_string = 'T'
    elif array_value == 2:
        output_string = 'H'
    elif array_value == 3:
        if index < len(gates):
            output_string = '. - (+)'
    elif array_value == 4:
        if index > 0:
            output_string = '(+) - .'

    return output_string


def output_quantum_gates(gates, gate_array):
    for k in range(len(gate_array)):
        output_string = ''
        i = 0

        while i < len(gate_array[k]):
            if gate_array[k][i] < 3:
                output_string += '    ' + quantum_gate_output_switch(gates, gate_array[k][i], i)
                i += 1
            else:
                output_string += '    ' + quantum_gate_output_switch(gates, gate_array[k][i], i)
                i += 2

        print output_string


def cnot_two_gate_operation(gate_array):
    row_length = len(gate_array[1])
    for k in range(len(gate_array)):
        for i in range(row_length):
            if gate_array[k][i] == 3:
                if i < row_length - 1:
                    gate_array[k][i + 1] = 0
                else:
                    gate_array[k][i] = 0

    for k in range(len(gate_array)):
        for i in range(row_length):
            if gate_array[k][i] == 4:
                if i < 0:
                    gate_array[k][i - 1] = 0
                else:
                    gate_array[k][i] = 0
    return gate_array


def run_quantum_algorithm(input_state, gates, gate_array):
    quantum_computer = initialise_quantum_computer(input_state)

    quantum_computer = apply_quantum_gates(quantum_computer, gates, gate_array)

    return measure_quantum_output(quantum_computer, gates)


def initialise_quantum_computer(input_state):
    quantum_computer = QuantumComputer()

    if input_state[1] == 1:
        quantum_computer.apply_gate(Gate.X, "q1")

    if input_state[3] == 1:
        quantum_computer.apply_gate(Gate.X, "q2")

    if input_state[5] == 1:
        quantum_computer.apply_gate(Gate.X, "q3")

    return quantum_computer


def measure_quantum_output(quantum_computer, gates):
    state = quantum_computer.qubits.get_quantum_register_containing(gates[0]).get_state()
    probability = Probability.get_probabilities(state)

    #Remove any solutions that are not fully entangled due to input/ output requirements.
    if len(probability) != 2 ** len(gates):
        probability = np.empty((2 ** len(gates),)) * np.nan

    return probability


def run_quantum_algorithm_over_set(input_set, target_set, gates, gate_array):
    probabilities = np.zeros((len(input_set), 2 ** len(gates)))

    for i in range(len(input_set)):
        probabilities[i, :] = run_quantum_algorithm(input_set[i, :], gates, gate_array)

    score = - 1 - np.sum((probabilities - target_set) ** 2) / (2 ** len(gates))

    if np.isnan(score) :
        score = -2

    if score == -1:
        score /= (1 + count_blank_rows(gate_array))

    return score,


def count_blank_rows(gate_array):
    blank_counter = 0
    for row in gate_array:
        if sum(row) == 0:
            blank_counter += 1

    return blank_counter


def invert_targets(input_arr):
    return np.mod(input_arr + np.ones(input_arr.shape), 2)
