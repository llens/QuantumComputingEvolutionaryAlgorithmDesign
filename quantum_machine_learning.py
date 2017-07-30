from QuantumComputerModified import QuantumComputer, Gate, Probability

# Quantum Gate to Number Map:
# Identity: 0
# T: 1
# Hadamard: 2
# CNOT: 3


def quantum_gate_switch(quantum_computer, gates, array_value, index):
    if array_value == 1:
        quantum_computer.apply_gate(Gate.T, gates[index])
    elif array_value == 2:
        quantum_computer.apply_gate(Gate.T, gates[index])
    elif array_value == 3:
        gate_1, gate_2 = gates
        quantum_computer.qc.apply_two_qubit_gate_CNOT(gate_1, gate_2)

    return quantum_computer


def apply_quantum_gates(quantum_computer, gate_array):
    gates = ("q1", "q2")

    for row in gate_array:
        for index, entry in row:
            quantum_gate_switch(quantum_computer, gates, entry)

            if entry == 3:
                gates(row, index + 1)

    return quantum_computer
