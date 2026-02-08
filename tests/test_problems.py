import numpy as np
import pytest

from quantum_ea.problems.base import ProblemDefinition
from quantum_ea.problems.definitions import (
    grover_problem,
    flip_problem,
    inverse_problem,
    fourier_problem,
    deutsch_jozsa_problem,
    bernstein_vazirani_problem,
    all_problems,
)


class TestGrOverProblem:
    def test_returns_problem_definition(self):
        p = grover_problem(num_qubits=3)
        assert isinstance(p, ProblemDefinition)
        assert p.name == "grover"
        assert p.num_qubits == 3
        assert p.input_set.shape == (1, 3)
        assert p.target_set.shape == (1, 8)
        assert np.isclose(p.target_set.sum(), 1.0)

    def test_marked_item(self):
        p = grover_problem(num_qubits=2, marked_item=1)
        assert p.target_set[0, 1] == 1.0
        assert p.target_set[0, 0] == 0.0


class TestFlipProblem:
    def test_returns_problem_definition(self):
        p = flip_problem(num_qubits=2)
        assert isinstance(p, ProblemDefinition)
        assert p.name == "flip"
        assert p.num_qubits == 2


class TestInverseProblem:
    def test_returns_problem_definition(self):
        p = inverse_problem(num_qubits=2)
        assert isinstance(p, ProblemDefinition)
        assert p.name == "inverse"


class TestFourierProblem:
    def test_returns_problem_definition(self):
        p = fourier_problem(num_qubits=2)
        assert isinstance(p, ProblemDefinition)
        assert p.name == "fourier"


class TestDeutschJozsaProblem:
    def test_returns_problem_definition(self):
        p = deutsch_jozsa_problem(num_qubits=3)
        assert isinstance(p, ProblemDefinition)
        assert p.name == "deutsch_jozsa"
        assert p.target_set[0, 0] == 0.0
        assert np.isclose(p.target_set[0].sum(), 1.0)

    def test_uniform_non_zero(self):
        p = deutsch_jozsa_problem(num_qubits=2)
        # Should have uniform probability on non-zero states
        non_zero = p.target_set[0, 1:]
        assert np.allclose(non_zero, non_zero[0])


class TestBernsteinVaziraniProblem:
    def test_returns_problem_definition(self):
        p = bernstein_vazirani_problem(num_qubits=3)
        assert isinstance(p, ProblemDefinition)
        assert p.name == "bernstein_vazirani"
        assert np.isclose(p.target_set[0].sum(), 1.0)

    def test_hidden_string(self):
        p = bernstein_vazirani_problem(num_qubits=3, hidden_string=5)
        assert p.target_set[0, 5] == 1.0


class TestAllProblems:
    def test_returns_six_problems(self):
        problems = all_problems(num_qubits=2)
        assert len(problems) == 6
        names = [p.name for p in problems]
        assert "grover" in names
        assert "flip" in names
        assert "inverse" in names
        assert "fourier" in names
        assert "deutsch_jozsa" in names
        assert "bernstein_vazirani" in names
