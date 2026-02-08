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
examples/
    grover_demonstration.py        # Grover's search vs classical search
    algorithm_building_script.py   # General algorithm evolution
tests/                             # pytest test suite
config.ini                         # EA hyperparameters
```

## Installation

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
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
