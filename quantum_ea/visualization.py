from numpy import ndarray

from quantum_ea.gates import GateType


def quantum_gate_output_switch(array_value: complex) -> str:
    match array_value:
        case GateType.IDENTITY:
            return '|'
        case GateType.T_GATE:
            return 'T'
        case GateType.HADAMARD:
            return 'H'
        case GateType.CNOT_DOWN:
            return '. - (+)'
        case GateType.CNOT_UP:
            return '(+) - .'
    return ''


def output_quantum_gates(gate_array: ndarray) -> None:
    for k in range(len(gate_array)):
        output_string = ''
        i = 0

        while i < len(gate_array[k]):
            if gate_array[k][i] < GateType.CNOT_DOWN:
                output_string += '     ' + quantum_gate_output_switch(gate_array[k][i])
                i += 1
            else:
                output_string += '     ' + quantum_gate_output_switch(gate_array[k][i])
                i += 2

        print(output_string)
