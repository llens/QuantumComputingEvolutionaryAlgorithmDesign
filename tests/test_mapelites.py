import numpy as np
import pytest

from quantum_ea.optimizers.base import OptimizationResult
from quantum_ea.optimizers.mapelites_optimizer import MAPElitesOptimizer
from quantum_ea.problems.definitions import grover_problem


@pytest.fixture
def simple_problem():
    return grover_problem(num_qubits=2)


class TestMAPElitesOptimizer:
    def test_returns_valid_result(self, simple_problem):
        opt = MAPElitesOptimizer(depth_bins=5, density_bins=5, initial_population=20)
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
        opt = MAPElitesOptimizer(depth_bins=5, density_bins=5, initial_population=20)
        r1 = opt.optimize(
            simple_problem.input_set, simple_problem.target_set,
            simple_problem.num_qubits, simple_problem.recommended_time_steps,
            evaluation_budget=50, seed=123,
        )
        opt2 = MAPElitesOptimizer(depth_bins=5, density_bins=5, initial_population=20)
        r2 = opt2.optimize(
            simple_problem.input_set, simple_problem.target_set,
            simple_problem.num_qubits, simple_problem.recommended_time_steps,
            evaluation_budget=50, seed=123,
        )
        assert r1.best_fitness == r2.best_fitness

    def test_archive_stored(self, simple_problem):
        opt = MAPElitesOptimizer(depth_bins=5, density_bins=5, initial_population=20)
        opt.optimize(
            simple_problem.input_set, simple_problem.target_set,
            simple_problem.num_qubits, simple_problem.recommended_time_steps,
            evaluation_budget=100, seed=42,
        )
        assert len(opt.last_archive) > 0
        for (row, col), (fitness, gates, descriptors) in opt.last_archive.items():
            assert 0 <= row < 5
            assert 0 <= col < 5
            assert 0.0 <= fitness <= 1.0
            assert gates.shape == (simple_problem.recommended_time_steps, simple_problem.num_qubits)
            depth, density = descriptors
            assert depth >= 0
            assert 0.0 <= density <= 1.0

    def test_archive_coverage(self, simple_problem):
        opt = MAPElitesOptimizer(depth_bins=5, density_bins=5, initial_population=50)
        opt.optimize(
            simple_problem.input_set, simple_problem.target_set,
            simple_problem.num_qubits, simple_problem.recommended_time_steps,
            evaluation_budget=500, seed=42,
        )
        # With 500 evaluations we should fill at least a few cells
        assert len(opt.last_archive) >= 2
