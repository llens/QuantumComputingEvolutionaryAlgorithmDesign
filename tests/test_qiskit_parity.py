"""Cross-validate numpy statevector simulation against Qiskit."""
import numpy as np
import pytest
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

from quantum_ea.circuit import initialise_statevector, apply_quantum_gates, compute_probabilities
from quantum_ea.gates import GateType

NUM_QUBITS = 3


def qiskit_probabilities(qc: QuantumCircuit) -> np.ndarray:
    return Statevector.from_instruction(qc).probabilities()


@pytest.mark.parametrize("qubit", range(NUM_QUBITS))
def test_hadamard_each_qubit(qubit):
    # Numpy path
    sv = initialise_statevector(np.zeros(NUM_QUBITS, dtype=int), NUM_QUBITS)
    gate_row = [GateType.IDENTITY] * NUM_QUBITS
    gate_row[qubit] = GateType.HADAMARD
    gate_array = np.array([gate_row])
    numpy_probs = compute_probabilities(apply_quantum_gates(sv, NUM_QUBITS, gate_array))

    # Qiskit path: uniform superposition then extra H on qubit collapses it
    qc = QuantumCircuit(NUM_QUBITS)
    qc.h(range(NUM_QUBITS))  # matches all-zero -> uniform superposition
    qc.h(qubit)
    qiskit_probs = qiskit_probabilities(qc)

    assert np.allclose(numpy_probs, qiskit_probs, atol=1e-10)


def test_t_gate_on_one_state():
    # Prepare |1> on qubit 0, apply T gate
    input_state = np.array([1, 0, 0])
    sv = initialise_statevector(input_state, NUM_QUBITS)
    gate_array = np.array([[GateType.T_GATE, GateType.IDENTITY, GateType.IDENTITY]])
    numpy_probs = compute_probabilities(apply_quantum_gates(sv, NUM_QUBITS, gate_array))

    # Qiskit path
    qc = QuantumCircuit(NUM_QUBITS)
    qc.x(0)  # flip qubit 0
    qc.t(0)
    qiskit_probs = qiskit_probabilities(qc)

    assert np.allclose(numpy_probs, qiskit_probs, atol=1e-10)


def test_cnot_down():
    # |01> on 2 qubits: qubit 0 is |1>, CNOT_DOWN control=0 target=1
    sv = initialise_statevector(np.array([1, 0]), 2)
    gate_array = np.array([[GateType.CNOT_DOWN, GateType.IDENTITY]])
    numpy_probs = compute_probabilities(apply_quantum_gates(sv, 2, gate_array))

    qc = QuantumCircuit(2)
    qc.x(0)
    qc.cx(0, 1)
    qiskit_probs = qiskit_probabilities(qc)

    assert np.allclose(numpy_probs, qiskit_probs, atol=1e-10)


def test_cnot_up():
    # |10> on 2 qubits: qubit 1 is |1>, CNOT_UP at index 1 means control=0, target=1
    # Wait — CNOT_UP at index i means control=i-1, target=i
    # So we need control qubit (i-1)=0 to be |1>
    sv = initialise_statevector(np.array([1, 0]), 2)
    gate_array = np.array([[GateType.IDENTITY, GateType.CNOT_UP]])
    numpy_probs = compute_probabilities(apply_quantum_gates(sv, 2, gate_array))

    # CNOT_UP at qubit 1: control=qubit0, target=qubit1
    qc = QuantumCircuit(2)
    qc.x(0)
    qc.cx(0, 1)
    qiskit_probs = qiskit_probabilities(qc)

    assert np.allclose(numpy_probs, qiskit_probs, atol=1e-10)


def test_bell_state():
    # H on qubit 0, then CNOT_DOWN from qubit 0 to qubit 1
    # Starting from |00>: H|0> = (|0>+|1>)/sqrt(2), CNOT -> (|00>+|11>)/sqrt(2)
    sv = initialise_statevector(np.array([0, 0]), 2)
    # First need to undo the uniform superposition — start from basis |00>
    # Actually, all-zero input gives uniform superposition, not |00>
    # Use a non-zero input to get |00> — but there's no way with current API.
    # Instead: build manually
    sv = np.array([1, 0, 0, 0], dtype=complex)  # |00>
    gate_array = np.array([
        [GateType.HADAMARD, GateType.IDENTITY],
        [GateType.CNOT_DOWN, GateType.IDENTITY],
    ])
    numpy_probs = compute_probabilities(apply_quantum_gates(sv, 2, gate_array))

    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qiskit_probs = qiskit_probabilities(qc)

    assert np.allclose(numpy_probs, qiskit_probs, atol=1e-10)
    # Bell state: 50% |00>, 50% |11>
    assert np.allclose(numpy_probs, [0.5, 0.0, 0.0, 0.5], atol=1e-10)
