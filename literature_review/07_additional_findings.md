# Additional Findings from Emerging Topics Search

## Date: 2026-02-08

---

## Standout Results Not Covered in Main Review

### Grammatical Evolution for Grover -- 97.9% vs 44.2% on Real Hardware (2025)
- **Paper**: "Evolving Hardware-Efficient Grover Circuits via Grammatical Evolution"
- Uses BNF grammar + hardware-aware fitness function
- Evolved Grover circuits for all 8 basis states of a 3-qubit system on IBM ibm_brisbane
- **Best evolved circuit: 97.9% fidelity** vs 44.2-47.6% for standard Grover
- Depth reduction: up to 93.3%. Gate count reduction: up to 92.7%
- https://www.researchgate.net/publication/392226977

### EXAQC -- Neuroevolution-Style Circuit Search (RIT)
- Simultaneously searches gate types, qubit connectivity, parameterization, and circuit depth
- Accommodates hardware/noise constraints
- Achieves >90% accuracy on Iris, Wine, Seeds, Breast Cancer benchmarks
- Supports both Qiskit and PennyLane
- https://quantumzeitgeist.com/ai-quantum-circuits-evolves-bypassing-limits-more-powerful/

### QuantumNAS -- Noise-Adaptive Co-Search (Wang et al., HPCA 2022, heavily cited 2023-2025)
- SuperCircuit decouples training from search
- Noise-adaptive evolutionary co-search for (circuit, qubit mapping) pairs
- Tested on 14 quantum computers, 12 QML and VQE benchmarks
- 95% 2-class, 85% 4-class, 32% 10-class classification accuracy on real hardware
- Lowest eigenvalues for VQE on H2, H2O, LiH, CH4, BeH2
- https://hanlab.mit.edu/projects/quantumnas

### Evolutionary BP+OSD Decoding for QEC (Dec 2025)
- Differential evolution optimizes belief propagation weights
- Achieves comparable performance with 5 BP iterations vs 32 (standard) or 150 (BP with memory)
- Tested on surface codes and quantum LDPC codes
- https://arxiv.org/abs/2512.18273

### RBF Surrogate for 127-Qubit QAOA (2025)
- Radial basis function interpolation as adaptive, hyperparameter-free surrogate
- Successfully optimized 127-qubit QAOA circuits on IBM hardware
- Measurement counts: 10^4-10^5
- https://arxiv.org/abs/2501.04636

---

## Key Active Research Groups

### LMU Munich (Linnhoff-Popien group)
Most prolific group in the field:
- Michael Kolle: Mutation strategies (GECCO 2025)
- Philipp Altmann: Hybrid EA (GECCO 2025)
- Maximilian Zorn, Jonas Stein: Quality-Diversity (ICAPS 2025)
- Leo Sunkel: Circuit construction (GECCO 2025)
- Thomas Gabor: QNEAT (GECCO Companion 2023)

### Other Active Groups
- **MIT HAN Lab** (Wang): QuantumNAS
- **University of KwaZulu-Natal** (Rouillard, Petruccione): DSL-based algorithm design
- **RIT** (Kar, Krutz, Desell): EXAQC neuroevolution
- **OsloMet** (Bhandari, Nichele, Lind): EA for entanglement
- **University of Melbourne** (Creevey, Hill, Hollenberg): GASP

---

## Key Software Toolkits

| Tool | Description | URL |
|------|-------------|-----|
| EVOVAQ | Python toolbox for evolutionary VQC training (Qiskit) | https://github.com/Quasar-UniNA/EVOVAQ |
| EXAQC | Neuroevolution for quantum circuits (Qiskit + PennyLane) | (RIT) |
| AlphaTensor-Quantum | DeepMind RL for T-count optimization | https://github.com/google-deepmind/alphatensor_quantum |
| MQT Bench | ~70,000 benchmark circuits, 2-130 qubits | https://github.com/munich-quantum-toolkit/bench |
| Benchpress | 1000+ tests for circuit compilation (up to 930 qubits) | Nature Comp. Sci. 2025 |
| RevLib | Reversible function/circuit benchmarks | https://revlib.org/ |

---

## Revised Whitespace Assessment (Post Emerging-Topics Search)

| Topic | Papers Found | Status |
|-------|-------------|--------|
| Quality-Diversity / MAP-Elites | 1 (ICAPS 2025) | VERY UNDER-EXPLORED |
| Transfer Learning for Evolved Circuits | ~2 (tangential) | SEVERELY UNDER-EXPLORED |
| Co-Evolution (multiple populations) | 0 (true co-evolution) | EMPTY |
| Surrogate-Assisted EA for QCS | 2-3 (but none EA-specific) | UNDER-EXPLORED |
| Grammatical Evolution for QCS | 2 (strong results) | PROMISING but SMALL |
| Noise-Aware EA | 3-4 (QuantumNAS dominant) | GROWING |
| Multi-Objective EA for QCS | 3-4 | GROWING |
| Adaptive Mutation for QCS | 1 (GECCO 2025) | UNDER-EXPLORED |

---

## Updated Publication Opportunities

The grammatical evolution result (97.9% fidelity on real hardware) suggests a **sixth publication direction** not in the original recommendations:

### Recommendation 6: Grammatical Evolution with Hardware Constraints
- Formalize your existing gate preprocessing rules (CNOT adjacency, H/T cancellation) as a BNF grammar
- Use grammatical evolution instead of flat integer encoding
- Test on IBM/IonQ hardware noise models
- Compare GE vs standard GA vs random search
- The 2025 GE paper only tested 3-qubit Grover; expanding to your 6-problem benchmark suite + 2-5 qubits would be a clear extension
- **Target**: GECCO 2026, Evolutionary Computation journal

This would be **lower effort** than the MAP-Elites recommendation since you can reuse your existing fitness infrastructure -- you just need to replace the genome representation.
