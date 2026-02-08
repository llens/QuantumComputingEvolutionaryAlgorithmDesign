from collections import defaultdict

import numpy as np

from quantum_ea.study.metrics import AggregatedMetrics


def plot_fitness_comparison(aggregated: list[AggregatedMetrics], save_path: str | None = None) -> None:
    """Bar chart comparing mean fitness across optimizers for each problem."""
    import matplotlib.pyplot as plt

    problems, optimizers = _get_axes(aggregated)
    lookup = _build_lookup(aggregated)

    x = np.arange(len(problems))
    width = 0.8 / len(optimizers)

    fig, ax = plt.subplots(figsize=(12, 6))
    for i, opt in enumerate(optimizers):
        means = [lookup.get((p, opt), (0, 0))[0] for p in problems]
        stds = [lookup.get((p, opt), (0, 0))[1] for p in problems]
        ax.bar(x + i * width, means, width, yerr=stds, label=opt, capsize=3)

    ax.set_xlabel("Problem")
    ax.set_ylabel("Mean Fitness")
    ax.set_title("Fitness Comparison Across Optimizers")
    ax.set_xticks(x + width * (len(optimizers) - 1) / 2)
    ax.set_xticklabels(problems, rotation=30, ha="right")
    ax.legend()
    ax.set_ylim(0, 1.05)
    fig.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=150)
        print(f"Saved fitness comparison to {save_path}")
    plt.close(fig)


def plot_convergence_curves(aggregated: list[AggregatedMetrics], save_path: str | None = None) -> None:
    """Convergence curves: mean fitness history over evaluations for each problem."""
    import matplotlib.pyplot as plt

    problems, optimizers = _get_axes(aggregated)
    lookup_hist = {(a.problem_name, a.optimizer_name): a.all_fitness_histories for a in aggregated}

    n_problems = len(problems)
    cols = min(3, n_problems)
    rows = (n_problems + cols - 1) // cols
    fig, axes = plt.subplots(rows, cols, figsize=(5 * cols, 4 * rows), squeeze=False)

    for idx, problem in enumerate(problems):
        ax = axes[idx // cols][idx % cols]
        for opt in optimizers:
            histories = lookup_hist.get((problem, opt), [])
            if not histories:
                continue
            max_len = max(len(h) for h in histories)
            padded = np.array([h + [h[-1]] * (max_len - len(h)) if h else [0] * max_len for h in histories])
            mean_curve = padded.mean(axis=0)
            ax.plot(mean_curve, label=opt)
        ax.set_title(problem)
        ax.set_xlabel("Evaluations")
        ax.set_ylabel("Best Fitness")
        ax.legend(fontsize=7)

    # Hide unused axes
    for idx in range(n_problems, rows * cols):
        axes[idx // cols][idx % cols].set_visible(False)

    fig.suptitle("Convergence Curves", fontsize=14)
    fig.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=150)
        print(f"Saved convergence curves to {save_path}")
    plt.close(fig)


def plot_wall_clock_comparison(aggregated: list[AggregatedMetrics], save_path: str | None = None) -> None:
    """Bar chart comparing wall-clock time across optimizers for each problem."""
    import matplotlib.pyplot as plt

    problems, optimizers = _get_axes(aggregated)
    lookup = {(a.problem_name, a.optimizer_name): (a.time_mean, a.time_std) for a in aggregated}

    x = np.arange(len(problems))
    width = 0.8 / len(optimizers)

    fig, ax = plt.subplots(figsize=(12, 6))
    for i, opt in enumerate(optimizers):
        means = [lookup.get((p, opt), (0, 0))[0] for p in problems]
        stds = [lookup.get((p, opt), (0, 0))[1] for p in problems]
        ax.bar(x + i * width, means, width, yerr=stds, label=opt, capsize=3)

    ax.set_xlabel("Problem")
    ax.set_ylabel("Wall-Clock Time (s)")
    ax.set_title("Wall-Clock Time Comparison")
    ax.set_xticks(x + width * (len(optimizers) - 1) / 2)
    ax.set_xticklabels(problems, rotation=30, ha="right")
    ax.legend()
    fig.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=150)
        print(f"Saved wall-clock comparison to {save_path}")
    plt.close(fig)


def plot_complexity_comparison(aggregated: list[AggregatedMetrics], save_path: str | None = None) -> None:
    """Bar chart comparing circuit complexity across optimizers for each problem."""
    import matplotlib.pyplot as plt

    problems, optimizers = _get_axes(aggregated)
    lookup = {(a.problem_name, a.optimizer_name): (a.complexity_mean, a.complexity_std) for a in aggregated}

    x = np.arange(len(problems))
    width = 0.8 / len(optimizers)

    fig, ax = plt.subplots(figsize=(12, 6))
    for i, opt in enumerate(optimizers):
        means = [lookup.get((p, opt), (0, 0))[0] for p in problems]
        stds = [lookup.get((p, opt), (0, 0))[1] for p in problems]
        ax.bar(x + i * width, means, width, yerr=stds, label=opt, capsize=3)

    ax.set_xlabel("Problem")
    ax.set_ylabel("Circuit Complexity (non-identity gates)")
    ax.set_title("Circuit Complexity Comparison")
    ax.set_xticks(x + width * (len(optimizers) - 1) / 2)
    ax.set_xticklabels(problems, rotation=30, ha="right")
    ax.legend()
    fig.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=150)
        print(f"Saved complexity comparison to {save_path}")
    plt.close(fig)


def print_summary_table(aggregated: list[AggregatedMetrics]) -> None:
    """Print a text summary table."""
    header = f"{'Problem':<20} {'Optimizer':<25} {'Fitness':>12} {'Time (s)':>12} {'Complexity':>12} {'Conv. Eval':>12}"
    print(header)
    print("-" * len(header))
    for agg in sorted(aggregated, key=lambda a: (a.problem_name, a.optimizer_name)):
        print(
            f"{agg.problem_name:<20} {agg.optimizer_name:<25} "
            f"{agg.fitness_mean:>8.4f}±{agg.fitness_std:<4.3f}"
            f"{agg.time_mean:>8.4f}±{agg.time_std:<4.3f}"
            f"{agg.complexity_mean:>8.1f}±{agg.complexity_std:<4.1f}"
            f"{agg.convergence_eval_mean:>8.1f}±{agg.convergence_eval_std:<4.1f}"
        )


def _get_axes(aggregated: list[AggregatedMetrics]) -> tuple[list[str], list[str]]:
    problems = list(dict.fromkeys(a.problem_name for a in aggregated))
    optimizers = list(dict.fromkeys(a.optimizer_name for a in aggregated))
    return problems, optimizers


def _build_lookup(aggregated: list[AggregatedMetrics]) -> dict:
    return {(a.problem_name, a.optimizer_name): (a.fitness_mean, a.fitness_std) for a in aggregated}
