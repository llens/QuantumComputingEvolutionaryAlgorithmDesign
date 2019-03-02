#ifndef EVOLUTIONARY_ALGORITHM
#define EVOLUTIONARY_ALGORITHM

#include <vector>
#include "quantum-computer.h"
#include "quantum-test-generator.h"

using namespace std;

class EvolutionarySearch {
	static const int geneNum = 4;
	public:
	int dnaLength;
	int mutationRate;
	int generationSize;
	double bestScore;
	vector<int> bestDna;
	vector< vector<int> > generation;
	vector<double> scores;
	QuantumComputer quant_comp;
	QuantumTestGenerator quant_test;
	
	void SetDnaLength (int);
	void SetMutationRate (int);
	void SetGenerationSize (int);
	vector<int> GenerateDna ();
	void Init ();
	void EvaluateGeneration ();
	double Reward (vector<int>);
	void InsertInGeneration (vector<int>, double);
	vector<int> Breed (vector<int>, vector<int>);
	void BreedGeneration ();
	void ScoreDna (vector<int>);
	void Evolve (int);
	void PrintGeneration (int);
};

#endif