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
    for row in gate_array:
        output_string = ''
        for gate_val in row:
            output_string += '     ' + quantum_gate_output_switch(gate_val)
        print(output_string)
