import array
from deap import creator, base

from Config import Config
from EvolutionaryAlgorithm import EvolutionaryAlgorithm
from target_generation import setup_example_problem, ExampleType

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", array.array, typecode='b', fitness=creator.FitnessMax)

def run_algorithm():
    config = Config()
    example = ExampleType.Fourier
    gates = ["q0", "q1", "q2"]
    input_test_cases=10

    input_set, targets = setup_example_problem(
        example,
        gates,
        input_test_cases
    )

    EvolutionaryAlgorithm(config).evolve_algorithm(input_set, targets, gates)

if __name__ == "__main__":
    run_algorithm()
