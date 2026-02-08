import numpy as np

from quantum_ea.circuit import initialise_statevector, apply_quantum_gates, compute_probabilities
from quantum_ea.gates import GateType


def test_initialise_statevector_zero_state():
    sv = initialise_statevector(np.array([0, 0]), num_qubits=2)
    probs = compute_probabilities(sv)
    assert np.allclose(probs, [0.25, 0.25, 0.25, 0.25])


def test_initialise_statevector_basis_state():
    # input [0, 1] flips qubit 1 -> basis state index 2 (binary 10)
    sv = initialise_statevector(np.array([0, 1]), num_qubits=2)
    assert np.isclose(sv[2], 1.0)
    assert np.isclose(np.sum(np.abs(sv) ** 2), 1.0)


def test_apply_quantum_gates_identity():
    sv = initialise_statevector(np.array([1, 0]), num_qubits=2)
    gate_array = np.array([[GateType.IDENTITY, GateType.IDENTITY]])
    sv_out = apply_quantum_gates(sv, num_qubits=2, gate_array=gate_array)
    assert np.allclose(sv, sv_out)


def test_apply_quantum_gates_hadamard():
    # |01> (qubit 0 flipped), apply H on qubit 0
    sv = initialise_statevector(np.array([1, 0]), num_qubits=2)
    gate_array = np.array([[GateType.HADAMARD, GateType.IDENTITY]])
    sv_out = apply_quantum_gates(sv, num_qubits=2, gate_array=gate_array)
    probs = compute_probabilities(sv_out)
    # H on |1> -> (|0>-|1>)/sqrt(2), so equal prob on indices 0 and 1
    assert np.allclose(probs, [0.5, 0.5, 0.0, 0.0])


def test_apply_quantum_gates_cnot():
    # |01> means qubit 0 is |1>, qubit 1 is |0>
    # CNOT_DOWN with control=qubit0, target=qubit1
    # control is 1, so target flips: |01> -> |11> (index 3)
    sv = initialise_statevector(np.array([1, 0]), num_qubits=2)
    gate_array = np.array([[GateType.CNOT_DOWN, GateType.IDENTITY]])
    sv_out = apply_quantum_gates(sv, num_qubits=2, gate_array=gate_array)
    probs = compute_probabilities(sv_out)
    expected = np.array([0.0, 0.0, 0.0, 1.0])
    assert np.allclose(probs, expected)


def test_probabilities_sum_to_one():
    sv = initialise_statevector(np.array([0, 0, 0]), num_qubits=3)
    gate_array = np.array([[GateType.HADAMARD, GateType.T_GATE, GateType.IDENTITY]])
    sv_out = apply_quantum_gates(sv, num_qubits=3, gate_array=gate_array)
    probs = compute_probabilities(sv_out)
    assert np.isclose(np.sum(probs), 1.0)
