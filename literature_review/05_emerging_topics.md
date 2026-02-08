# Emerging Topics and Niche Opportunities

## Date: 2026-02-08

---

## 1. Quality-Diversity (QD) for Quantum Circuits -- HIGHLY UNDER-EXPLORED

**Current state**: Only one paper (Zorn et al., CMA-MAE for VQC optimization on MaxCut/MVC/MIS/MaxClique). Used CMA-MAE with circuit sparsity + gate diversity as behavioral descriptors. Found optimal solutions within 20 optimization steps.

**Gap**: No application of MAP-Elites or other QD algorithms to algorithmic quantum circuit discovery (QFT, Grover, etc.). No study of the *diversity* of viable circuits for a given quantum task.

**Opportunity**: MAP-Elites with (depth, entanglement_density) as descriptors could reveal fundamentally different circuit families for the same problem -- a finding with both practical value (hardware flexibility) and theoretical interest.

---

## 2. Noise-Aware Evolutionary Circuit Synthesis -- NASCENT

**Current state**: Only one direct paper (arXiv 2601.10965, Jan 2026) applies NSGA-II with noise models. Uses variable-depth encoding and dual objectives (performance vs hardware cost).

**Gap**: No fast numpy-based noisy simulation for EA fitness evaluation. All existing work uses Qiskit noise models (slow). No surrogate-assisted noise-aware EA.

**Opportunity**: Implement depolarizing/amplitude damping noise in numpy, use as fitness function. Show that noise-aware evolution produces more hardware-robust circuits.

---

## 3. Surrogate-Assisted Evolutionary Quantum Circuit Optimization -- VERY NEW

**Current state**: Gustafson et al. (PNAS 2025) pioneered surrogate optimization for VQC, but used gradient-based methods, not EA. Graph-Based Bayesian Optimization for QAS (arXiv 2512.09586) explores Bayesian surrogates.

**Gap**: No surrogate-assisted EA specifically for quantum circuit structure optimization. The combination of cheap numpy fitness evaluation + surrogate pre-screening for even faster evaluation is unexplored.

**Opportunity**: Train random forest or Gaussian process on (circuit_features -> fitness) from your fast numpy evaluations. Use surrogate for pre-screening in EA population. Potentially enable scaling to larger qubit counts.

---

## 4. Transfer Learning for Evolved Quantum Circuits -- NEARLY EMPTY

**Current state**: Rouillard et al. (arXiv 2503.08449) showed DSL-based circuits learned on 5 qubits generalize to larger instances. No EA-based transfer learning work exists.

**Gap**: Can circuits evolved for 2-qubit problems seed evolution for 3-4-5 qubit problems? Can circuits evolved for Grover transfer to Bernstein-Vazirani?

**Opportunity**: Study cross-problem and cross-scale transfer of evolved circuit building blocks. This is a natural extension of your multi-problem benchmark.

---

## 5. Grammatical Evolution for Quantum Circuits -- SPARSE

**Current state**: "Gene Expression Programming for Quantum Computing" (ACM TQC 2023) is the closest work. "GeQuPI" (J. Systems and Software 2024) applies genetic improvement to quantum programs.

**Gap**: No application of grammatical evolution (GE) with a quantum circuit grammar to constrain the search space to syntactically valid circuits. Your gate preprocessing (CNOT adjacency enforcement, redundant gate removal) is already doing this implicitly.

**Opportunity**: Formalize your gate constraints as a BNF grammar and use GE to ensure all evolved circuits are valid by construction. This eliminates wasted evaluations on invalid circuits.

---

## 6. Co-Evolution for Quantum Circuits -- EMPTY

**Current state**: "Quantum-Inspired Neuro Coevolution" (2020) is only tangentially related. No true co-evolutionary approach to quantum circuit design exists.

**Gap**: Co-evolving circuit structure + test cases, or co-evolving complementary circuit sub-modules, is completely unexplored.

**Opportunity**: Co-evolve the oracle and the algorithm simultaneously; or co-evolve circuit "layers" as separate populations that must work together.

---

## 7. Evolutionary Quantum Error Mitigation -- NASCENT

**Current state**: One paper (IEEE 2021) uses GA for measurement error mitigation. Evolutionary QEC code search (IEEE TQE 2025) addresses code design but not error mitigation strategies.

**Gap**: No EA-based search for optimal error mitigation protocols (zero-noise extrapolation parameters, probabilistic error cancellation strategies).

**Opportunity**: Evolve error mitigation strategy parameters alongside circuit structure. Novel and practically important for NISQ.

---

## Summary: Whitespace Map

| Topic | Papers Found | Opportunity Level |
|-------|-------------|-------------------|
| Quality-Diversity / MAP-Elites for QCS | 1 | VERY HIGH |
| Noise-Aware EA for QCS | 1 | HIGH |
| Surrogate-Assisted EA for QCS | 0 (direct) | HIGH |
| Transfer Learning for Evolved Circuits | 0 | HIGH |
| Co-Evolution for Quantum Circuits | 0 | HIGH |
| Grammatical Evolution for QCS | 1 (tangential) | MEDIUM-HIGH |
| Evolutionary Quantum Error Mitigation | 1 (tangential) | MEDIUM |
