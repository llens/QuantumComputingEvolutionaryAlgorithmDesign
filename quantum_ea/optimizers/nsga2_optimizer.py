import random
import time

import numpy as np
from deap import algorithms, tools, base, creator
from numpy import ndarray

from quantum_ea.gates import GateType, preprocess_gates
from quantum_ea.fitness import (
    run_quantum_algorithm_over_set,
    count_non_identity_gates,
    count_active_depth,
)
from quantum_ea.optimizers.base import OptimizerBase, OptimizationResult

# Separate DEAP creator classes to avoid conflict with EAOptimizer's FitnessMax
if not hasattr(creator, "FitnessNSGA"):
    creator.create("FitnessNSGA", base.Fitness, weights=(1.0, -1.0, -1.0))
if not hasattr(creator, "IndividualNSGA"):
    creator.create("IndividualNSGA", list, fitness=creator.FitnessNSGA)


def _dna_to_gates(individual: list[int], num_qubits: int) -> ndarray:
    gate_array = np.asarray(individual).reshape((-1, num_qubits))
    return preprocess_gates(gate_array)


class NSGA2Optimizer(OptimizerBase):
    name = "nsga2"

    def __init__(
        self,
        population_size: int = 100,
        breeding_probability: float = 0.5,
        mutation_probability: float = 0.2,
        swap_probability: float = 0.1,
    ):
        self.population_size = population_size
        self.breeding_probability = breeding_probability
        self.mutation_probability = mutation_probability
        self.swap_probability = swap_probability
        self.last_pareto_front: list[tuple[float, int, int, ndarray]] = []

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
        num_gate_types = len(GateType)
        ngen = max(1, evaluation_budget // self.population_size - 1)

        toolbox = base.Toolbox()
        toolbox.register("attr_gene", random.randint, 0, num_gate_types - 1)
        toolbox.register(
            "individual", tools.initRepeat, creator.IndividualNSGA,
            toolbox.attr_gene, dna_size,
        )
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)

        def evaluate(individual):
            gates = _dna_to_gates(individual, num_qubits)
            fidelity = run_quantum_algorithm_over_set(
                input_set, target_set, num_qubits, gates,
            )[0]
            depth = count_active_depth(gates)
            gate_count = count_non_identity_gates(gates)
            return fidelity, depth, gate_count

        toolbox.register("evaluate", evaluate)
        toolbox.register("mate", tools.cxTwoPoint)
        toolbox.register("mutate", tools.mutFlipBit, indpb=self.swap_probability)
        toolbox.register("select", tools.selNSGA2)

        pop = toolbox.population(n=self.population_size)

        # Evaluate initial population
        fitnesses = list(map(toolbox.evaluate, pop))
        for ind, fit in zip(pop, fitnesses):
            ind.fitness.values = fit

        # Track best fidelity per generation
        fitness_history = []
        best_fidelity_so_far = max(f[0] for f in fitnesses)
        fitness_history.append(best_fidelity_so_far)

        start = time.perf_counter()

        for gen in range(ngen):
            offspring = algorithms.varOr(
                pop, toolbox,
                lambda_=self.population_size,
                cxpb=self.breeding_probability,
                mutpb=self.mutation_probability,
            )

            # Evaluate offspring that don't have fitness
            invalid = [ind for ind in offspring if not ind.fitness.valid]
            fitnesses = list(map(toolbox.evaluate, invalid))
            for ind, fit in zip(invalid, fitnesses):
                ind.fitness.values = fit

            # Mu+Lambda selection
            pop = toolbox.select(pop + offspring, self.population_size)

            gen_best = max(ind.fitness.values[0] for ind in pop)
            best_fidelity_so_far = max(best_fidelity_so_far, gen_best)
            fitness_history.append(best_fidelity_so_far)

        elapsed = time.perf_counter() - start

        # Extract Pareto front
        pareto_front = tools.sortNondominated(pop, len(pop), first_front_only=True)[0]
        self.last_pareto_front = []
        for ind in pareto_front:
            fidelity, depth, gate_count = ind.fitness.values
            gates = _dna_to_gates(list(ind), num_qubits)
            self.last_pareto_front.append((fidelity, int(depth), int(gate_count), gates))

        # Pick best-fidelity member from Pareto front for backward compat
        best_member = max(self.last_pareto_front, key=lambda x: x[0])
        best_gates = best_member[3]
        best_fitness = best_member[0]

        total_evals = self.population_size + ngen * self.population_size

        return OptimizationResult(
            best_gate_array=best_gates,
            best_fitness=best_fitness,
            total_evaluations=total_evals,
            wall_clock_seconds=elapsed,
            circuit_complexity=count_non_identity_gates(best_gates),
            fitness_history=fitness_history,
        )
