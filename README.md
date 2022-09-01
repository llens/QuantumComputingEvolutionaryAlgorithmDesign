## QuantumComputingEvolutionaryAlgorithmDesign

# Description
Uses evolutionary algorithms and python-quintuple to automatically design quantum computing algorithms. Inspired by the ideas in the following PhD thesis, but implemented entirely originally, http://theses.ucalgary.ca/jspui/bitstream/11023/2780/3/ucalgary_2016_zahedinejad_ehsan.pdf.
The Quantum Computer implementation itself is from this project https://github.com/corbett/QuantumComputing, the file QuantumComputer.py, is unmodified in any way from the original.

# Operation.
The algorithm maps the complete set of quantum gates T, Hadamard, CNOT, and their relative positions as a simple 'DNA', a generation of multiple random quantum algorithm 'DNA' are generated and compared to the desired output quantum state, the best members of this generation are bred (cut and joined together) and mutated (random 'DNA' changes) to create the next generation which is again evaluated.

Gate symbol key:  
T: T  
H: Hadamard  
.- (+): CNOT  
I: Identity (Blank)

# Inputs and Targets
The required inputs and outputs for an algorithm are supplied as a series of probabilities, for instance a 2 qbit inversion gate could have the following inputs [[0, 0], [0, 1], [1, 0], [1, 1]] and following outputs [[1, 1], [1, 0], [0, 1], [0, 0]]. 

# Scoring 
Score = (-1 - mean square error) / (1 + number of blank rows)  
Scoring is based on the absolute difference from the target probability and output probability of generated individual, divided by the number of possible eigenstates, this is then divided by the number of blank rows to promote simple algorithms. Python DEAP aims to minimise a negative score.
