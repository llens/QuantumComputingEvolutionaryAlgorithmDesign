import numpy as np

from EvolutionaryAlgorithm import dna_to_gates


def test_dna_to_gates():
    dna = [2, 0, 1, 0]
    gates = ["q0", "q1"]
    gate_array = dna_to_gates(dna, gates)
    expected_array = np.array([[2, 0], [1, 0]])
    assert np.array_equal(gate_array, expected_array)
