"""
Quality-Diversity Study: NSGA-II & MAP-Elites Quantum Circuit Optimization

Run with: python -m examples.run_qd_study
Full study: python -m examples.run_qd_study --full
"""

import argparse
import json
import os
from collections import defaultdict

import numpy as np

from quantum_ea.optimizers import (
    RandomSearchOptimizer,
    EAOptimizer,
    GradientOptimizer,
    DLOptimizer,
    NSGA2Optimizer,
    MAPElitesOptimizer,
)
from quantum_ea.optimizers.dl_optimizer import _TORCH_AVAILABLE
from quantum_ea.fitness import clear_fitness_cache
from quantum_ea.problems.definitions import all_problems
from quantum_ea.study.config import StudyConfig
from quantum_ea.study.runner import ExperimentRunner
from quantum_ea.study.plotting import (
    plot_fitness_comparison,
    plot_convergence_curves,
    plot_wall_clock_comparison,
    plot_complexity_comparison,
    print_summary_table,
)
from quantum_ea.study.qd_plotting import (
    plot_pareto_fronts,
    plot_archive_heatmaps,
    plot_archive_coverage,
    plot_qd_score,
    plot_scalability,
)


def _build_optimizers(population_size: int = 50):
    optimizers = [
        RandomSearchOptimizer(),
        EAOptimizer(population_size=population_size),
        GradientOptimizer(num_restarts=3),
    ]
    if _TORCH_AVAILABLE:
        optimizers.append(DLOptimizer(batch_size=8, hidden_size=32))
    else:
        print("Note: PyTorch not available, skipping DL optimizer.\n")
    optimizers.append(NSGA2Optimizer(population_size=population_size))
    optimizers.append(MAPElitesOptimizer(depth_bins=10, density_bins=10, initial_population=population_size))
    return optimizers


def _run_qd_detail(
    qubit_counts: list[int],
    problem_names: list[str],
    evaluation_budget: int,
    num_trials: int,
    base_seed: int,
):
    """Run NSGA-II and MAP-Elites separately to capture Pareto fronts and archives."""
    nsga2 = NSGA2Optimizer(population_size=50)
    mapelites = MAPElitesOptimizer(depth_bins=10, density_bins=10, initial_population=50)

    # Collect per-problem Pareto fronts and archives (from the last trial at each qubit count)
    pareto_data: dict[str, list[tuple[float, int, int]]] = {}
    archive_data: dict[str, dict] = {}
    # Scaling data: {optimizer: {qubit_count: mean_best_fitness}}
    scaling_data: dict[str, dict[int, float]] = defaultdict(dict)

    for nq in qubit_counts:
        problems = all_problems(nq)

        for problem in problems:
            if problem.name not in problem_names:
                continue

            nsga2_fitnesses = []
            mapelites_fitnesses = []

            for trial in range(num_trials):
                seed = base_seed + trial
                clear_fitness_cache()

                print(f"  QD detail: {nq}q / {problem.name} / nsga2 / trial {trial + 1}")
                nsga2_result = nsga2.optimize(
                    problem.input_set, problem.target_set,
                    problem.num_qubits, problem.recommended_time_steps,
                    evaluation_budget, seed=seed,
                )
                nsga2_fitnesses.append(nsga2_result.best_fitness)

                clear_fitness_cache()

                print(f"  QD detail: {nq}q / {problem.name} / map_elites / trial {trial + 1}")
                mapelites_result = mapelites.optimize(
                    problem.input_set, problem.target_set,
                    problem.num_qubits, problem.recommended_time_steps,
                    evaluation_budget, seed=seed,
                )
                mapelites_fitnesses.append(mapelites_result.best_fitness)

            # Store Pareto front from last trial
            label = f"{problem.name} ({nq}q)"
            pareto_data[label] = [
                (f, d, g) for f, d, g, _ in nsga2.last_pareto_front
            ]

            # Store archive from last trial
            archive_data[label] = mapelites.last_archive

            # Scaling data
            scaling_data["nsga2"][nq] = float(np.mean(nsga2_fitnesses))
            scaling_data["map_elites"][nq] = float(np.mean(mapelites_fitnesses))

    return pareto_data, archive_data, scaling_data


