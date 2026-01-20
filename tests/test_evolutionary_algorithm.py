import numpy as np
from deap import base, creator, tools
from unittest.mock import MagicMock

from EvolutionaryAlgorithm import dna_to_gates, evaluate_quantum_algorithm, EvolutionaryAlgorithm
from Config import Config


def test_dna_to_gates():
    dna = [2, 0, 1, 0]
    gates = ["q0", "q1"]
    gate_array = dna_to_gates(dna, gates)
    expected_array = np.array([[2, 0], [1, 0]])
    assert np.array_equal(gate_array, expected_array)


def test_evaluate_quantum_algorithm(monkeypatch):
    mock_run = MagicMock(return_value=(-0.5,))
    monkeypatch.setattr('EvolutionaryAlgorithm.run_quantum_algorithm_over_set', mock_run)
    result = evaluate_quantum_algorithm([1, 2, 3], np.array([]), np.array([]), ["q0"])
    assert result == (-0.5,)


def test_evolve_algorithm(monkeypatch):
    config = Config()
    ea = EvolutionaryAlgorithm(config)

    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)

    ind = creator.Individual([1, 0, 1, 0, 1, 0, 1, 0, 1, 0])
    ind.fitness.values = (0.9,)

    def mock_ea_simple(population, toolbox, cxpb, mutpb, ngen, stats, halloffame, verbose):
        halloffame.update([ind])
        return population, None

    monkeypatch.setattr('EvolutionaryAlgorithm.algorithms.eaSimple', mock_ea_simple)

    def mock_init_repeat(container, func, n):
        return [ind for _ in range(n)]

    monkeypatch.setattr('EvolutionaryAlgorithm.tools.initRepeat', mock_init_repeat)

    ea.evolve_algorithm(np.array([[1, 0]]), np.array([[0, 1]]), ["q0"])
