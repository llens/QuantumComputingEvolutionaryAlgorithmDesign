import numpy as np
import random


def flip_targets(input_arr):
    return np.mod(input_arr + np.ones(input_arr.shape), 2)


def one_over_targets(input_arr):
    return np.divide(np.ones(input_arr.shape), input_arr)


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
    inputs = np.random.uniform(0, 2, 2 ** len(gates))
    inputs /= sum(inputs)
    return inputs