def main():
    parser = argparse.ArgumentParser(description="Quality-Diversity Quantum Circuit Optimization Study")
    parser.add_argument("--full", action="store_true", help="Run full study (2-5 qubits, 25000 budget, 20 trials)")
    args = parser.parse_args()

    if args.full:
        qubit_counts = [2, 3, 4, 5]
        evaluation_budget = 25000
        num_trials = 20
    else:
        qubit_counts = [3]
        evaluation_budget = 10000
        num_trials = 10

    output_dir = "study_results/qd_study"
    os.makedirs(output_dir, exist_ok=True)

    print("=== Quality-Diversity Quantum Circuit Optimization Study ===\n")

    # 1. Run all optimizers through existing study framework
    print("--- Phase 1: Comparative Study (all optimizers) ---")
    optimizers = _build_optimizers()
    config = StudyConfig(
        num_qubits=qubit_counts[0],
        evaluation_budget=evaluation_budget,
        num_trials=num_trials,
        optimizers=optimizers,
        qubit_counts=qubit_counts,
    )

    runner = ExperimentRunner(config)
    results = runner.run()

    print("\n--- Summary Table ---")
    print_summary_table(results)

    runner.save_results(results, os.path.join(output_dir, "results.json"))

    # 2. Generate standard comparative plots
    print("\n--- Generating Standard Plots ---")
    plot_fitness_comparison(results, os.path.join(output_dir, "fitness_comparison.png"))
    plot_convergence_curves(results, os.path.join(output_dir, "convergence_curves.png"))
    plot_wall_clock_comparison(results, os.path.join(output_dir, "wall_clock_comparison.png"))
    plot_complexity_comparison(results, os.path.join(output_dir, "complexity_comparison.png"))

    # 3. Run QD-specific detail collection
    print("\n--- Phase 2: QD Detail Collection ---")
    pareto_data, archive_data, scaling_data = _run_qd_detail(
        qubit_counts=qubit_counts,
        problem_names=config.problem_names,
        evaluation_budget=evaluation_budget,
        num_trials=num_trials,
        base_seed=config.base_seed,
    )

    # Add scaling data from the comparative study results
    # Group results by optimizer across qubit counts if we ran scaling
    if len(qubit_counts) > 1:
        scaling_runner = ExperimentRunner(config)
        scaling_results = scaling_runner.run_scaling()
        for nq, agg_list in scaling_results.items():
            for agg in agg_list:
                if agg.optimizer_name not in scaling_data:
                    scaling_data[agg.optimizer_name] = {}
                if nq not in scaling_data[agg.optimizer_name]:
                    scaling_data[agg.optimizer_name][nq] = agg.fitness_mean

    # 4. Generate QD-specific plots
    print("\n--- Generating QD Plots ---")
    plot_pareto_fronts(pareto_data, os.path.join(output_dir, "pareto_fronts.png"))
    plot_archive_heatmaps(archive_data, save_path=os.path.join(output_dir, "archive_heatmaps.png"))
    plot_archive_coverage(archive_data, save_path=os.path.join(output_dir, "archive_coverage.png"))
    plot_qd_score(archive_data, save_path=os.path.join(output_dir, "qd_score.png"))

    if len(qubit_counts) > 1:
        plot_scalability(scaling_data, os.path.join(output_dir, "scalability.png"))

    # 5. Save QD-specific data
    qd_summary = {
        "pareto_fronts": {
            label: [(f, d, g) for f, d, g in points]
            for label, points in pareto_data.items()
        },
        "archive_stats": {
            label: {
                "cells_filled": len(archive),
                "total_cells": 100,
                "coverage_pct": len(archive) / 100 * 100,
                "qd_score": sum(v[0] for v in archive.values()),
                "best_fitness": max(v[0] for v in archive.values()) if archive else 0,
            }
            for label, archive in archive_data.items()
        },
        "scaling": {opt: dict(qf) for opt, qf in scaling_data.items()},
    }
    with open(os.path.join(output_dir, "qd_results.json"), "w") as f:
        json.dump(qd_summary, f, indent=2)
    print(f"QD results saved to {os.path.join(output_dir, 'qd_results.json')}")

    print(f"\nStudy complete! All results saved to {output_dir}/")


if __name__ == "__main__":
    main()
