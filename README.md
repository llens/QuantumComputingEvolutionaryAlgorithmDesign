## QuantumComputingEvolutionaryAlgorithmDesign

# Description
A C++ program to both simulate a quantum computer and use parallel evolutionary techniques to design algorithms for it. Inspired by the ideas in the following PhD thesis, but implemented entirely originally, http://theses.ucalgary.ca/jspui/bitstream/11023/2780/3/ucalgary_2016_zahedinejad_ehsan.pdf,.

# Operation.
The algorithm maps the complete set of quantum gates T and their relative positions as a simple 'DNA', a generation of multiple random quantum algorithm 'DNA' are generated and compared to the desired output quantum state, the best members of this generation are bred (cut and joined together) and mutated (random 'DNA' changes) to create the next generation which is again evaluated.

Example of a 5-qbit algorithm 'DNA'  
![Alt text](DNA_example.png?raw=true "Optional Title")  
Gate symbol key:  
T: T  
H: Hadamard  
.- (+): CNOT  
I: Identity (Blank)

#Compilation
g++ -g -O3 -fopenmp ....
Choose either the single core or parallel version.

