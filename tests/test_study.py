import json
import os
import tempfile

import numpy as np
import pytest

from quantum_ea.study.config import StudyConfig
from quantum_ea.study.metrics import TrialMetrics, AggregatedMetrics, aggregate_trials
from quantum_ea.study.runner import ExperimentRunner
from quantum_ea.optimizers.random_search import RandomSearchOptimizer


class TestTrialMetrics:
    def test_convergence_eval(self):
        m = TrialMetrics(
            problem_name="test", optimizer_name="test", trial=0,
            fitness=1.0, total_evaluations=100, wall_clock_seconds=1.0,
            circuit_complexity=5, fitness_history=[0.1, 0.5, 0.8, 0.95, 1.0],
        )
        # 95% of 1.0 = 0.95, first reached at index 3 -> eval 4
        assert m.convergence_eval == 4

    def test_convergence_eval_zero_fitness(self):
        m = TrialMetrics(
            problem_name="test", optimizer_name="test", trial=0,
            fitness=0.0, total_evaluations=10, wall_clock_seconds=0.1,
            circuit_complexity=0, fitness_history=[0.0] * 10,
        )
        assert m.convergence_eval == 10


class TestAggregateTrials:
    def test_aggregation(self):
        trials = [
            TrialMetrics("p", "o", i, fitness=0.5 + i * 0.1,
                         total_evaluations=100, wall_clock_seconds=1.0,
                         circuit_complexity=5, fitness_history=[0.5 + i * 0.1])
            for i in range(3)
        ]
        agg = aggregate_trials(trials)
        assert isinstance(agg, AggregatedMetrics)
        assert agg.problem_name == "p"
        assert agg.optimizer_name == "o"
        assert agg.num_trials == 3
        assert np.isclose(agg.fitness_mean, 0.6)


class TestExperimentRunner:
    def test_run_small(self):
        config = StudyConfig(
            num_qubits=2,
            evaluation_budget=20,
            num_trials=2,
            optimizers=[RandomSearchOptimizer()],
            problem_names=["grover"],
        )
        runner = ExperimentRunner(config)
        results = runner.run()
        assert len(results) == 1
        assert results[0].problem_name == "grover"
        assert results[0].optimizer_name == "random_search"
        assert results[0].num_trials == 2

    def test_save_results(self):
        config = StudyConfig(
            num_qubits=2,
            evaluation_budget=10,
            num_trials=1,
            optimizers=[RandomSearchOptimizer()],
            problem_names=["grover"],
        )
        runner = ExperimentRunner(config)
        results = runner.run()

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            path = f.name
        try:
            runner.save_results(results, path)
            with open(path) as f:
                data = json.load(f)
            assert len(data) == 1
            assert data[0]["problem_name"] == "grover"
        finally:
            os.unlink(path)
