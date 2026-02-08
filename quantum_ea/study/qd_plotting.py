"""Quality-diversity specific visualizations for NSGA-II and MAP-Elites."""

import numpy as np


def plot_pareto_fronts(
    pareto_data: dict[str, list[tuple[float, int, int]]],
    save_path: str | None = None,
) -> None:
    """2D scatter of fidelity vs depth, colored by optimizer/problem.

    pareto_data: {label: [(fidelity, depth, gate_count), ...]}
    """
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(8, 6))
    for label, points in pareto_data.items():
        if not points:
            continue
        fidelities = [p[0] for p in points]
        depths = [p[1] for p in points]
        ax.scatter(depths, fidelities, label=label, alpha=0.7, s=30)

    ax.set_xlabel("Active Circuit Depth")
    ax.set_ylabel("Fidelity")
    ax.set_title("Pareto Fronts: Fidelity vs Depth")
    ax.legend(fontsize=7)
    ax.set_ylim(-0.05, 1.05)
    fig.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=150)
        print(f"Saved Pareto fronts to {save_path}")
    plt.close(fig)


def plot_archive_heatmaps(
    archives: dict[str, dict[tuple[int, int], tuple[float, any, any]]],
    depth_bins: int = 10,
    density_bins: int = 10,
    save_path: str | None = None,
) -> None:
    """2D heatmap of MAP-Elites archive fitness per problem.

    archives: {problem_name: {(row, col): (fitness, gates, descriptors)}}
    """
    import matplotlib.pyplot as plt

    n = len(archives)
    if n == 0:
        return
    cols = min(3, n)
    rows = (n + cols - 1) // cols
    fig, axes = plt.subplots(rows, cols, figsize=(5 * cols, 4 * rows), squeeze=False)

    for idx, (name, archive) in enumerate(archives.items()):
        ax = axes[idx // cols][idx % cols]
        grid = np.full((depth_bins, density_bins), np.nan)
        for (r, c), (fitness, _, _) in archive.items():
            if 0 <= r < depth_bins and 0 <= c < density_bins:
                grid[r, c] = fitness

        im = ax.imshow(grid, origin="lower", aspect="auto", vmin=0, vmax=1, cmap="viridis")
        ax.set_xlabel("Entanglement Density Bin")
        ax.set_ylabel("Active Depth Bin")
        ax.set_title(name)
        fig.colorbar(im, ax=ax, label="Fitness")

    for idx in range(n, rows * cols):
        axes[idx // cols][idx % cols].set_visible(False)

    fig.suptitle("MAP-Elites Archive Heatmaps", fontsize=14)
    fig.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=150)
        print(f"Saved archive heatmaps to {save_path}")
    plt.close(fig)


def plot_archive_coverage(
    archives: dict[str, dict[tuple[int, int], any]],
    depth_bins: int = 10,
    density_bins: int = 10,
    save_path: str | None = None,
) -> None:
    """Bar chart of archive coverage (% cells filled) per problem."""
    import matplotlib.pyplot as plt

    total_cells = depth_bins * density_bins
    names = list(archives.keys())
    coverages = [len(archives[n]) / total_cells * 100 for n in names]

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(names, coverages, color="steelblue")
    ax.set_xlabel("Problem")
    ax.set_ylabel("Archive Coverage (%)")
    ax.set_title("MAP-Elites Archive Coverage")
    ax.set_ylim(0, 105)
    plt.xticks(rotation=30, ha="right")
    fig.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=150)
        print(f"Saved archive coverage to {save_path}")
    plt.close(fig)


def plot_qd_score(
    archives: dict[str, dict[tuple[int, int], tuple[float, any, any]]],
    save_path: str | None = None,
) -> None:
    """Bar chart of QD-score (sum of fitnesses across all archive cells) per problem."""
    import matplotlib.pyplot as plt

    names = list(archives.keys())
    scores = [sum(v[0] for v in archives[n].values()) for n in names]

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(names, scores, color="darkorange")
    ax.set_xlabel("Problem")
    ax.set_ylabel("QD-Score (sum of fitnesses)")
    ax.set_title("MAP-Elites QD-Score")
    plt.xticks(rotation=30, ha="right")
    fig.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=150)
        print(f"Saved QD-score to {save_path}")
    plt.close(fig)


def plot_scalability(
    scaling_data: dict[str, dict[int, float]],
    save_path: str | None = None,
) -> None:
    """Line plot of best fitness vs qubit count for each optimizer.

    scaling_data: {optimizer_name: {qubit_count: mean_best_fitness}}
    """
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(8, 5))
    for opt_name, qubit_fitness in scaling_data.items():
        qubits = sorted(qubit_fitness.keys())
        fitnesses = [qubit_fitness[q] for q in qubits]
        ax.plot(qubits, fitnesses, marker="o", label=opt_name)

    ax.set_xlabel("Number of Qubits")
    ax.set_ylabel("Mean Best Fitness")
    ax.set_title("Scalability: Fitness vs Qubit Count")
    ax.legend(fontsize=8)
    ax.set_ylim(-0.05, 1.05)
    ax.set_xticks(sorted({q for d in scaling_data.values() for q in d}))
    fig.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=150)
        print(f"Saved scalability plot to {save_path}")
    plt.close(fig)
