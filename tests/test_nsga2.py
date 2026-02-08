import numpy as np
import pytest

from quantum_ea.optimizers.base import OptimizationResult
from quantum_ea.optimizers.nsga2_optimizer import NSGA2Optimizer
from quantum_ea.problems.definitions import grover_problem


@pytest.fixture
def simple_problem():
    return grover_problem(num_qubits=2)


class TestNSGA2Optimizer:
    def test_returns_valid_result(self, simple_problem):
        opt = NSGA2Optimizer(population_size=20)
        result = opt.optimize(
            simple_problem.input_set, simple_problem.target_set,
            simple_problem.num_qubits, simple_problem.recommended_time_steps,
            evaluation_budget=100, seed=42,
        )
        assert isinstance(result, OptimizationResult)
        assert result.best_gate_array.shape == (simple_problem.recommended_time_steps, simple_problem.num_qubits)
        assert 0.0 <= result.best_fitness <= 1.0
        assert result.total_evaluations > 0
        assert result.wall_clock_seconds > 0
        assert result.circuit_complexity >= 0

    def test_deterministic_with_seed(self, simple_problem):
        opt = NSGA2Optimizer(population_size=20)
        r1 = opt.optimize(
            simple_problem.input_set, simple_problem.target_set,
            simple_problem.num_qubits, simple_problem.recommended_time_steps,
            evaluation_budget=60, seed=123,
        )
        opt2 = NSGA2Optimizer(population_size=20)
        r2 = opt2.optimize(
            simple_problem.input_set, simple_problem.target_set,
            simple_problem.num_qubits, simple_problem.recommended_time_steps,
            evaluation_budget=60, seed=123,
        )
        assert r1.best_fitness == r2.best_fitness

    def test_pareto_front_stored(self, simple_problem):
        opt = NSGA2Optimizer(population_size=20)
        opt.optimize(
            simple_problem.input_set, simple_problem.target_set,
            simple_problem.num_qubits, simple_problem.recommended_time_steps,
            evaluation_budget=100, seed=42,
        )
        assert len(opt.last_pareto_front) > 0
        for fidelity, depth, gate_count, gates in opt.last_pareto_front:
            assert 0.0 <= fidelity <= 1.0
            assert depth >= 0
            assert gate_count >= 0
            assert gates.shape == (simple_problem.recommended_time_steps, simple_problem.num_qubits)

    def test_fitness_history_populated(self, simple_problem):
        opt = NSGA2Optimizer(population_size=20)
        result = opt.optimize(
            simple_problem.input_set, simple_problem.target_set,
            simple_problem.num_qubits, simple_problem.recommended_time_steps,
            evaluation_budget=100, seed=42,
        )
        assert len(result.fitness_history) > 0
