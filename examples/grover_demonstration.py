"""
This script provides a practical demonstration of Grover's search algorithm
compared to a classical unstructured search.

The problem is to find a specific "marked" item in an unstructured list.
"""

import numpy as np
from quantum_ea import EvolutionaryAlgorithm, EAConfig

def classical_unstructured_search(search_space, marked_item):
    """
    Performs a classical linear search to find the marked item.

    Args:
        search_space (list): The list of items to search through.
        marked_item (any): The item to find.

    Returns:
        tuple: A tuple containing the index of the marked item and the number of queries.
               Returns (None, num_queries) if the item is not found.
    """
    num_queries = 0
    for index, item in enumerate(search_space):
        num_queries += 1
        if item == marked_item:
            return index, num_queries
    return None, num_queries

def main():
    """
    Main function to run the demonstration.
    """
    n_bits = 3
    search_space_size = 2**n_bits

    # The search space is all possible n-bit strings
    search_space = [format(i, f'0{n_bits}b') for i in range(search_space_size)]

    # The item we are looking for
    marked_item = '101'

    print("--- Grover's Algorithm Demonstration ---")
    print(f"Search Space Size (N): {search_space_size}")
    print(f"Marked Item: {marked_item}\n")

    # --- Grover's Problem Definition ---
    n_qubits = 3
    marked_item_bitstring = '101' # Corresponds to decimal 5
    marked_item_decimal = int(marked_item_bitstring, 2)

    # Input set for Grover's: a single all-zeros state, which will be transformed
    # into a uniform superposition by initialise_quantum_circuit.
    grover_input_set = np.array([[0] * n_qubits])

    # Target set for Grover's: a probability distribution with 1.0 for the marked item
    grover_target_distribution = np.zeros(search_space_size)
    grover_target_distribution[marked_item_decimal] = 1.0
    grover_target_set = np.array([grover_target_distribution])

    # --- Classical Search ---
    print("--- 1. Classical Unstructured Search ---")
    classical_index, classical_queries = classical_unstructured_search(search_space, marked_item)

    if classical_index is not None:
        print(f"Classical search found marked item at index: {classical_index}")
        print(f"Number of classical queries: {classical_queries} (O(N))")
    else:
        print("Classical search did not find the marked item.")
        print(f"Number of classical queries: {classical_queries}\n")

    # --- Evolutionary Algorithm for Grover's Search ---
    print("--- 2. Evolutionary Algorithm for Grover's Search ---")
    config = EAConfig()
    ea = EvolutionaryAlgorithm(config)

    print("Starting Evolutionary Algorithm...")
    ea.evolve_algorithm(grover_input_set, grover_target_set, num_qubits=n_qubits)
    print("Evolutionary Algorithm Finished.\n")

if __name__ == "__main__":
    main()
