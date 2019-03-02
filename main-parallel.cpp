#include "evolutionary-algorithm-parallel.h"
#include "quantum-computer.h"
#include "main.h"

VectorXi convertVectorToEigen(vector<int> vec) {
	return Map<VectorXi>(
		&vec[vec.size()],
		 vec.size(),
		  vec.size());
}

int main(int argc, char ** argv)
{
	srand((unsigned)time(NULL));
	
	EvolutionarySearch evol_search;
	
	evol_search.SetDnaLength(100);
	evol_search.SetMutationRate(0.05);
	evol_search.SetGenerationSize(50);
	
	evol_search.Init();

	evol_search.Evolve(1000);
	VectorXi bestDna_e = convertVectorToEigen(evol_search.bestDna);
	printDna(bestDna_e);
	
	return 0;
}