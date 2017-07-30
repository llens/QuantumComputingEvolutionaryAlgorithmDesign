# Description
Uses evolutionary algorithms and python-quintuple to automatically design quantum computing algorithms. The algorithm maps the complete set of quantum gates T, Hadamard, CNOT, and their relative positions as a simple 'DNA', a generation of multiple random quantum algorithm 'DNA' are generated and compared to the desired output quantum state, the best members of this generation are bred (cut and joined together) and mutated (random 'DNA' changes) to create the next generation which is again evaluated.

# Current stage.
Working version for 2-bit quantum computer currently expanding to 5-bit to use the full capabilities of the IBM Quantum Experience.
