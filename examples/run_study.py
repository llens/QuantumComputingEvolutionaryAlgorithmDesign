"""
Comparative Study: Quantum Circuit Optimization Methods

Run with: python -m examples.run_study

Uses a small configuration by default for quick verification.
Increase evaluation_budget and num_trials for publication-quality results.
"""

import os

from quantum_ea.optimizers import (
    EAOptimizer,
    RandomSearchOptimizer,
    GradientOptimizer,
    DLOptimizer,
)
from quantum_ea.optimizers.dl_optimizer import _TORCH_AVAILABLE
from quantum_ea.classical.baselines import run_classical_baseline
from quantum_ea.study.config import StudyConfig
from quantum_ea.study.runner import ExperimentRunner
from quantum_ea.study.plotting import (
    plot_fitness_comparison,
    plot_convergence_curves,
    plot_wall_clock_comparison,
    plot_complexity_comparison,
    print_summary_table,
)


def main():
    print("=== Quantum Circuit Optimization: Comparative Study ===\n")

    # Build optimizer list
    optimizers = [
        RandomSearchOptimizer(),
        EAOptimizer(population_size=50),
        GradientOptimizer(num_restarts=3),
    ]
    if _TORCH_AVAILABLE:
        optimizers.append(DLOptimizer(batch_size=8, hidden_size=32))
    else:
        print("Note: PyTorch not available, skipping DL optimizer.\n")

    config = StudyConfig(
        num_qubits=2,
        evaluation_budget=5000,
        num_trials=20,
        optimizers=optimizers,
        problem_names=["grover", "flip", "inverse", "fourier", "deutsch_jozsa", "bernstein_vazirani"],
    )

    # Run classical baselines
    print("--- Classical Baselines ---")
    for problem_name in config.problem_names:
        result = run_classical_baseline(problem_name, config.num_qubits)
        print(f"  {problem_name}: {result.complexity_class} ({result.num_operations} ops, {result.time_seconds:.6f}s)")
    print()

    # Run quantum optimizers
    print("--- Running Quantum Optimizer Trials ---")
    runner = ExperimentRunner(config)
    results = runner.run()

    # Summary
    print("\n--- Summary Table ---")
    print_summary_table(results)

    # Save results
    output_dir = "study_results"
    os.makedirs(output_dir, exist_ok=True)
    runner.save_results(results, os.path.join(output_dir, "results.json"))

    # Generate plots
    print("\n--- Generating Plots ---")
    plot_fitness_comparison(results, os.path.join(output_dir, "fitness_comparison.png"))
    plot_convergence_curves(results, os.path.join(output_dir, "convergence_curves.png"))
    plot_wall_clock_comparison(results, os.path.join(output_dir, "wall_clock_comparison.png"))
    plot_complexity_comparison(results, os.path.join(output_dir, "complexity_comparison.png"))

    print("\nStudy complete! Results saved to study_results/")


if __name__ == "__main__":
    main()
