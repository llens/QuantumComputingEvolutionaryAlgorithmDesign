from evolutionary_algorithm import evolve_algorithm
from target_generation import one_over_targets, flip_targets, continuous_inputs, discrete_inputs, fourier_targets
import numpy as np


def underlined_output(string):
    print(string)
    print("----------------------")


if __name__ == "__main__":
    example = 'fourier'
    gates = ["q0", "q1", "q2", "q3", "q4"]
    input_size = 10

    # Sum of probabilities exceeds ones as not yet entangled.
    input_set = []
    if example == 'flip':
        input_set = discrete_inputs(gates, input_size)
    elif example == 'inverse':
        input_set = continuous_inputs(gates, input_size)
    elif example == 'fourier':
        input_set = continuous_inputs(gates, input_size)

    targets = np.zeros(input_set.shape) + np.zeros(input_set.shape) * 1j

    for i in range(len(input_set)):
        if example == 'flip':
            targets[i, :] = flip_targets(input_set[i, :])
        elif example == 'inverse':
            targets[i, :] = one_over_targets(input_set[i, :])
        elif example == 'fourier':
            targets[i, :] = fourier_targets(input_set[i, :])

        temp_sum = sum(targets[i, :])
        if temp_sum != 0:
            targets[i, :] /= temp_sum

    evolve_algorithm(input_set, targets, gates)
