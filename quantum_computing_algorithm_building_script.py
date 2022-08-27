from evolutionary_algorithm import evolve_algorithm
from target_generation import one_over_targets, flip_targets, continuous_inputs, discrete_inputs, fourier_targets, \
    setup_example_problem
import numpy as np


def underlined_output(string):
    print(string)
    print("----------------------")


if __name__ == "__main__":
    example = 'fourier'  # 'flip', 'inverse' problem case to solve
    gates = ["q0", "q1", "q2"]  # , "q3", "q4"] quantum gates to initialize
    input_size = 10  # number of random inputs to use when testing

    input_set, targets = setup_example_problem(example, gates, input_size)

    evolve_algorithm(input_set, targets, gates)
