import numpy as np
from numpy import ndarray
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

from quantum_ea.gates import GateType


def initialise_quantum_circuit(input_state: ndarray, num_qubits: int) -> QuantumCircuit:
    qc = QuantumCircuit(num_qubits, num_qubits)

    if np.all(input_state == 0):
        qc.h(range(num_qubits))
    else:
        for i, state_val in enumerate(input_state):
            if state_val == 1 and i < num_qubits:
                qc.x(i)

    return qc


def quantum_gate_switch(qc: QuantumCircuit, array_value: complex, index: int):
    num_qubits = qc.num_qubits
    match array_value:
        case GateType.T_GATE:
            qc.t(index)
        case GateType.HADAMARD:
            qc.h(index)
        case GateType.CNOT_DOWN:
            if index + 1 < num_qubits:
                qc.cx(index, index + 1)
        case GateType.CNOT_UP:
            if index > 0:
                qc.cx(index - 1, index)


def apply_quantum_gates(qc: QuantumCircuit, gate_array: ndarray) -> QuantumCircuit:
    for k in range(len(gate_array)):
        for i in range(len(gate_array[k])):
            quantum_gate_switch(qc, gate_array[k][i], i)

    return qc


def measure_quantum_output(qc: QuantumCircuit) -> ndarray:
    num_qubits = qc.num_qubits

    qc.measure(range(num_qubits), range(num_qubits))

    simulator = AerSimulator()

    shots = 1024
    result = simulator.run(qc, shots=shots).result()
    counts = result.get_counts(qc)

    probabilities = np.zeros(2**num_qubits)
    for state, count in counts.items():
        measured_index = int(state, 2)
        probabilities[measured_index] = count / shots

    return probabilities
