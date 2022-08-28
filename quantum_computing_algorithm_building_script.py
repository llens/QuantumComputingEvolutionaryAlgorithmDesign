from evolutionary_algorithm import evolve_algorithm
from target_generation import setup_example_problem, ExampleType


if __name__ == "__main__":
    example = ExampleType.Fourier  # 'flip', 'inverse' problem case to solve
    gates = ["q0", "q1", "q2"]  # , "q3", "q4"] quantum gates to initialize
    input_size = 10  # number of random inputs to use when testing

    input_set, targets = setup_example_problem(example, gates, input_size)

    evolve_algorithm(input_set, targets, gates)
