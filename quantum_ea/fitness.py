from typing import Tuple

import numpy as np
from numpy import ndarray

from quantum_ea.circuit import initialise_statevector, apply_quantum_gates, compute_probabilities

_fitness_cache: dict[bytes, Tuple[float]] = {}


def clear_fitness_cache() -> None:
    _fitness_cache.clear()


def run_quantum_algorithm(input_state: ndarray, num_qubits: int, gate_array: ndarray) -> ndarray:
    sv = initialise_statevector(input_state, num_qubits)
    sv = apply_quantum_gates(sv, num_qubits, gate_array)
    return compute_probabilities(sv)


def run_quantum_algorithm_over_set(input_set: ndarray, target_set: ndarray, num_qubits: int, gate_array: ndarray) -> Tuple[float]:
    cache_key = input_set.tobytes() + target_set.tobytes() + gate_array.tobytes()
    if cache_key in _fitness_cache:
        return _fitness_cache[cache_key]

    probabilities_output = run_quantum_algorithm(input_set[0, :], num_qubits, gate_array)

    marked_item_index = np.argmax(target_set[0])

    fitness_score = probabilities_output[marked_item_index]

    if fitness_score > 0.99:
        num_blank_rows = count_blank_rows(gate_array)
        if num_blank_rows > 0:
            fitness_score /= (1.0 + num_blank_rows * 0.1)

    if np.isnan(fitness_score):
        fitness_score = 0.0

    result = float(fitness_score),
    _fitness_cache[cache_key] = result
    return result


def count_blank_rows(gate_array: ndarray) -> int:
    blank_counter = 0
    for row in gate_array:
        if sum(row) == 0:
            blank_counter += 1

    return blank_counter
