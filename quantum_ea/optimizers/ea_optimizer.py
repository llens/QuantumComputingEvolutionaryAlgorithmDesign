import random
import time

import numpy as np
from deap import algorithms, tools, base, creator
from numpy import ndarray

from quantum_ea.gates import preprocess_gates
from quantum_ea.fitness import run_quantum_algorithm_over_set, count_non_identity_gates
from quantum_ea.optimizers.base import OptimizerBase, OptimizationResult


def _dna_to_gates(individual: list[int], num_qubits: int) -> ndarray:
    gate_array = np.asarray(individual).reshape((-1, num_qubits))
    return preprocess_gates(gate_array)


class EAOptimizer(OptimizerBase):
    name = "evolutionary_algorithm"

    def __init__(
        self,
        population_size: int = 100,
        breeding_probability: float = 0.5,
        mutation_probability: float = 0.2,
        tournament_size: int = 3,
        swap_probability: float = 0.1,
    ):
        self.population_size = population_size
        self.breeding_probability = breeding_probability
        self.mutation_probability = mutation_probability
        self.tournament_size = tournament_size
        self.swap_probability = swap_probability

    def optimize(
        self,
        input_set: ndarray,
        target_set: ndarray,
        num_qubits: int,
        time_steps: int,
        evaluation_budget: int,
        seed: int | None = None,
    ) -> OptimizationResult:
        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)

        dna_size = time_steps * num_qubits
        ngen = max(1, evaluation_budget // self.population_size - 1)

        # Build own toolbox
        toolbox = base.Toolbox()
        toolbox.register("attr_gene", random.randint, 0, 4)
        toolbox.register(
            "individual", tools.initRepeat, creator.Individual,
            toolbox.attr_gene, dna_size,
        )
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)

        def evaluate(individual):
            return run_quantum_algorithm_over_set(
                input_set, target_set, num_qubits,
                _dna_to_gates(individual, num_qubits),
            )

        toolbox.register("evaluate", evaluate)
        toolbox.register("mate", tools.cxTwoPoint)
        toolbox.register("mutate", tools.mutFlipBit, indpb=self.swap_probability)
        toolbox.register("select", tools.selTournament, tournsize=self.tournament_size)

        pop = toolbox.population(n=self.population_size)
        hof = tools.HallOfFame(1)
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("max", np.max)

        start = time.perf_counter()
        pop, logbook = algorithms.eaSimple(
            pop, toolbox,
            cxpb=self.breeding_probability,
            mutpb=self.mutation_probability,
            ngen=ngen,
            stats=stats,
            halloffame=hof,
            verbose=False,
        )
        elapsed = time.perf_counter() - start

        best_gates = _dna_to_gates(list(hof[0]), num_qubits)
        best_fitness = run_quantum_algorithm_over_set(
            input_set, target_set, num_qubits, best_gates
        )[0]

        # Extract fitness history from logbook
        fitness_history = [record["max"] for record in logbook]

        total_evals = self.population_size + ngen * self.population_size

        return OptimizationResult(
            best_gate_array=best_gates,
            best_fitness=best_fitness,
            total_evaluations=total_evals,
            wall_clock_seconds=elapsed,
            circuit_complexity=count_non_identity_gates(best_gates),
            fitness_history=fitness_history,
        )
