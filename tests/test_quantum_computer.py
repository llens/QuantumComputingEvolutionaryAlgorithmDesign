from QuantumComputer import QuantumComputer, Programs, State, Gate


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
