import numpy as np
import random


def setup_example_problem(example, gates, input_size):
    # Sum of probabilities exceeds ones as not yet entangled.
    input_set = []
    match example:
        case 'flip':
            input_set = discrete_inputs(gates, input_size)
        case 'inverse':
            input_set = continuous_inputs(gates, input_size)
        case 'fourier':
            input_set = continuous_inputs(gates, input_size)

    targets = np.zeros(input_set.shape) + np.zeros(input_set.shape) * 1j

    for i in range(len(input_set)):
        match example:
            case 'flip':
                targets[i, :] = flip_targets(input_set[i, :])
            case 'inverse':
                targets[i, :] = one_over_targets(input_set[i, :])
            case 'fourier':
                targets[i, :] = fourier_targets(input_set[i, :])

        temp_sum = sum(targets[i, :])
        if temp_sum != 0:
            targets[i, :] /= temp_sum

    return input_set, targets

def flip_targets(input_arr):
    return np.mod(input_arr + np.ones(input_arr.shape), 2)


def one_over_targets(input_arr):
    return np.divide(np.ones(input_arr.shape), input_arr)


def fourier_targets(input_arr):
    return np.fft.fft(input_arr)


def continuous_inputs(gates, n_inputs):
    i = 1
    input_arr = continuous_input(gates)
    while i < n_inputs:
        input_arr = np.vstack((input_arr, continuous_input(gates)))
        i += 1

    return input_arr


def discrete_inputs(gates, n_inputs):
    i = 1
    input_arr = discrete_input(gates)
    while i < n_inputs:
        input_arr = np.vstack((input_arr, discrete_input(gates)))
        i += 1

    return input_arr


def discrete_input(gates):
    i = 0
    inputs = []
    while i < (2 ** len(gates) / 2):
        inputs = np.hstack((inputs, discrete_qbit()))
        i += 1

    return inputs


def discrete_qbit():
    temp = random.getrandbits(1)

    return [temp, 1 - temp]


def continuous_input(gates):
    inputs = np.random.uniform(0, 2, 2 ** len(gates)) + np.random.uniform(0, 2, 2 ** len(gates)) * 1j
    inputs /= sum(inputs)
    return inputs
