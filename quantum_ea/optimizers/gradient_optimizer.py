import time

import numpy as np
from numpy import ndarray
from scipy.optimize import minimize
from scipy.special import softmax

from quantum_ea.circuit import (
    _H2, _T2, _I2,
    _full_single_qubit_gate, _cnot_matrix,
    initialise_statevector, compute_probabilities,
)
from quantum_ea.gates import GateType, preprocess_gates
from quantum_ea.fitness import run_quantum_algorithm_over_set, count_non_identity_gates
from quantum_ea.optimizers.base import OptimizerBase, OptimizationResult

# 2x2 base matrices for the 5 gate types
_BASE_MATRICES_2x2 = {
    GateType.IDENTITY: _I2,
    GateType.T_GATE: _T2,
    GateType.HADAMARD: _H2,
}


class GradientOptimizer(OptimizerBase):
    name = "gradient_based"

    def __init__(self, num_restarts: int = 5):
        self.num_restarts = num_restarts

    def optimize(
        self,
        input_set: ndarray,
        target_set: ndarray,
        num_qubits: int,
        time_steps: int,
        evaluation_budget: int,
        seed: int | None = None,
    ) -> OptimizationResult:
        rng = np.random.default_rng(seed)
        num_gate_types = len(GateType)
        num_params = time_steps * num_qubits * num_gate_types

        # Budget split across restarts
        budget_per_restart = max(10, evaluation_budget // self.num_restarts)

        # Pre-compute full gate matrices for single-qubit gates
        full_single_gates = {}
        for gt in [GateType.IDENTITY, GateType.T_GATE, GateType.HADAMARD]:
            for qi in range(num_qubits):
                full_single_gates[(gt, qi)] = _full_single_qubit_gate(
                    _BASE_MATRICES_2x2[gt], qi, num_qubits
                )

        # Pre-compute CNOT matrices
        cnot_down_gates = {}
        cnot_up_gates = {}
        for qi in range(num_qubits):
            if qi + 1 < num_qubits:
                cnot_down_gates[qi] = _cnot_matrix(qi, qi + 1, num_qubits)
            if qi > 0:
                cnot_up_gates[qi] = _cnot_matrix(qi - 1, qi, num_qubits)

        dim = 2 ** num_qubits
        target_dist = target_set[0]
        marked_idx = np.argmax(target_dist)
        sv_init = initialise_statevector(input_set[0], num_qubits)

        eval_count = [0]
        best_fitness = [-1.0]
        best_logits = [None]
        fitness_history: list[float] = []

        def _get_gate_matrices_for_qubit(qi: int) -> list[ndarray]:
            """Return list of 5 full gate matrices for qubit qi."""
            matrices = []
            for gt in range(num_gate_types):
                if gt <= GateType.HADAMARD:
                    matrices.append(full_single_gates[(gt, qi)])
                elif gt == GateType.CNOT_DOWN:
                    matrices.append(cnot_down_gates.get(qi, np.eye(dim, dtype=complex)))
                elif gt == GateType.CNOT_UP:
                    matrices.append(cnot_up_gates.get(qi, np.eye(dim, dtype=complex)))
                else:
                    matrices.append(np.eye(dim, dtype=complex))
            return matrices

        qubit_gate_matrices = [_get_gate_matrices_for_qubit(qi) for qi in range(num_qubits)]

        def neg_fitness(params_flat):
            eval_count[0] += 1
            logits = params_flat.reshape(time_steps, num_qubits, num_gate_types)
            sv = sv_init.copy()

            for t in range(time_steps):
                for qi in range(num_qubits):
                    weights = softmax(logits[t, qi])
                    # Weighted sum of gate matrices
                    mat = np.zeros((dim, dim), dtype=complex)
                    for g in range(num_gate_types):
                        mat += weights[g] * qubit_gate_matrices[qi][g]
                    sv = mat @ sv

            probs = np.abs(sv) ** 2
            fitness = float(probs[marked_idx])

            if fitness > best_fitness[0]:
                best_fitness[0] = fitness
                best_logits[0] = logits.copy()
            fitness_history.append(best_fitness[0])

            return -fitness

        start = time.perf_counter()

        for restart in range(self.num_restarts):
            x0 = rng.standard_normal(num_params) * 0.1
            minimize(
                neg_fitness, x0, method="L-BFGS-B",
                options={"maxfun": budget_per_restart, "maxiter": budget_per_restart},
            )

        elapsed = time.perf_counter() - start

        # Discretize best solution
        if best_logits[0] is not None:
            discrete = np.argmax(best_logits[0], axis=2).astype(int)
            discrete = preprocess_gates(discrete)
            disc_fitness = run_quantum_algorithm_over_set(
                input_set, target_set, num_qubits, discrete
            )[0]
        else:
            discrete = np.zeros((time_steps, num_qubits), dtype=int)
            disc_fitness = 0.0

        return OptimizationResult(
            best_gate_array=discrete,
            best_fitness=disc_fitness,
            total_evaluations=eval_count[0],
            wall_clock_seconds=elapsed,
            circuit_complexity=count_non_identity_gates(discrete),
            fitness_history=fitness_history,
        )
