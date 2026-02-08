import numpy as np
from qiskit.quantum_info import Statevector

from quantum_ea.circuit import initialise_quantum_circuit, apply_quantum_gates, measure_quantum_output


def test_initialise_quantum_circuit_zero_state():
    input_state = np.array([0, 0])
    qc = initialise_quantum_circuit(input_state, num_qubits=2)
    # All-zero input should create uniform superposition (Hadamard on all qubits)
    sv = Statevector.from_instruction(qc)
    probs = sv.probabilities()
    assert np.allclose(probs, [0.25, 0.25, 0.25, 0.25])


def test_initialise_quantum_circuit_basis_state():
    input_state = np.array([0, 1, 0, 0])
    qc = initialise_quantum_circuit(input_state, num_qubits=2)
    sv = Statevector.from_instruction(qc)
    expected_sv = Statevector.from_label('10')
    assert sv.equiv(expected_sv)


def test_apply_quantum_gates_identity():
    # input [1, 0] flips qubit 0 -> Qiskit state |01> (little-endian label '01')
    qc = initialise_quantum_circuit(np.array([1, 0]), num_qubits=2)
    gate_array = np.array([[0, 0]])
    qc = apply_quantum_gates(qc, gate_array)
    sv = Statevector.from_instruction(qc)
    expected_sv = Statevector.from_label('01')
    assert sv.equiv(expected_sv)


def test_apply_quantum_gates_no_double_processing():
    """Regression test: apply_quantum_gates should NOT preprocess gates.
    Preprocessing is now done once in dna_to_gates, not in the circuit layer."""
    qc = initialise_quantum_circuit(np.array([1, 0]), num_qubits=2)
    # Pass already-preprocessed gate array with a Hadamard
    gate_array = np.array([[2, 0]])
    qc = apply_quantum_gates(qc, gate_array)
    # The Hadamard should have been applied exactly once
    sv = Statevector.from_instruction(qc)
    probs = sv.probabilities()
    # q0 was |1>, after H it should be in superposition: |0>-|1> / sqrt(2)
    assert np.allclose(probs, [0.5, 0.5, 0.0, 0.0]) or np.allclose(probs, [0.0, 0.0, 0.5, 0.5])


def test_measure_quantum_output():
    input_state = np.array([1, 0])
    qc = initialise_quantum_circuit(input_state, num_qubits=2)
    gate_array = np.array([[0, 0]])
    qc = apply_quantum_gates(qc, gate_array)
    probs = measure_quantum_output(qc)
    # |10> state, qubit 0 is |1>, qubit 1 is |0>
    assert probs.shape == (4,)
    assert np.isclose(sum(probs), 1.0)
