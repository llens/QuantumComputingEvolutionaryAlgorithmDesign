import numpy as np
from numpy import ndarray

from quantum_ea.gates import GateType

# Pre-computed 2x2 gate matrices
_H2 = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
_T2 = np.array([[1, 0], [0, np.exp(1j * np.pi / 4)]], dtype=complex)
_I2 = np.eye(2, dtype=complex)

# Cache: (gate_type, qubit_index, num_qubits) -> full 2^n x 2^n matrix
_gate_matrix_cache: dict[tuple, ndarray] = {}


def _full_single_qubit_gate(gate_2x2: ndarray, qubit_index: int, num_qubits: int) -> ndarray:
    """Build 2^n x 2^n matrix for a single-qubit gate via Kronecker products.

    Uses LSB=qubit-0 convention (matching Qiskit): the gate sits at position
    (num_qubits - 1 - qubit_index) in the tensor product.
    """
    factors = [_I2] * num_qubits
    factors[num_qubits - 1 - qubit_index] = gate_2x2
    result = factors[0]
    for f in factors[1:]:
        result = np.kron(result, f)
    return result


def _cnot_matrix(control: int, target: int, num_qubits: int) -> ndarray:
    """Build 2^n x 2^n CNOT permutation matrix."""
    dim = 2 ** num_qubits
    mat = np.zeros((dim, dim), dtype=complex)
    for i in range(dim):
        if i & (1 << control):
            j = i ^ (1 << target)
        else:
            j = i
        mat[j, i] = 1.0
    return mat


def _get_gate_matrix(gate_type: int, qubit_index: int, num_qubits: int) -> ndarray | None:
    """Return the cached full gate matrix, or None for identity/skip."""
    if gate_type == GateType.IDENTITY:
        return None

    key = (gate_type, qubit_index, num_qubits)
    if key in _gate_matrix_cache:
        return _gate_matrix_cache[key]

    if gate_type == GateType.HADAMARD:
        mat = _full_single_qubit_gate(_H2, qubit_index, num_qubits)
    elif gate_type == GateType.T_GATE:
        mat = _full_single_qubit_gate(_T2, qubit_index, num_qubits)
    elif gate_type == GateType.CNOT_DOWN:
        if qubit_index + 1 < num_qubits:
            mat = _cnot_matrix(qubit_index, qubit_index + 1, num_qubits)
        else:
            return None
    elif gate_type == GateType.CNOT_UP:
        if qubit_index > 0:
            mat = _cnot_matrix(qubit_index - 1, qubit_index, num_qubits)
        else:
            return None
    else:
        return None

    _gate_matrix_cache[key] = mat
    return mat


def initialise_statevector(input_state: ndarray, num_qubits: int) -> ndarray:
    """Return a complex statevector of shape (2**num_qubits,).

    All-zero input -> uniform superposition (1/sqrt(dim)).
    Otherwise set the computational basis state by flipping indicated qubits.
    """
    dim = 2 ** num_qubits
    if np.all(input_state == 0):
        return np.full(dim, 1.0 / np.sqrt(dim), dtype=complex)

    index = 0
    for i, val in enumerate(input_state):
        if val == 1 and i < num_qubits:
            index |= (1 << i)
    sv = np.zeros(dim, dtype=complex)
    sv[index] = 1.0
    return sv


def apply_quantum_gates(statevector: ndarray, num_qubits: int, gate_array: ndarray) -> ndarray:
    """Apply gate_array rows/cols to statevector via matrix multiplication."""
    sv = statevector.copy()
    for row in gate_array:
        for qubit_index, gate_val in enumerate(row):
            mat = _get_gate_matrix(int(gate_val), qubit_index, num_qubits)
            if mat is not None:
                sv = mat @ sv
    return sv


def compute_probabilities(statevector: ndarray) -> ndarray:
    """Return measurement probabilities from a statevector."""
    return np.abs(statevector) ** 2
