from enum import IntEnum

import numpy as np
from numpy import ndarray


class GateType(IntEnum):
    IDENTITY = 0
    T_GATE = 1
    HADAMARD = 2
    CNOT_DOWN = 3
    CNOT_UP = 4


def cnot_two_gate_operation(gate_array: ndarray) -> ndarray:
    if gate_array.ndim == 1:
        gate_array = np.reshape(gate_array, (1, len(gate_array)))

    row_length = gate_array.shape[1]
    for k in range(len(gate_array)):
        for i in range(row_length):
            if gate_array[k][i] == GateType.CNOT_DOWN:
                if i < row_length - 1:
                    gate_array[k][i + 1] = GateType.IDENTITY
                else:
                    gate_array[k][i] = GateType.IDENTITY

            if gate_array[k][i] == GateType.CNOT_UP:
                if i > 0:
                    gate_array[k][i - 1] = GateType.CNOT_UP
                    gate_array[k][i] = GateType.IDENTITY
                else:
                    gate_array[k][i] = GateType.IDENTITY
    return gate_array


def remove_redundant_gate_series(gate_array: ndarray) -> ndarray:
    col_length = len(gate_array)
    for k in range(col_length):
        for i in range(len(gate_array[1])):
            remove_redundant_gate(gate_array, k, i, col_length)

    return gate_array


def remove_redundant_gate(gate_array: ndarray, idx_1: int, idx_2: int, column_length: int):
    if (gate_array[idx_1][idx_2] >= GateType.HADAMARD
            and idx_1 > 0
            and gate_array[idx_1][idx_2] == gate_array[idx_1 - 1][idx_2]):
        gate_array[idx_1][idx_2] = GateType.IDENTITY
        gate_array[idx_1 - 1][idx_2] = GateType.IDENTITY

    if (gate_array[idx_1][idx_2] >= GateType.HADAMARD
            and idx_1 < (column_length - 1)
            and gate_array[idx_1][idx_2] == gate_array[idx_1 + 1][idx_2]):
        gate_array[idx_1][idx_2] = GateType.IDENTITY
        gate_array[idx_1 + 1][idx_2] = GateType.IDENTITY


def preprocess_gates(gate_array: ndarray) -> ndarray:
    processed = gate_array.copy()
    return remove_redundant_gate_series(cnot_two_gate_operation(processed))
