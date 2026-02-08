import time

import numpy as np
from numpy import ndarray

from quantum_ea.gates import GateType, preprocess_gates
from quantum_ea.fitness import (
    run_quantum_algorithm_over_set,
    count_non_identity_gates,
    count_active_depth,
    count_cnot_gates,
)
from quantum_ea.optimizers.base import OptimizerBase, OptimizationResult


def _compute_descriptors(gate_array: ndarray) -> tuple[int, float]:
    """Return (active_depth, entanglement_density) for archive indexing."""
    depth = count_active_depth(gate_array)
    non_id = count_non_identity_gates(gate_array)
    if non_id == 0:
        return depth, 0.0
    density = count_cnot_gates(gate_array) / non_id
    return depth, density


class MAPElitesOptimizer(OptimizerBase):
    name = "map_elites"

    def __init__(
        self,
        depth_bins: int = 10,
        density_bins: int = 10,
        initial_population: int = 100,
        mutation_rate: float = 0.15,
    ):
        self.depth_bins = depth_bins
        self.density_bins = density_bins
        self.initial_population = initial_population
        self.mutation_rate = mutation_rate
        # Archive: (row, col) -> (fitness, gate_array, (active_depth, entanglement_density))
        self.last_archive: dict[tuple[int, int], tuple[float, ndarray, tuple[int, float]]] = {}

    def _discretize(self, active_depth: int, entanglement_density: float, max_depth: int) -> tuple[int, int]:
        """Map continuous descriptors to archive grid cell."""
        row = min(int(active_depth * self.depth_bins / (max_depth + 1)), self.depth_bins - 1)
        col = min(int(entanglement_density * self.density_bins), self.density_bins - 1)
        return row, col

    def _mutate(self, gate_array: ndarray, rng: np.random.Generator) -> ndarray:
        """Flip random genes to random gate types."""
        child = gate_array.copy()
        num_gate_types = len(GateType)
        mask = rng.random(child.shape) < self.mutation_rate
        child[mask] = rng.integers(0, num_gate_types, size=mask.sum())
        return preprocess_gates(child)

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
        max_depth = time_steps

        archive: dict[tuple[int, int], tuple[float, ndarray, tuple[int, float]]] = {}
        fitness_history: list[float] = []
        best_fitness = -1.0
        evals_used = 0

        start = time.perf_counter()

        # Phase 1: Random seeding
        seed_count = min(self.initial_population, evaluation_budget)
        for _ in range(seed_count):
            raw = rng.integers(0, num_gate_types, size=(time_steps, num_qubits))
            gates = preprocess_gates(raw)
            fitness = run_quantum_algorithm_over_set(
                input_set, target_set, num_qubits, gates,
            )[0]
            evals_used += 1

            depth, density = _compute_descriptors(gates)
            cell = self._discretize(depth, density, max_depth)

            if cell not in archive or fitness > archive[cell][0]:
                archive[cell] = (fitness, gates.copy(), (depth, density))

            best_fitness = max(best_fitness, fitness)
            fitness_history.append(best_fitness)

        # Phase 2: Mutation loop
        while evals_used < evaluation_budget:
            if not archive:
                break

            # Pick random occupied cell, mutate its occupant
            cell_keys = list(archive.keys())
            parent_cell = cell_keys[rng.integers(len(cell_keys))]
            parent_gates = archive[parent_cell][1]

            child_gates = self._mutate(parent_gates, rng)
            fitness = run_quantum_algorithm_over_set(
                input_set, target_set, num_qubits, child_gates,
            )[0]
            evals_used += 1

            depth, density = _compute_descriptors(child_gates)
            cell = self._discretize(depth, density, max_depth)

            if cell not in archive or fitness > archive[cell][0]:
                archive[cell] = (fitness, child_gates.copy(), (depth, density))

            best_fitness = max(best_fitness, fitness)
            fitness_history.append(best_fitness)

        elapsed = time.perf_counter() - start

        self.last_archive = archive

        # Return best-fidelity member
        if archive:
            best_cell = max(archive, key=lambda k: archive[k][0])
            best_gates = archive[best_cell][1]
            best_fitness = archive[best_cell][0]
        else:
            best_gates = np.zeros((time_steps, num_qubits), dtype=int)
            best_fitness = 0.0

        return OptimizationResult(
            best_gate_array=best_gates,
            best_fitness=best_fitness,
            total_evaluations=evals_used,
            wall_clock_seconds=elapsed,
            circuit_complexity=count_non_identity_gates(best_gates),
            fitness_history=fitness_history,
        )
