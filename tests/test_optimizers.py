import numpy as np
import pytest

from quantum_ea.optimizers.base import OptimizationResult
from quantum_ea.optimizers.random_search import RandomSearchOptimizer
from quantum_ea.optimizers.ea_optimizer import EAOptimizer
from quantum_ea.optimizers.gradient_optimizer import GradientOptimizer
from quantum_ea.optimizers.dl_optimizer import DLOptimizer, _TORCH_AVAILABLE
from quantum_ea.problems.definitions import grover_problem


@pytest.fixture
def simple_problem():
    return grover_problem(num_qubits=2)


class TestRandomSearch:
    def test_returns_valid_result(self, simple_problem):
        opt = RandomSearchOptimizer()
        result = opt.optimize(
            simple_problem.input_set, simple_problem.target_set,
            simple_problem.num_qubits, simple_problem.recommended_time_steps,
            evaluation_budget=50, seed=42,
        )
        assert isinstance(result, OptimizationResult)
        assert result.best_gate_array.shape == (simple_problem.recommended_time_steps, simple_problem.num_qubits)
        assert 0.0 <= result.best_fitness <= 1.0
        assert result.total_evaluations == 50
        assert result.wall_clock_seconds > 0
        assert result.circuit_complexity >= 0
        assert len(result.fitness_history) == 50

    def test_deterministic_with_seed(self, simple_problem):
        opt = RandomSearchOptimizer()
        r1 = opt.optimize(
            simple_problem.input_set, simple_problem.target_set,
            simple_problem.num_qubits, simple_problem.recommended_time_steps,
            evaluation_budget=20, seed=123,
        )
        r2 = opt.optimize(
            simple_problem.input_set, simple_problem.target_set,
            simple_problem.num_qubits, simple_problem.recommended_time_steps,
            evaluation_budget=20, seed=123,
        )
        assert r1.best_fitness == r2.best_fitness

    def test_fitness_history_monotonic(self, simple_problem):
        opt = RandomSearchOptimizer()
        result = opt.optimize(
            simple_problem.input_set, simple_problem.target_set,
            simple_problem.num_qubits, simple_problem.recommended_time_steps,
            evaluation_budget=30, seed=42,
        )
        for i in range(1, len(result.fitness_history)):
            assert result.fitness_history[i] >= result.fitness_history[i - 1]


class TestEAOptimizer:
    def test_returns_valid_result(self, simple_problem):
        opt = EAOptimizer(population_size=20)
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
        assert len(result.fitness_history) > 0


class TestGradientOptimizer:
    def test_returns_valid_result(self, simple_problem):
        opt = GradientOptimizer(num_restarts=2)
        result = opt.optimize(
            simple_problem.input_set, simple_problem.target_set,
            simple_problem.num_qubits, simple_problem.recommended_time_steps,
            evaluation_budget=50, seed=42,
        )
        assert isinstance(result, OptimizationResult)
        assert result.best_gate_array.shape == (simple_problem.recommended_time_steps, simple_problem.num_qubits)
        assert 0.0 <= result.best_fitness <= 1.0
        assert result.total_evaluations > 0
        assert len(result.fitness_history) > 0


@pytest.mark.skipif(not _TORCH_AVAILABLE, reason="torch not installed")
class TestDLOptimizer:
    def test_returns_valid_result(self, simple_problem):
        opt = DLOptimizer(batch_size=4, hidden_size=16)
        result = opt.optimize(
            simple_problem.input_set, simple_problem.target_set,
            simple_problem.num_qubits, simple_problem.recommended_time_steps,
            evaluation_budget=20, seed=42,
        )
        assert isinstance(result, OptimizationResult)
        assert result.best_gate_array.shape == (simple_problem.recommended_time_steps, simple_problem.num_qubits)
        assert 0.0 <= result.best_fitness <= 1.0
        assert result.total_evaluations > 0
        assert len(result.fitness_history) > 0

    def test_graceful_without_torch(self):
        """Test the fallback path when torch is absent (simulated)."""
        import quantum_ea.optimizers.dl_optimizer as mod
        original = mod._TORCH_AVAILABLE
        mod._TORCH_AVAILABLE = False
        try:
            opt = DLOptimizer()
            problem = grover_problem(num_qubits=2)
            result = opt.optimize(
                problem.input_set, problem.target_set,
                problem.num_qubits, problem.recommended_time_steps,
                evaluation_budget=10,
            )
            assert result.best_fitness == 0.0
            assert result.total_evaluations == 0
        finally:
            mod._TORCH_AVAILABLE = original
