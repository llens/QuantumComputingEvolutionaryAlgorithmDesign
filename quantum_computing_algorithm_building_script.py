from Config import Config
from EvolutionaryAlgorithm import EvolutionaryAlgorithm
from target_generation import setup_example_problem, ExampleType


if __name__ == "__main__":
    config = Config()
    example = ExampleType.Fourier  # 'flip', 'inverse' problem case to solve
    gates = ["q0", "q1", "q2"]  # , "q3", "q4"] quantum gates to initialize

    input_set, targets = setup_example_problem(
        example,
        gates,
        int(config.get_config_value("EvolutionaryAlgorithm", "INPUT_TEST_CASES"))
    )

    EvolutionaryAlgorithm(config).evolve_algorithm(input_set, targets, gates)
