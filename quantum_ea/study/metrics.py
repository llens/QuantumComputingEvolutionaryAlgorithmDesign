from dataclasses import dataclass, field

import numpy as np


@dataclass
class TrialMetrics:
    problem_name: str
    optimizer_name: str
    trial: int
    fitness: float
    total_evaluations: int
    wall_clock_seconds: float
    circuit_complexity: int
    fitness_history: list[float] = field(default_factory=list)

    @property
    def convergence_eval(self) -> int:
        """Evaluation index at which 95% of final fitness was reached."""
        if not self.fitness_history or self.fitness <= 0:
            return self.total_evaluations
        threshold = 0.95 * self.fitness
        for i, f in enumerate(self.fitness_history):
            if f >= threshold:
                return i + 1
        return len(self.fitness_history)


@dataclass
class AggregatedMetrics:
    problem_name: str
    optimizer_name: str
    fitness_mean: float
    fitness_std: float
    fitness_median: float
    time_mean: float
    time_std: float
    complexity_mean: float
    complexity_std: float
    convergence_eval_mean: float
    convergence_eval_std: float
    num_trials: int
    all_fitness_histories: list[list[float]] = field(default_factory=list)


def aggregate_trials(trials: list[TrialMetrics]) -> AggregatedMetrics:
    """Aggregate a list of TrialMetrics for the same (problem, optimizer) pair."""
    fitnesses = [t.fitness for t in trials]
    times = [t.wall_clock_seconds for t in trials]
    complexities = [t.circuit_complexity for t in trials]
    convergences = [t.convergence_eval for t in trials]

    return AggregatedMetrics(
        problem_name=trials[0].problem_name,
        optimizer_name=trials[0].optimizer_name,
        fitness_mean=float(np.mean(fitnesses)),
        fitness_std=float(np.std(fitnesses)),
        fitness_median=float(np.median(fitnesses)),
        time_mean=float(np.mean(times)),
        time_std=float(np.std(times)),
        complexity_mean=float(np.mean(complexities)),
        complexity_std=float(np.std(complexities)),
        convergence_eval_mean=float(np.mean(convergences)),
        convergence_eval_std=float(np.std(convergences)),
        num_trials=len(trials),
        all_fitness_histories=[t.fitness_history for t in trials],
    )
