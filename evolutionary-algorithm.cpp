#include <iostream>
#include <vector>
#include <cstdlib>
#include <climits>
#include "evolutionary-algorithm.h"
#include "quantum-test-generator.h"

void EvolutionarySearch::SetDnaLength (int len) {
	dnaLength = len;
}

void EvolutionarySearch::SetMutationRate (double mtr) {
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

	vector<int> vec;
	for (int i = 0; i < generationSize; i++) {
		for (int j = 0; j < dnaLength; j++) {
			vec.push_back(generation[i][j]);	
		}
		unorderedGeneration.push_back(vec);
		vec.clear();
	}
	generation.clear();
	scores.clear();
	for (int i = 0; i < generationSize; i++) {
		ScoreDna(unorderedGeneration[i]);
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

void EvolutionarySearch::PrintGeneration(int i) {
	cout << i << '\t' << scores[0] << '\t' << scores[scores.size() - 1] << endl;
}

double EvolutionarySearch::Reward (vector<int> dna) {
	VectorXcd distance;
	double reward = 0;
	int num_bits = 5;
	int input_iter = 100;
	Map<VectorXi> dna_e(dna.data(), dna.size());
	
	quant_comp.SetNumQBits(num_bits);
	quant_test.Init(num_bits);
	int i = 0;
	while (i < input_iter) {
		quant_test.Next();
		quant_test.input.normalize();
		quant_comp.states = quant_test.input;
		quant_comp.ApplyAlgorithm(dna_e);
		distance = quant_comp.states - quant_test.output;
		reward += distance.norm();
		i++;
	}

	return reward;
}
