import random
from enum import Enum
from typing import List

import numpy as np
from numpy import ndarray


class ExampleType(Enum):
    Flip = "flip"
    Inverse = "inverse"
    Fourier = "fourier"


def setup_example_problem(example: ExampleType, num_qubits: int, input_size: int) -> tuple[ndarray, ndarray]:
    input_set = np.empty([])
    match example:
        case ExampleType.Flip:
            input_set = discrete_inputs(num_qubits, input_size)
        case ExampleType.Inverse:
            input_set = continuous_inputs(num_qubits, input_size)
        case ExampleType.Fourier:
            input_set = continuous_inputs(num_qubits, input_size)
        case _:
            ValueError("No mapping found for given example type.")

    targets = np.zeros(input_set.shape) + np.zeros(input_set.shape) * 1j

    for i in range(len(input_set)):
        match example:
            case ExampleType.Flip:
                targets[i, :] = flip_targets(input_set[i, :])
            case ExampleType.Inverse:
                targets[i, :] = one_over_targets(input_set[i, :])
            case ExampleType.Fourier:
                targets[i, :] = fourier_targets(input_set[i, :])

        temp_sum = sum(targets[i, :])
        if temp_sum != 0:
            targets[i, :] /= temp_sum

    return input_set, targets


def flip_targets(input_arr: ndarray) -> ndarray:
    return np.mod(input_arr + np.ones(input_arr.shape), 2)


def one_over_targets(input_arr: ndarray) -> ndarray:
    return np.divide(np.ones(input_arr.shape), input_arr)


def fourier_targets(input_arr: ndarray) -> ndarray:
    return np.fft.fft(input_arr)


def continuous_inputs(num_qubits: int, n_inputs: int) -> ndarray:
    i = 1
    input_arr = continuous_input(num_qubits)
    while i < n_inputs:
        input_arr = np.vstack((input_arr, continuous_input(num_qubits)))
        i += 1

    return input_arr


def discrete_inputs(num_qubits: int, n_inputs: int) -> ndarray:
    i = 1
    input_arr = discrete_input(num_qubits)
    while i < n_inputs:
        input_arr = np.vstack((input_arr, discrete_input(num_qubits)))
        i += 1

    return input_arr


def discrete_input(num_qubits: int) -> ndarray:
    i = 0
    inputs = []
    while i < (2 ** num_qubits / 2):
        inputs.extend(discrete_qbit())
        i += 1

    return np.array(inputs)


def discrete_qbit() -> List[int]:
    temp = random.getrandbits(1)

    return [temp, 1 - temp]


def continuous_input(num_qubits: int) -> ndarray:
    inputs: ndarray = np.random.uniform(0, 2, 2 ** num_qubits) + np.random.uniform(0, 2, 2 ** num_qubits) * 1j
    inputs /= sum(inputs)
    return inputs
