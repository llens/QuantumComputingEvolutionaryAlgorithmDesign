# Gap Analysis: This Project vs. the Literature

## Date: 2026-02-08

---

## Current Project Summary

This project implements a comparative study of 4 optimization methods (EA, Random Search, Gradient-Based, REINFORCE) for evolving quantum circuits across 6 benchmark problems (Grover, Flip, Inverse, Fourier, Deutsch-Jozsa, Bernstein-Vazirani) using:
- Pure numpy statevector simulation (~microseconds/eval)
- DEAP evolutionary algorithm framework
- 2-qubit circuits with 5 discrete gate types (I, T, H, CNOT_DOWN, CNOT_UP)
- Single-objective fitness (target probability)
- Fitness caching keyed by circuit bytes

## Strengths vs. Literature

| Strength | How It Compares |
|----------|----------------|
| **Simulation speed** (~us/eval) | 100-1000x faster than Qiskit Aer used in GA4QCO, GASP, etc. |
| **Fitness caching** | Rarely seen in published frameworks |
| **DEAP integration** | Mature, well-tested; most papers use custom implementations |
| **Multi-method comparison** | 4 methods compared head-to-head (EA, Random, Gradient, DL) |
| **Reproducibility** | Deterministic seeds, 20 trials per condition, 480 total runs |
| **No runtime Qiskit dependency** | Eliminates version churn, import overhead |

## Gaps vs. Literature

| Gap | Severity | What the Literature Does |
|-----|----------|--------------------------|
| **Fixed discrete gate set only** | HIGH | GA4QCO, GASP, GECCO 2025 all support parameterized rotation gates (Rx, Ry, Rz) |
| **Single-objective optimization** | HIGH | Trend is multi-objective (NSGA-II for fidelity vs depth vs gate count); DEAP supports this natively |
| **No noise model** | HIGH | Noise-Aware QAS (2026), GA-QAOA on real hardware show noise-aware fitness is critical for NISQ |
| **Only 2-qubit experiments** | MEDIUM | Most papers test on 4-6+ qubits |
| **Limited gate set** | MEDIUM | No Rx, Ry, Rz, CZ, Toffoli gates; limits circuit expressiveness |
| **No adaptive operators** | MEDIUM | GECCO 2025 shows benefits of adaptive mutation rates |
| **No hardware topology constraints** | LOW | Compilation-aware synthesis is an emerging direction |
| **No transfer/generalization study** | LOW | DSL paper (2503.08449) shows generalizable algorithm learning |

## Key Positioning

The project occupies a practical niche: **a lightweight, fast, dependency-minimal framework for evolving small quantum circuits**. Most comparable to GA4QCO and GASP, but differentiated by simulation speed and DEAP integration.

The main gap is the **lack of continuous parameters, multi-objective optimization, and noise modeling** -- all of which are feasible extensions of the existing architecture.
