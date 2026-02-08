from typing import Tuple

import numpy as np
from numpy import ndarray

from quantum_ea.circuit import initialise_quantum_circuit, apply_quantum_gates, measure_quantum_output


def run_quantum_algorithm(input_state: ndarray, num_qubits: int, gate_array: ndarray) -> ndarray:
    qc = initialise_quantum_circuit(input_state, num_qubits)
    qc = apply_quantum_gates(qc, gate_array)
    return measure_quantum_output(qc)


def run_quantum_algorithm_over_set(input_set: ndarray, target_set: ndarray, num_qubits: int, gate_array: ndarray) -> Tuple[float]:
    probabilities_output = run_quantum_algorithm(input_set[0, :], num_qubits, gate_array)

    marked_item_index = np.argmax(target_set[0])

    fitness_score = probabilities_output[marked_item_index]

    if fitness_score > 0.99:
        num_blank_rows = count_blank_rows(gate_array)
        if num_blank_rows > 0:
            fitness_score /= (1.0 + num_blank_rows * 0.1)

    if np.isnan(fitness_score):
        fitness_score = 0.0

    return float(fitness_score),


def count_blank_rows(gate_array: ndarray) -> int:
    blank_counter = 0
    for row in gate_array:
        if sum(row) == 0:
            blank_counter += 1

    return blank_counter
