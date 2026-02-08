# Literature Review: Evolutionary Algorithms for Quantum Circuit Design

## Date: 2026-02-08

---

## 1. Field Overview

The intersection of evolutionary algorithms (EAs) and quantum circuit design is experiencing a renaissance driven by the NISQ era's need for automated, hardware-aware circuit optimization. Three major trends dominate:

1. **EAs remain competitive** with RL and generative models for small-scale circuit synthesis, with advantages in interpretability and ease of implementation
2. **Multi-objective and noise-aware optimization** are becoming standard requirements
3. **Hybrid approaches dominate**: Pure EA or pure RL approaches are being replaced by hybrids (EA + parameter optimization, EA + noise models, GA + QAOA)

---

## 2. Key Recent Papers by Topic

### 2.1 EA-Based Quantum Circuit Synthesis

| Paper | Authors | Venue | Year | Key Contribution |
|-------|---------|-------|------|-----------------|
| Evaluating Mutation Techniques in GA-Based QCS | Kolle et al. | GECCO | 2025 | Delete+swap mutations outperform others for 4-6 qubit circuits |
| Hybrid EA Circuit Construction & Optimization | Sunkel, Altmann, Kolle et al. (LMU Munich) | GECCO | 2025 | Hybrid EA+COBYLA achieves 80% depth reduction at 0.98 fidelity |
| GA4QCO: GA for Quantum Circuit Optimization | Various | arXiv 2302.01303 | 2023 | GA framework for circuit optimization with Qiskit |
| GASP: GA for State Preparation | Various | Nature Sci. Reports | 2023 | GA for quantum state preparation circuits |
| Evolving Quantum Circuits | Tandeitnik & Guerreiro | arXiv 2210.05058 | 2022 | Island-model GA for circuit decomposition |
| EA for Boolean Gates, CA, Entanglement | Bhandari, Nichele, Denysov, Lind | arXiv 2408.00448 | 2024 | Mutation rate balancing for 5-qubit entangling circuits |

### 2.2 Quantum Architecture Search (QAS)

| Paper | Authors | Venue | Year | Key Contribution |
|-------|---------|-------|------|-----------------|
| AQEA-QAS | Li et al. | MDPI Entropy | 2025 | Adaptive quantum evolutionary algorithm for QNN design |
| Noise-Aware QAS with NSGA-II | Various | arXiv 2601.10965 | 2026 | Multi-objective noise-aware architecture search |
| Hierarchical QAS | Various | npj Quantum Information | 2023 | Hierarchical representations for modular search |
| Balanced QNAS | Various | Neurocomputing | 2024 | One-shot NAS with quantum parallelism |

### 2.3 QAOA + Evolutionary Methods

| Paper | Authors | Venue | Year | Key Contribution |
|-------|---------|-------|------|-----------------|
| GA as Classical Optimizer for QAOA | Various | Applied Soft Computing | 2023 | GA outperforms gradient-free optimizers for QAOA parameters |
| QAOA Exponential Time for Linear Functions | Various | GECCO | 2025 | Fundamental complexity limitations of QAOA |
| GA-Based QAOA for Power Networks | Various | Springer | 2024 | Domain-specific QAOA+GA evaluation |

### 2.4 VQE + Evolutionary Optimization

| Paper | Authors | Venue | Year | Key Contribution |
|-------|---------|-------|------|-----------------|
| PSO for VQE (GAQPSO) | Various | Phys. Chem. Chem. Phys. | 2024 | Gradient-free PSO with noise resilience for VQE |
| Surrogate Optimization of VQC | Gustafson et al. | PNAS | 2025 | Classical surrogates to accelerate VQE convergence |

### 2.5 Multi-Objective Quantum Optimization

| Paper | Authors | Venue | Year | Key Contribution |
|-------|---------|-------|------|-----------------|
| Quantum Approximate Multi-Objective Optimization | Various | Nature Comp. Sci. | 2025 | QAOA for Pareto-optimal multi-objective solutions |
| MEAS-PQC | Various | MDPI Entropy | 2023 | Multi-objective EA for parameterized circuit architecture |
| Quality Diversity for VQC Optimization | Zorn, Stein, Kolle et al. | Various | 2025 | CMA-MAE for quality-diversity in circuit design |

