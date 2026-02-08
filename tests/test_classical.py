import pytest

from quantum_ea.classical.baselines import ClassicalResult, run_classical_baseline


class TestClassicalBaselines:
    @pytest.mark.parametrize("problem_name", [
        "grover", "flip", "inverse", "fourier", "deutsch_jozsa", "bernstein_vazirani",
    ])
    def test_returns_valid_result(self, problem_name):
        result = run_classical_baseline(problem_name, num_qubits=3)
        assert isinstance(result, ClassicalResult)
        assert result.name
        assert result.num_operations > 0
        assert result.time_seconds >= 0
        assert result.complexity_class

    def test_grover_finds_item(self):
        result = run_classical_baseline("grover", num_qubits=3)
        assert result.answer == 7  # 2^3 - 1

    def test_bernstein_vazirani_recovers_string(self):
        result = run_classical_baseline("bernstein_vazirani", num_qubits=3)
        assert result.answer == 6  # (1 << 3) - 2 = 6

    def test_unknown_problem_raises(self):
        with pytest.raises(ValueError, match="No classical baseline"):
            run_classical_baseline("nonexistent", num_qubits=2)
