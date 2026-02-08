from quantum_ea import EAConfig, EvolutionaryAlgorithm, ExampleType, setup_example_problem


def run_algorithm():
    config = EAConfig()
    example = ExampleType.Fourier
    num_qubits = 3
    input_test_cases = 10

    input_set, targets = setup_example_problem(
        example,
        num_qubits,
        input_test_cases
    )

    EvolutionaryAlgorithm(config).evolve_algorithm(input_set, targets, num_qubits)

if __name__ == "__main__":
    run_algorithm()
