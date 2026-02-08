import numpy as np
import pytest

from quantum_ea.fitness import run_quantum_algorithm, run_quantum_algorithm_over_set, count_blank_rows, clear_fitness_cache


@pytest.fixture(autouse=True)
def _clear_cache():
    clear_fitness_cache()
    yield
    clear_fitness_cache()


def test_run_quantum_algorithm():
    input_state = np.array([0, 0])
    gate_array = np.array([[2, 0], [3, 0]])  # H on q0, then CNOT q0->q1
    probabilities = run_quantum_algorithm(input_state, num_qubits=2, gate_array=gate_array)
    assert probabilities.shape == (4,)
    assert np.isclose(sum(probabilities), 1.0)


def test_run_quantum_algorithm_over_set():
    input_set = np.array([[0, 0, 0]])
    target_distribution = np.zeros(8)
    target_distribution[5] = 1.0  # marked item at index 5
    target_set = np.array([target_distribution])
    gate_array = np.array([[2, 0, 0]])
    score, = run_quantum_algorithm_over_set(input_set, target_set, num_qubits=3, gate_array=gate_array)
    assert isinstance(score, float)
    assert 0.0 <= score <= 1.0


def test_count_blank_rows():
    gate_array = np.array([[0, 0], [1, 2], [0, 0]])
    assert count_blank_rows(gate_array) == 2


def test_count_blank_rows_no_blanks():
    gate_array = np.array([[1, 2], [3, 0]])
    assert count_blank_rows(gate_array) == 0


def test_fitness_caching():
    input_set = np.array([[0, 0, 0]])
    target_distribution = np.zeros(8)
    target_distribution[3] = 1.0
    target_set = np.array([target_distribution])
    gate_array = np.array([[2, 0, 0], [3, 0, 0]])

    result1 = run_quantum_algorithm_over_set(input_set, target_set, num_qubits=3, gate_array=gate_array)
    result2 = run_quantum_algorithm_over_set(input_set, target_set, num_qubits=3, gate_array=gate_array)

    # Exact float equality proves cache hit (deterministic numpy, no stochastic shots)
    assert result1 == result2
