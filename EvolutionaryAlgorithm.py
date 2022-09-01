import random
from typing import List

import array
import multiprocessing
import numpy as np
from deap import algorithms, tools, base, creator
from numpy import ndarray

import Config
from quantum_computer_operations import run_quantum_algorithm_over_set, cnot_two_gate_operation, \
    output_quantum_gates, remove_redundant_gate_series


class EvolutionaryAlgorithm:
    config: Config

    def __init__(self, config: Config):
        self.config = config

    def evolve_algorithm(self, input_set: ndarray, target_set: ndarray, gates: List[str]) -> None:

        toolbox = base.Toolbox()

        pool = multiprocessing.Pool()

        toolbox.register("map", pool.map)
        toolbox.register("attr_bool", random.randint, 0, 4)

        toolbox.register(
            "individual",
            tools.initRepeat,
            creator.Individual,
            toolbox.attr_bool,
            int(self.config.get_config_value("EvolutionaryAlgorithm", "INDIVIDUAL_DNA_SIZE"))
        )

        toolbox.register("population", tools.initRepeat, list, toolbox.individual)

        toolbox.register(
            "evaluate", evaluate_quantum_algorithm, input_set=input_set, target_set=target_set, gates=gates)
        toolbox.register("mate", tools.cxTwoPoint)
        toolbox.register(
            "mutate",
            tools.mutFlipBit,
            indpb=float(self.config.get_config_value("EvolutionaryAlgorithm", "INDIVIDUAL_SWAP_PROBABILITY"))
        )
        toolbox.register(
            "select",
            tools.selTournament,
            tournsize=int(self.config.get_config_value("EvolutionaryAlgorithm", "TOURNAMENT_SIZE"))
        )

        pop = toolbox.population(n=int(self.config.get_config_value("EvolutionaryAlgorithm", "POPULATION")))
        hof = tools.HallOfFame(1)
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("avg", np.mean)
        stats.register("std", np.std)
        stats.register("min", np.min)
        stats.register("max", np.max)

        algorithms.eaSimple(
            pop,
            toolbox,
            cxpb=float(self.config.get_config_value("EvolutionaryAlgorithm", "BREEDING_PROBABILITY")),
            mutpb=float(self.config.get_config_value("EvolutionaryAlgorithm", "MUTATION_PROBABILITY")),
            ngen=int(self.config.get_config_value("EvolutionaryAlgorithm", "GENERATIONS")),
            stats=stats,
            halloffame=hof,
            verbose=True)

        print("Best individual:")
        output_quantum_gates(dna_to_gates(list(hof[0]), gates))

        run_quantum_algorithm_over_set(input_set, target_set, gates, dna_to_gates(list(hof[0]), gates))


def evaluate_quantum_algorithm(individual: List[int], input_set: ndarray, target_set: ndarray, gates: List[str]):
    return run_quantum_algorithm_over_set(input_set, target_set, gates, dna_to_gates(individual, gates))


def dna_to_gates(individual: List[int], gates: List[str]) -> ndarray:
    gate_array = np.asarray(individual).reshape((-1, len(gates)))
    return remove_redundant_gate_series(cnot_two_gate_operation(gate_array))
