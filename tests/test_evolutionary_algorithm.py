import numpy as np
from deap import base, creator, tools
from unittest.mock import MagicMock

from quantum_ea.evolutionary_algorithm import dna_to_gates, default_evaluate, EvolutionaryAlgorithm
from quantum_ea.config import EAConfig


def test_dna_to_gates():
    dna = [2, 0, 1, 0]
    gate_array = dna_to_gates(dna, num_qubits=2)
    expected_array = np.array([[2, 0], [1, 0]])
    assert np.array_equal(gate_array, expected_array)


def test_default_evaluate(monkeypatch):
    mock_run = MagicMock(return_value=(-0.5,))
    monkeypatch.setattr('quantum_ea.evolutionary_algorithm.run_quantum_algorithm_over_set', mock_run)
    result = default_evaluate([1, 2, 3], np.array([]), np.array([]), num_qubits=1)
    assert result == (-0.5,)


def test_evolve_algorithm(monkeypatch):
    config = EAConfig()
    ea = EvolutionaryAlgorithm(config)

    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)

    ind = creator.Individual([1, 0, 1, 0, 1, 0, 1, 0, 1, 0])
    ind.fitness.values = (0.9,)

    def mock_ea_simple(population, toolbox, cxpb, mutpb, ngen, stats, halloffame, verbose):
        halloffame.update([ind])
        return population, None

    monkeypatch.setattr('quantum_ea.evolutionary_algorithm.algorithms.eaSimple', mock_ea_simple)

    def mock_init_repeat(container, func, n):
        return [ind for _ in range(n)]

    monkeypatch.setattr('quantum_ea.evolutionary_algorithm.tools.initRepeat', mock_init_repeat)

    ea.evolve_algorithm(np.array([[1, 0]]), np.array([[0, 1]]), num_qubits=1)
