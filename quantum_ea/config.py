import configparser
from pathlib import Path


class EAConfig:
    individual_dna_size: int
    individual_swap_probability: float
    tournament_size: int
    population: int
    breeding_probability: float
    mutation_probability: float
    generations: int

    def __init__(self, config_path: Path = None):
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config.ini"

        parser = configparser.ConfigParser()
        parser.read(config_path)

        section = "EvolutionaryAlgorithm"
        self.individual_dna_size = int(parser.get(section, "INDIVIDUAL_DNA_SIZE"))
        self.individual_swap_probability = float(parser.get(section, "INDIVIDUAL_SWAP_PROBABILITY"))
        self.tournament_size = int(parser.get(section, "TOURNAMENT_SIZE"))
        self.population = int(parser.get(section, "POPULATION"))
        self.breeding_probability = float(parser.get(section, "BREEDING_PROBABILITY"))
        self.mutation_probability = float(parser.get(section, "MUTATION_PROBABILITY"))
        self.generations = int(parser.get(section, "GENERATIONS"))
