#include <cstdlib>
#include "evolutionary-algorithm-parallel.h"
#include "quantum-computer.h"

int main(int argc, char ** argv)
{
	srand((unsigned)time(NULL));
	
	EvolutionarySearch evol_search;
	
	evol_search.SetDnaLength(50);
	evol_search.SetMutationRate(0.05);
	evol_search.SetGenerationSize(500);
	
	evol_search.Init();

	evol_search.Evolve(1000);
	printDna(evol_search.bestDna);
	
	return 0;
}