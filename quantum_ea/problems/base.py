from dataclasses import dataclass

from numpy import ndarray


@dataclass
class ProblemDefinition:
    name: str
    input_set: ndarray
    target_set: ndarray
    num_qubits: int
    recommended_time_steps: int
