from QuantumComputer import QuantumComputer, Programs, State, Gate, QuantumRegister, Probability
import numpy as np


def test_execute_cnot():
    qc = QuantumComputer()
    qc.execute(Programs.program_test_cnot.code)
    assert qc.qubit_states_equal("q0,q1,q2,q3,q4", State.state_from_string("01100"))


def test_reset():
    qc = QuantumComputer()
    qc.apply_gate(Gate.X, "q0")
    assert qc.qubit_states_equal("q0", State.one_state)
    qc.reset()
    assert qc.qubit_states_equal("q0", State.zero_state)


def test_get_ordering():
    qc = QuantumComputer()
    assert qc.get_ordering() == [0, 1, 2, 3, 4]


def test_is_in_canonical_ordering():
    qc = QuantumComputer()
    assert qc.is_in_canonical_ordering()


def test_get_requested_state_order_single_qubit():
    qc = QuantumComputer()
    qc.apply_gate(Gate.X, "q0")
    state = qc.get_requested_state_order("q0")
    # Expected state for all 5 qubits, with q0 as 1 and others as 0
    expected_state = np.kron(State.one_state, np.kron(State.zero_state, np.kron(State.zero_state, np.kron(State.zero_state, State.zero_state))))
    assert np.allclose(state, expected_state)


def test_get_requested_state_order_multiple_qubits():
    qc = QuantumComputer()
    qc.apply_gate(Gate.X, "q0")
    qc.apply_gate(Gate.X, "q1")
    state = qc.get_requested_state_order("q0,q1")
    # Expected state for all 5 qubits, with q0 and q1 as 1 and others as 0
    expected_state = np.kron(State.one_state, np.kron(State.one_state, np.kron(State.zero_state, np.kron(State.zero_state, State.zero_state))))
    assert np.allclose(state, expected_state)


def test_get_requested_state_order_entangled_qubits():
    qc = QuantumComputer()
    qc.execute(Programs.program_test_cnot.code) # This makes q1 and q2 entangled, q0 is X-ed, so 11000
    state = qc.get_requested_state_order("q1,q2")
    # Expected state for q1 and q2 after CNOT, others are 0
    # The actual state of the quantum computer after program_test_cnot is 01100
    expected_state = np.kron(State.zero_state, np.kron(State.one_state, np.kron(State.one_state, np.kron(State.zero_state, State.zero_state))))
    assert np.allclose(state, expected_state)


def test_probabilities_equal():
    qc = QuantumComputer()
    qc.apply_gate(Gate.H, "q0")
    assert qc.probabilities_equal("q0", Probability.get_probabilities(State.plus_state))


def test_bloch_coords_equal():
    qc = QuantumComputer()
    qc.bloch("q0")
    assert qc.bloch_coords_equal("q0", (0, 0, 1))


def test_measure():
    qc = QuantumComputer()
    qc.apply_gate(Gate.X, "q0")
    qc.measure("q0")
    assert qc.qubit_states_equal("q0", State.one_state)


def test_execute_blue_state():
    qc = QuantumComputer()
    qc.execute(Programs.program_blue_state.code)
    blue_state = Gate.H * Gate.S * Gate.T * Gate.H * Gate.T * Gate.H * Gate.S * Gate.T * Gate.H * Gate.T * Gate.H * Gate.T * Gate.H * State.zero_state
    assert qc.bloch_coords_equal("q1", State.get_bloch(blue_state))


def test_execute_xyz_measure():
    qc = QuantumComputer()
    qc.execute(Programs.program_test_XYZMeasureIdSdagTdag.code)
    assert qc.qubit_states_equal("q0", State.zero_state)
    assert qc.qubit_states_equal("q1", State.one_state)
    assert qc.qubit_states_equal("q2", State.one_state)
    assert qc.qubit_states_equal("q3", State.zero_state)
    assert qc.qubit_states_equal("q4", State.one_state)


def test_apply_two_qubit_gate_CNOT_separate_qubits_becomes_entangled():
    qc = QuantumComputer()
    qc.apply_gate(Gate.X, "q0")
    qc.apply_two_qubit_gate_CNOT("q0", "q1")
    assert qc.qubit_states_equal("q0,q1,q2,q3,q4", State.state_from_string("11000"))
    q0 = qc.qubits.get_quantum_register_containing("q0")
    assert q0.is_entangled()


def test_apply_two_qubit_gate_CNOT_already_entangled():
    qc = QuantumComputer()
    qc.execute("h q[0]; cx q[0], q[1];")  # Creates a Bell state, entangling q0 and q1
    q0_reg = qc.qubits.get_quantum_register_containing("q0")
    q1_reg = qc.qubits.get_quantum_register_containing("q1")

    # Now apply another CNOT between already entangled q0 and q1 (control q0, target q1)
    qc.apply_two_qubit_gate_CNOT("q0", "q1")

    # Expect the state to be 1/sqrt(2) * (|00> + |10>) for q0,q1 and |000> for q2,q3,q4
    expected_state_q0q1 = 1/np.sqrt(2) * (np.kron(State.zero_state, State.zero_state) + np.kron(State.one_state, State.zero_state))
    full_expected_state = np.kron(expected_state_q0q1, np.kron(State.zero_state, np.kron(State.zero_state, State.zero_state)))
    assert np.allclose(qc.qubit_states_equal("q0,q1,q2,q3,q4", full_expected_state), True)


def test_entangle_quantum_registers_already_entangled_groups():
    qc = QuantumComputer()
    qc.execute("h q[0]; cx q[0], q[1];")  # q0 and q1 entangled
    qc.execute("h q[2]; cx q[2], q[3];")  # q2 and q3 entangled

    # Now entangle q1 (part of q0-q1 group) and q2 (part of q2-q3 group)
    q1_reg = qc.qubits.get_quantum_register_containing("q1")
    q2_reg = qc.qubits.get_quantum_register_containing("q2")
    qc.qubits.entangle_quantum_registers(q1_reg, q2_reg)

    # All four q0,q1,q2,q3 should now be in one entangled group
    # Check that q0 (which was part of the first group) is now entangled
    q0_reg_after_entangle = qc.qubits.get_quantum_register_containing("q0")
    assert q0_reg_after_entangle.is_entangled()
    # Check that the number of qubits in this entangled group is 4
    assert q0_reg_after_entangle.get_num_qubits() == 4
