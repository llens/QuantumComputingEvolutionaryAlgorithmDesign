# Quantum Computing Evolutionary Algorithm Design

Uses evolutionary algorithms to automatically design quantum computing algorithms. Inspired by the ideas in [this PhD thesis](http://theses.ucalgary.ca/jspui/bitstream/11023/2780/3/ucalgary_2016_zahedinejad_ehsan.pdf), but implemented entirely independently using [Qiskit](https://qiskit.org/) and [DEAP](https://deap.readthedocs.io/).

## How it works

The algorithm maps the complete set of quantum gates (T, Hadamard, CNOT) and their relative positions as a simple "DNA". A generation of random quantum algorithm DNA sequences are created and evaluated against a desired output quantum state. The best individuals are bred (two-point crossover) and mutated (random bit flips) to produce the next generation, repeating until a solution converges.

### Gate types

| Symbol | Gate |
|--------|------|
| `T` | T gate |
| `H` | Hadamard gate |
| `. - (+)` | CNOT (control above target) |
| `(+) - .` | CNOT (target above control) |
| `\|` | Identity (no-op) |

### Scoring

Fitness is the probability of measuring the correct marked item from the quantum circuit output. Near-optimal circuits (fitness > 0.99) receive a small penalty for blank gate rows to encourage simpler solutions. DEAP maximises this fitness score.

## Comparative Study

The project includes a study framework that benchmarks **4 optimization methods** across **6 quantum problems**, comparing fitness, convergence speed, wall-clock time, and circuit complexity.

### Optimizers

| Method | Approach |
|--------|----------|
| **Evolutionary Algorithm** | DEAP-based EA with two-point crossover and bit-flip mutation |
| **Random Search** | Uniform random circuit generation (baseline) |
| **Gradient-Based** | Continuous relaxation of gate choices with softmax weighting, optimized via L-BFGS-B with multiple restarts |
| **Deep Learning** | REINFORCE policy gradient with a feedforward network sampling gate choices |

### Problems

| Problem | Target | Classical Complexity |
|---------|--------|---------------------|
| Grover's Search | P(marked\_item) = 1.0 | O(N) linear search |
| Flip | Bitwise NOT | O(N) direct |
| Inverse | 1/x | O(N) direct |
| Fourier | FFT | O(N log N) |
| Deutsch-Jozsa | P(\|0...0>) = 0 for balanced function | O(N/2+1) queries |
| Bernstein-Vazirani | P(\|s>) = 1.0 for hidden string s | O(N) queries |

### Results

Study configuration: 2 qubits, 5000 evaluation budget, 20 trials per (problem, optimizer) pair.

#### Mean Fitness (higher is better)

| Problem | EA | Random Search | Gradient | Deep Learning |
|---------|:--:|:-------------:|:--------:|:-------------:|
| Grover | 0.82 | 0.90 | 0.00 | **1.00** |
| Flip | 0.56 | 0.79 | 0.41 | **0.95** |
| Inverse | 0.58 | 0.90 | 0.23 | **1.00** |
| Fourier | **1.00** | **1.00** | 0.60 | **1.00** |
| Deutsch-Jozsa | 0.80 | 0.90 | 0.26 | **1.00** |
| Bernstein-Vazirani | 0.85 | 0.92 | 0.39 | **1.00** |

#### Convergence Speed (evaluations to reach 95% of final fitness, lower is better)

| Problem | EA | Random Search | Gradient | Deep Learning |
|---------|:--:|:-------------:|:--------:|:-------------:|
| Grover | **19** | 1772 | 3575 | 404 |
| Flip | **4** | 1831 | 590 | 489 |
| Inverse | **6** | 1193 | 2268 | 418 |
| Fourier | **4** | 124 | 199 | 20 |
| Deutsch-Jozsa | **15** | 1543 | 2013 | 287 |
| Bernstein-Vazirani | **9** | 1722 | 430 | 223 |

#### Wall-Clock Time (seconds, lower is better)

| Problem | EA | Random Search | Gradient | Deep Learning |
|---------|:--:|:-------------:|:--------:|:-------------:|
| Grover | **0.59** | 1.03 | 2.70 | 3.76 |
| Flip | **0.51** | 0.81 | 1.52 | 3.61 |
| Inverse | **0.59** | 1.02 | 2.45 | 3.90 |
| Fourier | **0.72** | 1.28 | 1.82 | 3.77 |
| Deutsch-Jozsa | **0.60** | 1.16 | 2.82 | 3.63 |
| Bernstein-Vazirani | **0.59** | 1.10 | 2.30 | 3.80 |

### Key Findings

1. **Deep learning (REINFORCE) achieves the highest fitness**, reaching perfect 1.00 on 4 of 6 problems and 0.95 on Flip (across 20 trials). Given sufficient evaluation budget it consistently outperforms all other methods in solution quality.
2. **EA is the fastest optimizer by a wide margin.** It converges within the first few generations and uses 2-6x less wall-clock time than any competitor, making it the best choice when compute budget is limited.
3. **Random search is a strong baseline.** It reaches perfect fitness on Fourier and scores 0.79-0.92 on all other problems. Its simplicity makes it a useful sanity check for any new optimizer, and it outperforms the EA on several problems when given enough budget.
4. **Gradient-based optimization underperforms on discrete circuit design.** The continuous relaxation via softmax-weighted gate matrices loses information when discretized back to concrete gates. It consistently produces the lowest fitness and slowest convergence across all problems.

### Running the Study

```bash
pip install -r requirements-study.txt   # torch (CPU-only), matplotlib
python -m examples.run_study
```

Results are saved to `study_results/` including JSON data and PNG comparison charts (fitness, convergence curves, wall-clock time, circuit complexity).

## Project structure

```
quantum_ea/                        # Main package
    gates.py                       # GateType enum, CNOT handling, redundancy removal
    circuit.py                     # Circuit initialisation, gate application, measurement
    fitness.py                     # Algorithm execution and scoring
    visualization.py               # ASCII circuit output
    evolutionary_algorithm.py      # EA class with injectable evaluation
    config.py                      # Typed EAConfig from config.ini
    target_generation.py           # Problem definitions (Flip, Inverse, Fourier)
    optimizers/                    # Optimizer implementations
        base.py                    # OptimizerBase ABC + OptimizationResult
        ea_optimizer.py            # DEAP evolutionary algorithm wrapper
        random_search.py           # Random circuit generation baseline
        gradient_optimizer.py      # Continuous relaxation + L-BFGS-B
        dl_optimizer.py            # REINFORCE policy gradient (PyTorch)
    problems/                      # Benchmark problem definitions
        base.py                    # ProblemDefinition dataclass
        definitions.py             # 6 problem factory functions
    classical/                     # Classical algorithm baselines
        baselines.py               # Classical solver for each problem
    study/                         # Study framework
        config.py                  # StudyConfig dataclass
        runner.py                  # ExperimentRunner orchestrator
        metrics.py                 # TrialMetrics, AggregatedMetrics
        plotting.py                # matplotlib comparison charts
examples/
    grover_demonstration.py        # Grover's search vs classical search
    algorithm_building_script.py   # General algorithm evolution
    run_study.py                   # Comparative study entry point
tests/                             # pytest test suite
config.ini                         # EA hyperparameters
```

## Installation

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

For the comparative study (optional):

```bash
pip install -r requirements-study.txt
```

## Usage

Run the Grover's algorithm demonstration:

```bash
python -m examples.grover_demonstration
```

Run the general algorithm builder:

```bash
python -m examples.algorithm_building_script
```

Run the comparative study:

```bash
python -m examples.run_study
```

EA hyperparameters (population size, mutation rate, etc.) are configured in `config.ini`.

## Tests

```bash
pytest
```

## Configuration

Edit `config.ini` to tune the evolutionary algorithm:

```ini
[EvolutionaryAlgorithm]
INDIVIDUAL_DNA_SIZE = 30
INDIVIDUAL_SWAP_PROBABILITY = 0.1
TOURNAMENT_SIZE = 3
POPULATION = 100
BREEDING_PROBABILITY = 0.5
MUTATION_PROBABILITY = 0.2
GENERATIONS = 200
```
