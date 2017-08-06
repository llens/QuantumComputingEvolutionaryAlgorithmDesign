import random
import array
import multiprocessing
import numpy as np
from deap import algorithms, tools, base, creator
from quantum_computer_operations import run_quantum_algorithm_over_set, cnot_two_gate_operation,\
    output_quantum_gates


def evolve_algorithm(input_set, target_set, gates):
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", array.array, typecode='b', fitness=creator.FitnessMax)

    toolbox = base.Toolbox()

    pool = multiprocessing.Pool()

    toolbox.register("map", pool.map)
    toolbox.register("attr_bool", random.randint, 0, 4)

    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, 60)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    toolbox.register("evaluate", evaluate_quantum_algorithm, input_set=input_set, target_set=target_set, gates=gates)
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
    toolbox.register("select", tools.selTournament, tournsize=3)

    pop = toolbox.population(n=300)
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("std", np.std)
    stats.register("min", np.min)
    stats.register("max", np.max)

    pop, log = algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=30,
                                   stats=stats, halloffame=hof, verbose=True)

    print 'Best individual:'
    output_quantum_gates(gates, dna_to_gates(list(hof[0]), gates))


def evaluate_quantum_algorithm(individual, input_set, target_set, gates):
    return run_quantum_algorithm_over_set(input_set, target_set, gates, dna_to_gates(individual, gates))


def dna_to_gates(individual, gates):
    gate_array = np.asarray(individual).reshape((-1, len(gates)))
    gate_array = cnot_two_gate_operation(gate_array)

    return cnot_two_gate_operation(gate_array)
