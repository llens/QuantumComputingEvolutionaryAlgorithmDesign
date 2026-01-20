import numpy as np
import pytest

from target_generation import flip_targets, one_over_targets, fourier_targets, setup_example_problem, ExampleType


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
    monkeypatch.setattr('target_generation.discrete_inputs', lambda gates, input_size: np.array([[0, 1, 1, 0]]))
    input_set, target_set = setup_example_problem(ExampleType.Flip, ["q0", "q1"], 1)
    expected_input_set = np.array([[0, 1, 1, 0]])
    expected_target_set = np.array([[0.5, 0, 0, 0.5]])
    assert np.array_equal(input_set, expected_input_set)
    assert np.allclose(target_set, expected_target_set)