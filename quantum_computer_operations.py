from typing import List, Tuple

import numpy as np
from numpy import ndarray
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

from QuantumComputer import QuantumComputer


def quantum_gate_switch(qc: QuantumCircuit, array_value: complex, index: int, gates: List[str]):
    num_qubits = qc.num_qubits
    match array_value:
        case 1:  # T gate
            qc.t(index)
        case 2:  # Hadamard gate
            qc.h(index)
        case 3:  # CNOT gate
            if index + 1 < num_qubits:
                qc.cx(index, index + 1)
        case 4:
            if index > 0:
                qc.cx(index -1, index)

def apply_quantum_gates(qc: QuantumCircuit, gates: List[str], gate_array: ndarray) -> QuantumCircuit:
    gate_array = remove_redundant_gate_series(cnot_two_gate_operation(gate_array))

    for k in range(len(gate_array)):
        for i in range(len(gate_array[k])):
            quantum_gate_switch(qc, gate_array[k][i], i, gates)

    return qc


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
    if gate_array[idx_1][idx_2] >= 2 and idx_1 > 0 and gate_array[idx_1][idx_2] == gate_array[idx_1 - 1][idx_2]:
        gate_array[idx_1][idx_2] = 0
        gate_array[idx_1 - 1][idx_2] = 0

    if gate_array[idx_1][idx_2] >= 2 and idx_1 < (column_length - 1) and gate_array[idx_1][idx_2] == gate_array[idx_1 + 1][idx_2]:
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
    if gate_array.ndim == 1:
        gate_array = np.reshape(gate_array, (1, len(gate_array)))

    row_length = gate_array.shape[1]
    for k in range(len(gate_array)):
        for i in range(row_length):

            if gate_array[k][i] == 3:
                if i < row_length - 1:
                    gate_array[k][i + 1] = 0
                else:
                    gate_array[k][i] = 0

            if gate_array[k][i] == 4:
                if i > 0:
                    gate_array[k][i - 1] = 4
                    gate_array[k][i] = 0
                else:
                    gate_array[k][i] = 0
    return gate_array

def run_quantum_algorithm(input_state: ndarray, gates: List[str], gate_array: ndarray) -> ndarray:
    qc = initialise_quantum_circuit(input_state, gates)

    qc = apply_quantum_gates(qc, gates, gate_array)

    return measure_quantum_output(qc)

def initialise_quantum_circuit(input_state: ndarray, gates: List[str]) -> QuantumCircuit:
    num_qubits = len(gates)
    qc = QuantumCircuit(num_qubits, num_qubits)

    for i, state_val in enumerate(input_state):
        if state_val == 1 and i < num_qubits:
            qc.x(i)

    return qc

def measure_quantum_output(qc: QuantumCircuit) -> ndarray:
    num_qubits = qc.num_qubits
    qc.measure(range(num_qubits), range(num_qubits))
    
    simulator = AerSimulator()
    result = simulator.run(qc, shots=1, memory=True).result()
    measured_state_str = result.get_memory()[0]
    
    # Convert the measured state string (e.g., '010') to a probability vector
    probabilities = np.zeros(2**num_qubits)
    measured_index = int(measured_state_str, 2)
    probabilities[measured_index] = 1.0
    
    return probabilities

def run_quantum_algorithm_over_set(input_set: ndarray, target_set: ndarray, gates: List[str], gate_array: ndarray) -> Tuple[float]:
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
