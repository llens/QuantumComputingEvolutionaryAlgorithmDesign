import time

import numpy as np
from numpy import ndarray

from quantum_ea.gates import GateType, preprocess_gates
from quantum_ea.fitness import run_quantum_algorithm_over_set, count_non_identity_gates
from quantum_ea.optimizers.base import OptimizerBase, OptimizationResult


class RandomSearchOptimizer(OptimizerBase):
    name = "random_search"

    def optimize(
        self,
        input_set: ndarray,
        target_set: ndarray,
        num_qubits: int,
        time_steps: int,
        evaluation_budget: int,
        seed: int | None = None,
    ) -> OptimizationResult:
        rng = np.random.default_rng(seed)
        num_gate_types = len(GateType)

        best_fitness = -1.0
        best_gates = None
        fitness_history: list[float] = []

        start = time.perf_counter()
        for i in range(evaluation_budget):
            raw = rng.integers(0, num_gate_types, size=(time_steps, num_qubits))
            gate_array = preprocess_gates(raw)
            fitness_val = run_quantum_algorithm_over_set(
                input_set, target_set, num_qubits, gate_array
            )[0]

            if fitness_val > best_fitness:
                best_fitness = fitness_val
                best_gates = gate_array.copy()

            fitness_history.append(best_fitness)

        elapsed = time.perf_counter() - start

        if best_gates is None:
            best_gates = np.zeros((time_steps, num_qubits), dtype=int)

        return OptimizationResult(
            best_gate_array=best_gates,
            best_fitness=best_fitness,
            total_evaluations=evaluation_budget,
            wall_clock_seconds=elapsed,
            circuit_complexity=count_non_identity_gates(best_gates),
            fitness_history=fitness_history,
        )
