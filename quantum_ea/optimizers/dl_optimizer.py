import time

import numpy as np
from numpy import ndarray

from quantum_ea.gates import GateType, preprocess_gates
from quantum_ea.fitness import run_quantum_algorithm_over_set, count_non_identity_gates
from quantum_ea.optimizers.base import OptimizerBase, OptimizationResult

_TORCH_AVAILABLE = False
try:
    import torch
    import torch.nn as nn
    _TORCH_AVAILABLE = True
except ImportError:
    pass


class DLOptimizer(OptimizerBase):
    name = "deep_learning"

    def __init__(self, learning_rate: float = 1e-3, batch_size: int = 16, hidden_size: int = 64):
        self.learning_rate = learning_rate
        self.batch_size = batch_size
        self.hidden_size = hidden_size

    def optimize(
        self,
        input_set: ndarray,
        target_set: ndarray,
        num_qubits: int,
        time_steps: int,
        evaluation_budget: int,
        seed: int | None = None,
    ) -> OptimizationResult:
        if not _TORCH_AVAILABLE:
            # Fallback: return a zero result if torch not available
            gate_array = np.zeros((time_steps, num_qubits), dtype=int)
            return OptimizationResult(
                best_gate_array=gate_array,
                best_fitness=0.0,
                total_evaluations=0,
                wall_clock_seconds=0.0,
                circuit_complexity=0,
                fitness_history=[],
            )

        if seed is not None:
            torch.manual_seed(seed)
            np.random.seed(seed)

        num_gate_types = len(GateType)
        dim = 2 ** num_qubits
        total_positions = time_steps * num_qubits

        # Target distribution as network input
        target_input = torch.tensor(target_set[0], dtype=torch.float32)

        # Simple feedforward policy network
        net = nn.Sequential(
            nn.Linear(dim, self.hidden_size),
            nn.ReLU(),
            nn.Linear(self.hidden_size, self.hidden_size),
            nn.ReLU(),
            nn.Linear(self.hidden_size, total_positions * num_gate_types),
        )
        optimizer = torch.optim.Adam(net.parameters(), lr=self.learning_rate)

        best_fitness = -1.0
        best_gates = np.zeros((time_steps, num_qubits), dtype=int)
        fitness_history: list[float] = []
        baseline = 0.0
        eval_count = 0

        start = time.perf_counter()

        num_iterations = evaluation_budget // self.batch_size

        for iteration in range(num_iterations):
            logits = net(target_input).reshape(total_positions, num_gate_types)
            dist = torch.distributions.Categorical(logits=logits)

            log_probs_batch = []
            rewards_batch = []

            for _ in range(self.batch_size):
                actions = dist.sample()
                log_prob = dist.log_prob(actions).sum()

                gate_array = actions.detach().numpy().reshape(time_steps, num_qubits).astype(int)
                gate_array = preprocess_gates(gate_array)

                fitness_val = run_quantum_algorithm_over_set(
                    input_set, target_set, num_qubits, gate_array
                )[0]
                eval_count += 1

                log_probs_batch.append(log_prob)
                rewards_batch.append(fitness_val)

                if fitness_val > best_fitness:
                    best_fitness = fitness_val
                    best_gates = gate_array.copy()

            fitness_history.append(best_fitness)

            # REINFORCE update
            rewards = torch.tensor(rewards_batch, dtype=torch.float32)
            baseline = 0.9 * baseline + 0.1 * rewards.mean().item()
            advantages = rewards - baseline

            loss = torch.stack([-lp * adv for lp, adv in zip(log_probs_batch, advantages)]).mean()

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        elapsed = time.perf_counter() - start

        return OptimizationResult(
            best_gate_array=best_gates,
            best_fitness=best_fitness,
            total_evaluations=eval_count,
            wall_clock_seconds=elapsed,
            circuit_complexity=count_non_identity_gates(best_gates),
            fitness_history=fitness_history,
        )
