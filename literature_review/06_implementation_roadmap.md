# Implementation Roadmap: From Current Project to Publication

## Date: 2026-02-08

---

## Recommended Paper: "Illuminating the Landscape of Quantum Circuit Design via Multi-Objective Quality-Diversity Optimization"

This combines Recommendations 1 + 3 from 03_publishable_contributions.md into a single high-impact paper.

---

## Phase 1: Multi-Objective Extension (Weeks 1-2)

### 1.1 Add Objective Functions
- **Fidelity** (existing): probability of measuring target state
- **Circuit depth**: count non-identity time steps (rows where any gate != IDENTITY)
- **Gate count**: `count_non_identity_gates()` already exists in fitness.py
- **Entanglement cost**: count of CNOT gates (subset of gate count)

### 1.2 DEAP NSGA-II Integration
```python
# Replace single-objective fitness
creator.create("FitnessMulti", base.Fitness, weights=(1.0, -1.0, -1.0))
# weights: maximize fidelity, minimize depth, minimize gate count

# Replace tournament selection
toolbox.register("select", tools.selNSGA2)
```

### 1.3 New Optimizer: `nsga2_optimizer.py`
- Inherit from OptimizerBase
- Return OptimizationResult with Pareto front data
- Add hypervolume indicator computation

### 1.4 Scale to 3-5 Qubits
- Your numpy sim handles 5 qubits easily (32-element state vector)
- Update all 6 problems to support configurable qubit count
- Run experiments at n=2,3,4,5

---

## Phase 2: Quality-Diversity Extension (Weeks 3-4)

### 2.1 Install pyribs
```bash
pip install ribs
```

### 2.2 Define Behavioral Descriptors
- **Descriptor 1 - Circuit depth**: number of non-trivial time steps (0 to time_steps)
- **Descriptor 2 - Entanglement density**: fraction of CNOT gates / total non-identity gates (0.0 to 1.0)

### 2.3 Implement MAP-Elites Optimizer
```python
from ribs.archives import GridArchive
from ribs.emitters import EvolutionStrategyEmitter
from ribs.schedulers import Scheduler

archive = GridArchive(
    solution_dim=time_steps * num_qubits,
    dims=[20, 20],  # 20x20 grid
    ranges=[(0, time_steps), (0.0, 1.0)],  # depth range, entanglement range
)
```

### 2.4 Visualization
- 2D heatmaps showing archive illumination per problem
- Compare archive coverage: MAP-Elites vs random sampling
- Identify distinct circuit "families" in different archive regions

---

## Phase 3: Experiments (Weeks 5-6)

### 3.1 Experimental Design
| Factor | Levels |
|--------|--------|
| Problem | Grover, Flip, Inverse, Fourier, Deutsch-Jozsa, Bernstein-Vazirani |
| Qubits | 2, 3, 4, 5 |
| Optimizer | EA (single-obj), NSGA-II (multi-obj), MAP-Elites (QD), Random |
| Evaluation budget | 5000, 25000, 50000 |
| Trials per condition | 20 |

Total: 6 problems x 4 qubit counts x 4 optimizers x 3 budgets x 20 trials = 5,760 runs
At ~1s per run (numpy speed advantage), total wall-clock: ~1.5 hours

### 3.2 Metrics to Report
- **Fidelity**: mean +/- std of best solution
- **Pareto front quality**: hypervolume indicator (for NSGA-II)
- **Archive coverage**: % of cells filled (for MAP-Elites)
- **QD-score**: sum of fitnesses across all archive cells (for MAP-Elites)
- **Convergence speed**: evaluations to 95% of final fitness
- **Wall-clock time**: seconds per run
- **Circuit diversity**: number of structurally distinct high-fitness circuits found
- **Scalability**: how metrics change across 2-5 qubits

### 3.3 Key Research Questions
1. Does NSGA-II discover circuits on the Pareto front that single-objective EA misses?
2. Does MAP-Elites reveal multiple distinct circuit strategies for the same problem?
3. How does the trade-off between fidelity and depth change as qubit count increases?
4. Does the "random search is surprisingly good" finding from the current paper hold at higher qubit counts?
5. At what qubit count does EA consistently outperform random search?

---

## Phase 4: Paper Writing (Weeks 7-8)

### 4.1 Paper Structure
1. **Introduction**: Motivation for multi-objective and quality-diversity approaches
2. **Background**: Quantum circuit synthesis, NSGA-II, MAP-Elites
3. **Method**: Framework architecture, objective functions, behavioral descriptors
4. **Experimental Setup**: Problems, optimizers, metrics, statistical protocol
5. **Results**: Pareto fronts, archive heatmaps, scalability analysis
6. **Discussion**: Circuit families, practical implications, limitations
7. **Conclusion**: Summary + future work (noise-aware QD, parameterized gates)

### 4.2 Key Figures
1. Pareto fronts (fidelity vs depth) for each problem at each qubit count
2. MAP-Elites archive heatmaps (depth x entanglement) for each problem
3. QD-score convergence curves across evaluation budgets
4. Scalability plot: best fidelity vs qubit count for each optimizer
5. Example evolved circuits from different archive regions (using your ASCII visualization)

---

## File Changes Required

### New Files
- `quantum_ea/optimizers/nsga2_optimizer.py` - NSGA-II multi-objective optimizer
- `quantum_ea/optimizers/mapelites_optimizer.py` - MAP-Elites quality-diversity optimizer
- `quantum_ea/study/pareto.py` - Pareto front analysis and hypervolume computation
- `quantum_ea/study/qd_metrics.py` - QD-score, coverage, archive analysis
- `tests/test_nsga2.py` - Tests for NSGA-II optimizer
- `tests/test_mapelites.py` - Tests for MAP-Elites optimizer
- `requirements-qd.txt` - Additional dependency: ribs

### Modified Files
- `quantum_ea/fitness.py` - Add multi-objective fitness return (fidelity, depth, gate_count)
- `quantum_ea/problems/definitions.py` - Ensure all problems work at n=2,3,4,5
- `quantum_ea/study/runner.py` - Support multi-objective and QD experiment runs
- `quantum_ea/study/metrics.py` - Add hypervolume and QD-score metrics
- `quantum_ea/study/plotting.py` - Add Pareto front and archive heatmap plots
- `examples/run_study.py` - Add new optimizer configurations

---

## Dependencies to Add
```
# requirements-qd.txt
ribs>=0.7.0      # pyribs for MAP-Elites
pymoo>=0.6.0     # for hypervolume computation (optional, DEAP has basic support)
```

---

## Timeline Summary

| Week | Activity | Deliverable |
|------|----------|-------------|
| 1-2 | NSGA-II integration + scaling to 5 qubits | Working multi-objective optimizer |
| 3-4 | MAP-Elites implementation + visualization | Working QD optimizer with heatmaps |
| 5-6 | Full experimental campaign (5,760 runs) | Raw results JSON + figures |
| 7-8 | Paper writing + revision | Submission-ready manuscript |

**Total: ~8 weeks to submission-ready paper**
