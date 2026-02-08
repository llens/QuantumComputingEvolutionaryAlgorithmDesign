import numpy as np

from quantum_ea.target_generation import (
    flip_targets, one_over_targets, fourier_targets, setup_example_problem,
    ExampleType, discrete_input, continuous_input, discrete_inputs, continuous_inputs
)


def test_flip_targets():
    input_arr = np.array([0, 1, 1, 0])
    expected_arr = np.array([1, 0, 0, 1])
    assert np.array_equal(flip_targets(input_arr), expected_arr)


def test_one_over_targets():
    input_arr = np.array([1, 2, 4, 8])
    expected_arr = np.array([1, 0.5, 0.25, 0.125])
    assert np.allclose(one_over_targets(input_arr), expected_arr)


def test_fourier_targets():
    input_arr = np.array([1, 0, 0, 0])
    expected_arr = np.array([1, 1, 1, 1])
    assert np.allclose(fourier_targets(input_arr), expected_arr)


def test_setup_example_problem_flip(monkeypatch):
    monkeypatch.setattr('quantum_ea.target_generation.discrete_inputs', lambda num_qubits, input_size: np.array([[0, 1, 1, 0]]))
    input_set, target_set = setup_example_problem(ExampleType.Flip, num_qubits=2, input_size=1)
    expected_input_set = np.array([[0, 1, 1, 0]])
    expected_target_set = np.array([[0.5, 0, 0, 0.5]])
    assert np.array_equal(input_set, expected_input_set)
    assert np.allclose(target_set, expected_target_set)


def test_discrete_input():
    inputs = discrete_input(num_qubits=2)
    assert inputs.shape == (4,)
    assert np.all(np.isin(inputs, [0, 1]))


def test_continuous_input():
    inputs = continuous_input(num_qubits=2)
    assert inputs.shape == (4,)
    assert np.isclose(sum(inputs), 1)


def test_discrete_inputs():
    inputs = discrete_inputs(num_qubits=2, n_inputs=2)
    assert inputs.shape == (2, 4)


def test_continuous_inputs():
    inputs = continuous_inputs(num_qubits=2, n_inputs=2)
    assert inputs.shape == (2, 4)


def test_setup_example_problem_inverse(monkeypatch):
    monkeypatch.setattr('quantum_ea.target_generation.continuous_inputs', lambda num_qubits, input_size: np.array([[1, 2, 4, 8]]))
    input_set, target_set = setup_example_problem(ExampleType.Inverse, num_qubits=2, input_size=1)
    expected_input_set = np.array([[1, 2, 4, 8]])
    expected_target_set = np.array([1, 0.5, 0.25, 0.125])
    expected_target_set /= np.sum(expected_target_set)
    assert np.array_equal(input_set, expected_input_set)
    assert np.allclose(target_set, expected_target_set)


def test_setup_example_problem_fourier(monkeypatch):
    monkeypatch.setattr('quantum_ea.target_generation.continuous_inputs', lambda num_qubits, input_size: np.array([[1, 0, 0, 0]]))
    input_set, target_set = setup_example_problem(ExampleType.Fourier, num_qubits=2, input_size=1)
    expected_input_set = np.array([[1, 0, 0, 0]])
    expected_target_set = np.array([1., 1., 1., 1.])
    expected_target_set /= np.sum(expected_target_set)
    assert np.array_equal(input_set, expected_input_set)
    assert np.allclose(target_set, expected_target_set)
