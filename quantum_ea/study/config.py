from dataclasses import dataclass, field

from quantum_ea.optimizers.base import OptimizerBase


@dataclass
class StudyConfig:
    num_qubits: int = 3
    evaluation_budget: int = 1000
    num_trials: int = 10
    optimizers: list[OptimizerBase] = field(default_factory=list)
    problem_names: list[str] = field(default_factory=lambda: [
        "grover", "flip", "inverse", "fourier", "deutsch_jozsa", "bernstein_vazirani",
    ])
    base_seed: int = 42
