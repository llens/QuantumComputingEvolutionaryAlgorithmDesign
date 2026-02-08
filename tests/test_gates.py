import numpy as np

from quantum_ea.gates import GateType, cnot_two_gate_operation, remove_redundant_gate_series, preprocess_gates


def test_gate_type_values():
    assert GateType.IDENTITY == 0
    assert GateType.T_GATE == 1
    assert GateType.HADAMARD == 2
    assert GateType.CNOT_DOWN == 3
    assert GateType.CNOT_UP == 4


def test_cnot_two_gate_operation_cnot_down():
    gate_array = np.array([[3, 1, 0]])
    result = cnot_two_gate_operation(gate_array)
    expected = np.array([[3, 0, 0]])
    assert np.array_equal(result, expected)


def test_cnot_two_gate_operation_cnot_down_at_edge():
    gate_array = np.array([[1, 3]])
    result = cnot_two_gate_operation(gate_array)
    expected = np.array([[1, 0]])
    assert np.array_equal(result, expected)


def test_cnot_two_gate_operation_cnot_up():
    gate_array = np.array([[0, 4, 0]])
    result = cnot_two_gate_operation(gate_array)
    expected = np.array([[4, 0, 0]])
    assert np.array_equal(result, expected)


def test_cnot_two_gate_operation_cnot_up_at_edge():
    gate_array = np.array([[4, 1]])
    result = cnot_two_gate_operation(gate_array)
    expected = np.array([[0, 1]])
    assert np.array_equal(result, expected)


def test_cnot_two_gate_operation_1d_input():
    gate_array = np.array([3, 0, 1])
    result = cnot_two_gate_operation(gate_array)
    expected = np.array([[3, 0, 1]])
    assert np.array_equal(result, expected)


def test_remove_redundant_gate_series():
    gate_array = np.array([[2, 1], [2, 0]])
    result = remove_redundant_gate_series(gate_array)
    expected = np.array([[0, 1], [0, 0]])
    assert np.array_equal(result, expected)


def test_remove_redundant_gate_series_no_redundancy():
    gate_array = np.array([[2, 1], [1, 0]])
    result = remove_redundant_gate_series(gate_array)
    expected = np.array([[2, 1], [1, 0]])
    assert np.array_equal(result, expected)


def test_preprocess_gates_does_not_mutate():
    original = np.array([[3, 1, 0], [2, 2, 0]])
    original_copy = original.copy()
    preprocess_gates(original)
    assert np.array_equal(original, original_copy)


def test_preprocess_gates_combines_operations():
    gate_array = np.array([[2, 0], [2, 0]])
    result = preprocess_gates(gate_array)
    expected = np.array([[0, 0], [0, 0]])
    assert np.array_equal(result, expected)
