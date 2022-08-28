import numbers
from typing import List, Tuple

from numpy import ndarray

from QuantumComputer import QuantumComputer, Gate, Probability
import numpy as np

# Quantum Gate to Number Map:
# Identity: 0
# T: 1
# Hadamard: 2
# CNOT: 3


def quantum_gate_switch(quantum_computer: QuantumComputer, gates: List[str], array_value: complex, index: int) \
        -> QuantumComputer:
    match array_value:
        case 1:
            quantum_computer.apply_gate(Gate.T, gates[index])
        case 2:
            quantum_computer.apply_gate(Gate.H, gates[index])
        case 3:
            if index < len(gates):
                quantum_computer.apply_two_qubit_gate_CNOT(gates[index], gates[index + 1])
        case 4:
            if index > 0:
                quantum_computer.apply_two_qubit_gate_CNOT(gates[index - 1], gates[index])

    return quantum_computer


def apply_quantum_gates(quantum_computer: QuantumComputer, gates: List[str], gate_array: ndarray) -> QuantumComputer:
    gate_array = remove_redundant_gate_series(cnot_two_gate_operation(gate_array))

    for k in range(len(gate_array)):
        for i in range(len(gate_array[k])):
            quantum_computer = quantum_gate_switch(quantum_computer, gates, gate_array[k][i], i)

    return quantum_computer


def quantum_gate_output_switch(array_value: complex) -> str:
    output_string = ''
    match array_value:
        case 0:
            output_string = '|'
        case 1:
            output_string = 'T'
        case 2:
            output_string = 'H'
        case 3:
            output_string = '. - (+)'
        case 4:
            output_string = '(+) - .'

    return output_string


def remove_redundant_gate_series(gate_array: ndarray) -> ndarray:
    col_length = len(gate_array)
    for k in range(col_length):
        for i in range(len(gate_array[1])):
            remove_redundant_gate(gate_array, k, i, col_length)

    return gate_array


def remove_redundant_gate(gate_array: ndarray, idx_1: int, idx_2: int, column_length: int):
    if gate_array[idx_1][idx_2] == 2 or gate_array[idx_1][idx_2] == 3 or gate_array[idx_1][idx_2] == 4:
        if idx_1 > 0 and gate_array[idx_1][idx_2] == gate_array[idx_1 - 1][idx_2]:
            gate_array[idx_1][idx_2] = 0
            gate_array[idx_1 - 1][idx_2] = 0

        if idx_1 < (column_length - 1) and gate_array[idx_1][idx_2] == gate_array[idx_1 + 1][idx_2]:
            gate_array[idx_1][idx_2] = 0
            gate_array[idx_1 + 1][idx_2] = 0


def output_quantum_gates(gate_array: ndarray) -> None:
    for k in range(len(gate_array)):
        output_string = ''
        i = 0

        while i < len(gate_array[k]):
            if gate_array[k][i] < 3:
                output_string += '     ' + quantum_gate_output_switch(gate_array[k][i])
                i += 1
            else:
                output_string += '     ' + quantum_gate_output_switch(gate_array[k][i])
                i += 2

        print(output_string)


def cnot_two_gate_operation(gate_array: ndarray) -> ndarray:
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
                if i > 0:
                    gate_array[k][i - 1] = 4
                    gate_array[k][i] = 0
                else:
                    gate_array[k][i] = 0
    return gate_array


def run_quantum_algorithm(input_state: ndarray, gates: List[str], gate_array: ndarray) -> ndarray:
    quantum_computer = initialise_quantum_computer(input_state, gates)

    quantum_computer = apply_quantum_gates(quantum_computer, gates, gate_array)

    return measure_quantum_output(quantum_computer, gates)


def initialise_quantum_computer(input_state: ndarray, gates: List[str]) -> QuantumComputer:
    quantum_computer = QuantumComputer()

    gate_length = len(gates)

    if input_state[1] == 1:
        quantum_computer.apply_gate(Gate.X, "q0")

    if gate_length > 1 and input_state[3] == 1:
        quantum_computer.apply_gate(Gate.X, "q1")

    if gate_length > 2 and input_state[5] == 1:
        quantum_computer.apply_gate(Gate.X, "q2")

    if gate_length > 3 and input_state[7] == 1:
        quantum_computer.apply_gate(Gate.X, "q3")

    if gate_length > 4 and input_state[9] == 1:
        quantum_computer.apply_gate(Gate.X, "q4")

    return quantum_computer


def measure_quantum_output(quantum_computer: QuantumComputer, gates: List[str]) -> ndarray:
    state = quantum_computer.qubits.get_quantum_register_containing(gates[0]).get_state()
    probability = Probability.get_probabilities(state)

    # Remove any solutions that are not fully entangled due to input/ output requirements.
    if len(probability) != 2 ** len(gates):
        probability = np.empty((2 ** len(gates),)) * np.nan

    return np.asarray(probability)


def run_quantum_algorithm_over_set(input_set: ndarray, target_set: ndarray, gates: List[str], gate_array: ndarray) \
        -> Tuple[float]:
    probabilities = np.zeros((len(input_set), 2 ** len(gates)))

    for i in range(len(input_set)):
        probabilities[i, :] = run_quantum_algorithm(input_set[i, :], gates, gate_array)

    score = - 1.0 - np.abs(np.sum((probabilities - target_set) / (len(target_set)) ** 2))

    if np.isnan(score):
        score = -2.0

    if score == -1.0:
        score /= (1.0 + count_blank_rows(gate_array))

    return float(score),


def count_blank_rows(gate_array: ndarray) -> int:
    blank_counter = 0
    for row in gate_array:
        if sum(row) == 0:
            blank_counter += 1

    return blank_counter
