#include <iostream>
#include <vector>
#include <cstdlib>
#include <algorithm>
#include <cstring>
#include <climits>
#include <list>
#include <omp.h>
#include "evolutionary-algorithm.h"
#include "quantum-computer.h"
#include "quantum-test-generator.h"

using namespace std;

struct ParallelGenerationData {
	vector< vector<int> > generation;
	vector<double> scores;
};

ParallelGenerationData insertInGeneration (ParallelGenerationData pData, vector<int> dna, double score) {
	vector<double>::iterator it = lower_bound(pData.scores.begin(), pData.scores.end(), score);
	int index = distance(pData.scores.begin(), it);
	if (pData.scores.size() == 0) {
		pData.scores.push_back(score);
	} else {
		pData.scores.insert(it, score);
	}
	
	if (pData.generation.size() < 1) {
		pData.generation.push_back(dna);
	} else {
		pData.generation.insert(pData.generation.begin() + index, dna);
	}
	return pData;
}

double reward (vector<int> dna) {
	double reward = 0;
	int num_bits = 5;
	int input_iter = 100;

	QuantumComputer* quant_comp = new QuantumComputer();
	QuantumTestGenerator* quant_test = new QuantumTestGenerator();
	
	quant_comp -> SetNumQBits(num_bits);
	quant_test ->Init(num_bits);
	int i = 0;
	while (i < input_iter) {
		quant_test -> Next();
		quant_comp -> InputStates(quant_test -> input);
		quant_comp -> ApplyAlgorithm(dna);
		for (unsigned int j = 0; j < quant_comp -> states.size(); j++) {
			reward -= abs(quant_comp -> states[i] - quant_test -> output[i]);
		}
		i++;
	}

	delete quant_comp;
	delete quant_test;

	return reward;
}

ParallelGenerationData scoreDna (vector<int> dna, ParallelGenerationData pData) {
	double rwrd = reward(dna);
	return insertInGeneration(pData, dna, rwrd);
}	

void EvolutionarySearch::SetDnaLength (int len) {
	dnaLength = len;
}

void EvolutionarySearch::SetMutationRate (int mtr) {
	mutationRate = mtr;
}

void EvolutionarySearch::SetGenerationSize (int genSize) {
	generationSize = genSize;
}

vector<int> EvolutionarySearch::GenerateDna () {
	vector<int> dna;
	for (int i = 0; i < dnaLength; i++) {
		int a = rand() % geneNum;
		dna.push_back(a);
	}
	return dna;
}

void EvolutionarySearch::Init () {
	bestScore = -1E10;
	int i = 0;
	while (i < generationSize) {
		vector<int> dna = GenerateDna();
		ScoreDna(dna);
		i++;
	}
}

void EvolutionarySearch::EvaluateGeneration () {
	vector< vector<int> > unorderedGeneration;
	unorderedGeneration = generation;
	generation.clear();
	scores.clear();

	vector<ParallelGenerationData> loopGeneration;

	#pragma omp parallel
	{	
		float id = omp_get_thread_num();
		float total = omp_get_num_threads();
		float factor = generationSize / total;
		ParallelGenerationData pData;
		for (int i = factor * id; i < factor * (id +1); i++) {
			pData = scoreDna(unorderedGeneration[i], pData);
		}
		#pragma omp critical
		{
			loopGeneration.push_back(pData);
		}
	}
	
	for (int i = 0; i < loopGeneration.size(); i++) {
		for (int j = 0; j < loopGeneration[i].scores.size(); j++) {
			InsertInGeneration(loopGeneration[i].generation[j], loopGeneration[i].scores[j]);
		}
	}
}

void EvolutionarySearch::BreedGeneration () {
	for (int i = 0; i < (generationSize / 2); i++) {
		unsigned int j = generation.size() - i - 1;
		int a = rand() % generation.size();
		generation[i] = Breed(generation[j], generation[a]);
	}
}

vector<int> EvolutionarySearch::Breed (vector<int> dna_a, vector<int> dna_b) {
	for (unsigned int i = 0; i < dna_a.size(); i++)
	{	
		int a = rand() % 2;
		int b = rand() % INT_MAX;
		if (a == 1) {
			dna_a[i] = dna_b[i];
		}
		if (b < mutationRate * INT_MAX) {
			dna_a[i] = rand() % geneNum;
		}
	}
	return dna_a;
}

void EvolutionarySearch::InsertInGeneration (vector<int> dna, double score) {
	vector<double>::iterator it = lower_bound(scores.begin(), scores.end(), score);
	int index = distance(scores.begin(), it);
	if (scores.size() == 0) {
		scores.push_back(score);
	} else {
		scores.insert(it, score);
	}
	
	if (generation.size() < 1) {
		generation.push_back(dna);
	} else {
		generation.insert(generation.begin() + index, dna);
	}
}

void EvolutionarySearch::Evolve(int iter) {
	int i = 0;
	while (i < iter) {
		BreedGeneration();
		EvaluateGeneration();
		PrintGeneration(i);
		i++;
	}
}

void EvolutionarySearch::ScoreDna (vector<int> dna) {
	double reward = Reward(dna);
	if (reward > bestScore) {
		bestScore = reward;
		bestDna = dna;
	}
	InsertInGeneration(dna, reward);
}

double EvolutionarySearch::Reward (vector<int> dna) {
	double reward = 0;
	int num_bits = 5;
	int input_iter = 10;
	
	quant_comp.SetNumQBits(num_bits);
	quant_test.Init(num_bits);
	int i = 0;
	while (i < input_iter) {
		quant_test.Next();
		quant_comp.InputStates(quant_test.input);
		quant_comp.ApplyAlgorithm(dna);
		for (unsigned int j = 0; j < quant_comp.states.size(); j++) {
			reward -= abs(quant_comp.states[i] - quant_test.output[i]);
		}
		i++;
	};

	return reward;
}

void EvolutionarySearch::PrintGeneration(int i) {
	cout << i << '\t' << scores[0] << '\t' << scores[scores.size() - 1] << endl;
}
