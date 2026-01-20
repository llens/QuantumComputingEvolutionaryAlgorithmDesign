import numpy as np

from QuantumComputer import Gate, State


def test_gate_h():
    h_gate = 1 / np.sqrt(2) * np.array([[1, 1], [1, -1]])
    assert np.allclose(Gate.H, h_gate)


def test_state_zero():
    zero_state = np.array([[1], [0]])
    assert np.allclose(State.zero_state, zero_state)


def test_state_bell():
    bell_state = 1 / np.sqrt(2) * np.array([[1], [0], [0], [1]])
    assert np.allclose(State.bell_state, bell_state)


def test_change_to_x_basis():
    x_basis_state = State.change_to_x_basis(State.zero_state)
    assert np.allclose(x_basis_state, State.plus_state)


def test_change_to_y_basis():
    y_basis_state = State.change_to_y_basis(State.zero_state)
    assert np.allclose(y_basis_state, State.plus_state)


def test_is_fully_separable():
    assert State.is_fully_separable(State.zero_state)
    assert not State.is_fully_separable(State.bell_state)


def test_get_first_qubit():
    state = np.kron(State.one_state, State.zero_state)
    first_qubit = State.get_first_qubit(state)
    assert np.allclose(first_qubit, State.one_state)