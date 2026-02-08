import random
import multiprocessing
from typing import Callable, List, Optional

import numpy as np
from deap import algorithms, tools, base, creator
from numpy import ndarray

from quantum_ea.config import EAConfig
from quantum_ea.gates import preprocess_gates
from quantum_ea.fitness import run_quantum_algorithm_over_set
from quantum_ea.visualization import output_quantum_gates

if not hasattr(creator, "FitnessMax"):
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
if not hasattr(creator, "Individual"):
    creator.create("Individual", list, fitness=creator.FitnessMax)


def dna_to_gates(individual: List[int], num_qubits: int) -> ndarray:
    gate_array = np.asarray(individual).reshape((-1, num_qubits))
    return preprocess_gates(gate_array)


def default_evaluate(individual: List[int], input_set: ndarray, target_set: ndarray, num_qubits: int):
    return run_quantum_algorithm_over_set(input_set, target_set, num_qubits, dna_to_gates(individual, num_qubits))


class EvolutionaryAlgorithm:
    config: EAConfig

    def __init__(self, config: EAConfig, evaluate_fn: Optional[Callable] = None):
        self.config = config
        self.evaluate_fn = evaluate_fn

    def evolve_algorithm(self, input_set: ndarray, target_set: ndarray, num_qubits: int) -> None:
        toolbox = base.Toolbox()

        pool = multiprocessing.Pool()

        toolbox.register("map", pool.map)
        toolbox.register("attr_bool", random.randint, 0, 4)

        toolbox.register(
            "individual",
            tools.initRepeat,
            creator.Individual,
            toolbox.attr_bool,
            self.config.individual_dna_size
        )

        toolbox.register("population", tools.initRepeat, list, toolbox.individual)

        evaluate = self.evaluate_fn if self.evaluate_fn is not None else default_evaluate
        toolbox.register(
            "evaluate", evaluate, input_set=input_set, target_set=target_set, num_qubits=num_qubits)
        toolbox.register("mate", tools.cxTwoPoint)
        toolbox.register(
            "mutate",
            tools.mutFlipBit,
            indpb=self.config.individual_swap_probability
        )
        toolbox.register(
            "select",
            tools.selTournament,
            tournsize=self.config.tournament_size
        )

        pop = toolbox.population(n=self.config.population)
        hof = tools.HallOfFame(1)
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("avg", np.mean)
        stats.register("std", np.std)
        stats.register("min", np.min)
        stats.register("max", np.max)

        algorithms.eaSimple(
            pop,
            toolbox,
            cxpb=self.config.breeding_probability,
            mutpb=self.config.mutation_probability,
            ngen=self.config.generations,
            stats=stats,
            halloffame=hof,
            verbose=True)

        print("Best individual:")
        output_quantum_gates(dna_to_gates(list(hof[0]), num_qubits))

        run_quantum_algorithm_over_set(input_set, target_set, num_qubits, dna_to_gates(list(hof[0]), num_qubits))
