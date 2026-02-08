import time
from dataclasses import dataclass

import numpy as np


@dataclass
class ClassicalResult:
    name: str
    answer: object
    num_operations: int
    time_seconds: float
    complexity_class: str


def _classical_grover(num_qubits: int) -> ClassicalResult:
    """Classical linear search over N items."""
    n = 2 ** num_qubits
    marked = n - 1
    start = time.perf_counter()
    ops = 0
    for i in range(n):
        ops += 1
        if i == marked:
            answer = i
            break
    elapsed = time.perf_counter() - start
    return ClassicalResult("linear_search", answer, ops, elapsed, "O(N)")


def _classical_flip(num_qubits: int) -> ClassicalResult:
    """Classical bitwise NOT on all N-bit strings."""
    n = 2 ** num_qubits
    start = time.perf_counter()
    results = []
    for i in range(n):
        results.append(~i & ((1 << num_qubits) - 1))
    elapsed = time.perf_counter() - start
    return ClassicalResult("bitwise_not", results, n, elapsed, "O(N)")


def _classical_inverse(num_qubits: int) -> ClassicalResult:
    """Classical 1/x computation."""
    n = 2 ** num_qubits
    start = time.perf_counter()
    results = []
    for i in range(n):
        results.append(1.0 / i if i != 0 else 0.0)
    elapsed = time.perf_counter() - start
    return ClassicalResult("direct_inverse", results, n, elapsed, "O(N)")


def _classical_fourier(num_qubits: int) -> ClassicalResult:
    """Classical FFT."""
    n = 2 ** num_qubits
    data = np.random.randn(n)
    start = time.perf_counter()
    result = np.fft.fft(data)
    elapsed = time.perf_counter() - start
    ops = int(n * np.log2(n)) if n > 1 else 1
    return ClassicalResult("fft", result, ops, elapsed, "O(N log N)")


def _classical_deutsch_jozsa(num_qubits: int) -> ClassicalResult:
    """Classical Deutsch-Jozsa: must query N/2 + 1 in worst case."""
    n = 2 ** num_qubits
    queries_needed = n // 2 + 1
    start = time.perf_counter()
    # Simulate querying a balanced function
    f_values = [0] * (n // 2) + [1] * (n // 2)
    seen_values = set()
    ops = 0
    answer = "unknown"
    for v in f_values:
        ops += 1
        seen_values.add(v)
        if len(seen_values) > 1:
            answer = "balanced"
            break
        if ops > n // 2:
            answer = "constant"
            break
    elapsed = time.perf_counter() - start
    return ClassicalResult("exhaustive_query", answer, ops, elapsed, "O(N/2+1)")


def _classical_bernstein_vazirani(num_qubits: int) -> ClassicalResult:
    """Classical Bernstein-Vazirani: N queries to recover hidden string."""
    hidden = (1 << num_qubits) - 2
    start = time.perf_counter()
    recovered = 0
    ops = 0
    for i in range(num_qubits):
        query = 1 << i
        # f(x) = s.x mod 2
        result = bin(hidden & query).count('1') % 2
        recovered |= result << i
        ops += 1
    elapsed = time.perf_counter() - start
    return ClassicalResult("bitwise_query", recovered, ops, elapsed, "O(N)")


_BASELINES = {
    "grover": _classical_grover,
    "flip": _classical_flip,
    "inverse": _classical_inverse,
    "fourier": _classical_fourier,
    "deutsch_jozsa": _classical_deutsch_jozsa,
    "bernstein_vazirani": _classical_bernstein_vazirani,
}


def run_classical_baseline(problem_name: str, num_qubits: int) -> ClassicalResult:
    """Run the classical baseline for a given problem."""
    if problem_name not in _BASELINES:
        raise ValueError(f"No classical baseline for problem: {problem_name}")
    return _BASELINES[problem_name](num_qubits)