### 2.6 Quantum Error Correction + EA

| Paper | Authors | Venue | Year | Key Contribution |
|-------|---------|-------|------|-----------------|
| Engineering QEC Codes with EA | Various | IEEE TQE | 2025 | EA search for optimal stabilizer codes (n<=20 qubits) |
| T-Count Optimizing GA | Various | arXiv 2406.04004 | 2024 | Up to 79% T-depth reduction via GA |

### 2.7 ML-Based Circuit Design (Non-EA)

| Paper | Authors | Venue | Year | Key Contribution |
|-------|---------|-------|------|-----------------|
| FlowQ-Net (GFlowNets) | Various | arXiv 2510.26688 | 2025 | 10-30x more compact circuits vs baselines |
| AlphaTensor-Quantum (DeepMind) | Various | Nature Machine Intelligence | 2025 | RL for efficient non-Clifford gate decomposition |
| Q-Fusion (Diffusion Model) | Various | Penn State | 2025 | Graph-based diffusion for circuit generation |
| Automated QA Design with DSL | Rouillard, Lourens, Petruccione | arXiv 2503.08449 | 2025 | DSL + evolutionary search rediscovers QFT, D-J, Grover |

### 2.8 Surveys

| Paper | Venue | Year |
|-------|-------|------|
| Comprehensive Review of QCO | MDPI Quantum Reports / arXiv 2408.08941 | 2024/2025 |
| QC Synthesis & Compilation Overview | arXiv 2407.00736 | 2024 |
| AI for Quantum Computing | Nature Communications | 2025 |
| Review of Procedures to Evolve Quantum Algorithms | GP & Evolvable Machines (Springer) | 2009 |

---

## 3. Standard Benchmarks in the Field

| Benchmark | Description | Typical Use |
|-----------|-------------|-------------|
| QFT | Quantum Fourier Transform | Circuit synthesis/compilation |
| Grover's Search | Unstructured database search | EA-based circuit discovery |
| MaxCut (via QAOA) | Combinatorial optimization on graphs | QAOA parameter optimization |
| Quantum State Preparation | Prepare specific target states | GA fitness via fidelity |
| Toffoli/Fredkin Gates | Multi-qubit gate decomposition | Gate-level optimization |
| QASMBench | Suite of 1066 test circuits | Cross-framework benchmarking |
| Molecular Ground State (VQE) | H2, LiH, BeH2 molecules | VQE ansatz optimization |
| Random Unitary Compilation | Arbitrary unitary matrices | Compiler optimization |
| Stabilizer Codes | 5-qubit, Steane, Shor codes | QEC code discovery |

**Key Metrics**: State fidelity, circuit depth, gate count (total and T-count), approximation ratio, quantum volume, Hellinger fidelity, process fidelity, hypervolume indicator (multi-objective).

---

## 4. Open Problems Identified Across the Literature

1. **Scalability**: Most EA approaches tested on 4-8 qubits. Classical statevector simulation infeasible beyond ~30 qubits
2. **Continuous Parameters**: Handling rotation gate parameters within discrete evolutionary search remains open
3. **Noise-Aware Optimization**: Most EAs assume ideal execution; NISQ relevance requires noise models
4. **Standardized Benchmarks**: No universally accepted benchmark suite for EA-based quantum circuit synthesis
5. **Search Space Representation**: Optimal circuit encoding for evolutionary operators still debated
6. **Hardware-Software Co-Design**: Joint optimization with hardware topology constraints underexplored
7. **Multi-Objective Trade-offs**: Richer objective spaces (beyond fidelity + depth) largely unexplored
8. **Transfer and Generalization**: Evolved circuits rarely generalize across instances or hardware
9. **Verification at Scale**: Verifying evolved circuits becomes intractable for large qubit counts
10. **Adaptive Operators**: Self-adaptive mutation/crossover rates specifically for quantum circuit EAs
