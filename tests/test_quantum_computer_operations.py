import numpy as np

from quantum_computer_operations import remove_redundant_gate_series, cnot_two_gate_operation, count_blank_rows, \
    initialise_quantum_computer, quantum_gate_switch, apply_quantum_gates, run_quantum_algorithm, \
    run_quantum_algorithm_over_set
from QuantumComputer import State, QuantumComputer, Gate, Probability


def test_remove_redundant_gate_series():
    gate_array = np.array([[2, 0, 0], [2, 0, 0], [0, 3, 0], [0, 3, 0]])
    expected_array = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]])
    assert np.array_equal(remove_redundant_gate_series(gate_array), expected_array)


def test_cnot_two_gate_operation():
    gate_array = np.array([[3, 0, 0], [0, 4, 0], [0, 0, 3]])
    expected_array = np.array([[3, 0, 0], [4, 0, 0], [0, 0, 0]])
    assert np.array_equal(cnot_two_gate_operation(gate_array), expected_array)

def test_cnot_two_gate_operation_else_case():
    gate_array = np.array([[1, 2, 0]])
    expected_array = np.array([[1, 2, 0]])
    assert np.array_equal(cnot_two_gate_operation(gate_array), expected_array)


def test_count_blank_rows():
    gate_array = np.array([[0, 0, 0], [1, 2, 3], [0, 0, 0]])
    assert count_blank_rows(gate_array) == 2


def test_initialise_quantum_computer():
    input_state = np.array([0, 1, 0, 1, 0, 1, 0, 1, 0, 1])
    gates = ["q0", "q1", "q2", "q3", "q4"]
    qc = initialise_quantum_computer(input_state, gates)
    assert qc.qubit_states_equal("q0,q1,q2,q3,q4", State.state_from_string("11111"))


def test_quantum_gate_switch_t_gate():
    qc = QuantumComputer()
    gates = ["q0"]
    qc = quantum_gate_switch(qc, gates, 1, 0)
    assert qc.qubit_states_equal("q0", Gate.T @ State.zero_state)
def test_quantum_gate_switch_h_gate():
    qc = QuantumComputer()
    gates = ["q0"]
    qc = quantum_gate_switch(qc, gates, 2, 0)
    assert qc.qubit_states_equal("q0", Gate.H @ State.zero_state)
def test_quantum_gate_switch_cnot_gate():
    qc = QuantumComputer()
    qc.apply_gate(Gate.X, "q0")
    gates = ["q0", "q1"]
    qc = quantum_gate_switch(qc, gates, 3, 0)
    assert qc.qubit_states_equal("q0,q1,q2,q3,q4", State.state_from_string("11000"))


def test_apply_quantum_gates():
    qc = QuantumComputer()
    gates = ["q0", "q1"]
    gate_array = np.array([[2, 0], [1, 0]])
    qc = apply_quantum_gates(qc, gates, gate_array)
    expected_state = Gate.T @ Gate.H @ State.zero_state
    assert qc.qubit_states_equal("q0", expected_state)


def test_run_quantum_algorithm():
    input_state = np.array([0, 0, 0, 0])
    gates = ["q0", "q1"]
    gate_array = np.array([[2, 0], [3, 0]])
    probabilities = run_quantum_algorithm(input_state, gates, gate_array)
    expected_probabilities = Probability.get_probabilities(State.bell_state)
    assert np.allclose(probabilities, expected_probabilities)

def test_run_quantum_algorithm_over_set():
    input_set = np.array([[0, 0, 0, 0], [0, 0, 0, 0]])
    target_set = np.array([[0.5, 0, 0, 0.5], [0.5, 0, 0, 0.5]])
    gates = ["q0", "q1"]
    gate_array = np.array([[2, 0], [3, 0]])
    score, = run_quantum_algorithm_over_set(input_set, target_set, gates, gate_array)
    assert score == -1.0
