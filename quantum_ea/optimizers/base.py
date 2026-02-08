from abc import ABC, abstractmethod
from dataclasses import dataclass, field

import numpy as np
from numpy import ndarray


@dataclass
class OptimizationResult:
    best_gate_array: ndarray        # (time_steps, num_qubits), dtype int
    best_fitness: float             # [0, 1]
    total_evaluations: int
    wall_clock_seconds: float
    circuit_complexity: int         # count of non-IDENTITY gates
    fitness_history: list[float] = field(default_factory=list)


class OptimizerBase(ABC):
    name: str

    @abstractmethod
    def optimize(
        self,
        input_set: ndarray,
        target_set: ndarray,
        num_qubits: int,
        time_steps: int,
        evaluation_budget: int,
        seed: int | None = None,
    ) -> OptimizationResult:
        ...
