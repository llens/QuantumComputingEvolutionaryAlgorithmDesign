import numpy as np
from numpy import ndarray

from quantum_ea.problems.base import ProblemDefinition
from quantum_ea.target_generation import ExampleType, setup_example_problem


def grover_problem(num_qubits: int = 3, marked_item: int | None = None) -> ProblemDefinition:
    """Grover's search: find a marked item with probability 1.0."""
    search_space_size = 2 ** num_qubits
    if marked_item is None:
        marked_item = search_space_size - 1  # last item by default

    input_set = np.array([[0] * num_qubits])
    target_dist = np.zeros(search_space_size)
    target_dist[marked_item] = 1.0
    target_set = np.array([target_dist])

    return ProblemDefinition(
        name="grover",
        input_set=input_set,
        target_set=target_set,
        num_qubits=num_qubits,
        recommended_time_steps=num_qubits * 5,
    )


def flip_problem(num_qubits: int = 2, input_size: int = 4) -> ProblemDefinition:
    """Bitwise NOT: flip all bits."""
    input_set, target_set = setup_example_problem(ExampleType.Flip, num_qubits, input_size)
    return ProblemDefinition(
        name="flip",
        input_set=input_set,
        target_set=target_set,
        num_qubits=num_qubits,
        recommended_time_steps=num_qubits * 3,
    )


def inverse_problem(num_qubits: int = 2, input_size: int = 4) -> ProblemDefinition:
    """Compute 1/x."""
    input_set, target_set = setup_example_problem(ExampleType.Inverse, num_qubits, input_size)
    return ProblemDefinition(
        name="inverse",
        input_set=input_set,
        target_set=target_set,
        num_qubits=num_qubits,
        recommended_time_steps=num_qubits * 4,
    )


def fourier_problem(num_qubits: int = 2, input_size: int = 4) -> ProblemDefinition:
    """Quantum Fourier Transform."""
    input_set, target_set = setup_example_problem(ExampleType.Fourier, num_qubits, input_size)
    return ProblemDefinition(
        name="fourier",
        input_set=input_set,
        target_set=target_set,
        num_qubits=num_qubits,
        recommended_time_steps=num_qubits * 4,
    )


def deutsch_jozsa_problem(num_qubits: int = 3) -> ProblemDefinition:
    """Deutsch-Jozsa: distinguish constant from balanced functions.

    For a balanced function, the quantum algorithm should produce P(|0...0>) = 0.
    We set the target so that all probability is on any state other than |0...0>.
    A uniform distribution over non-zero states serves as target.
    """
    search_space_size = 2 ** num_qubits
    input_set = np.array([[0] * num_qubits])

    # Target: zero probability on |0...0>, uniform on everything else
    target_dist = np.ones(search_space_size) / (search_space_size - 1)
    target_dist[0] = 0.0
    target_set = np.array([target_dist])

    return ProblemDefinition(
        name="deutsch_jozsa",
        input_set=input_set,
        target_set=target_set,
        num_qubits=num_qubits,
        recommended_time_steps=num_qubits * 4,
    )


def bernstein_vazirani_problem(num_qubits: int = 3, hidden_string: int | None = None) -> ProblemDefinition:
    """Bernstein-Vazirani: recover hidden string s from f(x) = s.x mod 2.

    The quantum algorithm should produce P(|s>) = 1.0.
    """
    if hidden_string is None:
        hidden_string = (1 << num_qubits) - 2  # e.g. 110 for 3 qubits

    search_space_size = 2 ** num_qubits
    input_set = np.array([[0] * num_qubits])

    target_dist = np.zeros(search_space_size)
    target_dist[hidden_string] = 1.0
    target_set = np.array([target_dist])

    return ProblemDefinition(
        name="bernstein_vazirani",
        input_set=input_set,
        target_set=target_set,
        num_qubits=num_qubits,
        recommended_time_steps=num_qubits * 4,
    )


def all_problems(num_qubits: int = 3) -> list[ProblemDefinition]:
    """Return all 6 benchmark problems."""
    return [
        grover_problem(num_qubits),
        flip_problem(num_qubits),
        inverse_problem(num_qubits),
        fourier_problem(num_qubits),
        deutsch_jozsa_problem(num_qubits),
        bernstein_vazirani_problem(num_qubits),
    ]
