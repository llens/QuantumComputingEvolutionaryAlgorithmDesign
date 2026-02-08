import json
import time
from collections import defaultdict
from dataclasses import asdict

import numpy as np

from quantum_ea.fitness import clear_fitness_cache
from quantum_ea.problems.definitions import (
    grover_problem,
    flip_problem,
    inverse_problem,
    fourier_problem,
    deutsch_jozsa_problem,
    bernstein_vazirani_problem,
)
from quantum_ea.study.config import StudyConfig
from quantum_ea.study.metrics import TrialMetrics, AggregatedMetrics, aggregate_trials

_PROBLEM_FACTORIES = {
    "grover": grover_problem,
    "flip": flip_problem,
    "inverse": inverse_problem,
    "fourier": fourier_problem,
    "deutsch_jozsa": deutsch_jozsa_problem,
    "bernstein_vazirani": bernstein_vazirani_problem,
}


class ExperimentRunner:
    def __init__(self, config: StudyConfig):
        self.config = config

    def run(self) -> list[AggregatedMetrics]:
        all_trials: dict[tuple[str, str], list[TrialMetrics]] = defaultdict(list)
        total_runs = len(self.config.problem_names) * len(self.config.optimizers) * self.config.num_trials
        run_count = 0

        for problem_name in self.config.problem_names:
            factory = _PROBLEM_FACTORIES[problem_name]
            problem = factory(self.config.num_qubits)

            for optimizer in self.config.optimizers:
                for trial in range(self.config.num_trials):
                    run_count += 1
                    seed = self.config.base_seed + trial
                    clear_fitness_cache()

                    print(
                        f"  [{run_count}/{total_runs}] "
                        f"{problem_name} / {optimizer.name} / trial {trial + 1}"
                    )

                    result = optimizer.optimize(
                        input_set=problem.input_set,
                        target_set=problem.target_set,
                        num_qubits=problem.num_qubits,
                        time_steps=problem.recommended_time_steps,
                        evaluation_budget=self.config.evaluation_budget,
                        seed=seed,
                    )

                    metrics = TrialMetrics(
                        problem_name=problem_name,
                        optimizer_name=optimizer.name,
                        trial=trial,
                        fitness=result.best_fitness,
                        total_evaluations=result.total_evaluations,
                        wall_clock_seconds=result.wall_clock_seconds,
                        circuit_complexity=result.circuit_complexity,
                        fitness_history=result.fitness_history,
                    )
                    all_trials[(problem_name, optimizer.name)].append(metrics)

        aggregated = []
        for key in all_trials:
            aggregated.append(aggregate_trials(all_trials[key]))

        return aggregated

    def save_results(self, aggregated: list[AggregatedMetrics], path: str) -> None:
        """Save aggregated results to JSON."""
        data = []
        for agg in aggregated:
            d = {
                "problem_name": agg.problem_name,
                "optimizer_name": agg.optimizer_name,
                "fitness_mean": agg.fitness_mean,
                "fitness_std": agg.fitness_std,
                "fitness_median": agg.fitness_median,
                "time_mean": agg.time_mean,
                "time_std": agg.time_std,
                "complexity_mean": agg.complexity_mean,
                "complexity_std": agg.complexity_std,
                "convergence_eval_mean": agg.convergence_eval_mean,
                "convergence_eval_std": agg.convergence_eval_std,
                "num_trials": agg.num_trials,
            }
            data.append(d)

        with open(path, "w") as f:
            json.dump(data, f, indent=2)
        print(f"Results saved to {path}")

    def run_scaling(self) -> dict[int, list[AggregatedMetrics]]:
        """Run experiments across multiple qubit counts.

        Returns results grouped by qubit count.
        """
        results_by_qubits: dict[int, list[AggregatedMetrics]] = {}

        for nq in self.config.qubit_counts:
            print(f"\n--- Qubit count: {nq} ---")
            all_trials: dict[tuple[str, str], list[TrialMetrics]] = defaultdict(list)

            for problem_name in self.config.problem_names:
                factory = _PROBLEM_FACTORIES[problem_name]
                problem = factory(nq)

                for optimizer in self.config.optimizers:
                    for trial in range(self.config.num_trials):
                        seed = self.config.base_seed + trial
                        clear_fitness_cache()

                        print(
                            f"  {nq}q: {problem_name} / {optimizer.name} / trial {trial + 1}"
                        )

                        result = optimizer.optimize(
                            input_set=problem.input_set,
                            target_set=problem.target_set,
                            num_qubits=problem.num_qubits,
                            time_steps=problem.recommended_time_steps,
                            evaluation_budget=self.config.evaluation_budget,
                            seed=seed,
                        )

                        metrics = TrialMetrics(
                            problem_name=problem_name,
                            optimizer_name=optimizer.name,
                            trial=trial,
                            fitness=result.best_fitness,
                            total_evaluations=result.total_evaluations,
                            wall_clock_seconds=result.wall_clock_seconds,
                            circuit_complexity=result.circuit_complexity,
                            fitness_history=result.fitness_history,
                        )
                        all_trials[(problem_name, optimizer.name)].append(metrics)

            aggregated = []
            for key in all_trials:
                aggregated.append(aggregate_trials(all_trials[key]))
            results_by_qubits[nq] = aggregated

        return results_by_qubits
