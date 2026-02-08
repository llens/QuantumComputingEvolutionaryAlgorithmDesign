from quantum_ea.config import EAConfig


def test_ea_config_loads_values():
    config = EAConfig()
    assert config.individual_dna_size == 30
    assert config.individual_swap_probability == 0.1
    assert config.tournament_size == 3
    assert config.population == 100
    assert config.breeding_probability == 0.5
    assert config.mutation_probability == 0.2
    assert config.generations == 200


def test_ea_config_types():
    config = EAConfig()
    assert isinstance(config.individual_dna_size, int)
    assert isinstance(config.individual_swap_probability, float)
    assert isinstance(config.tournament_size, int)
    assert isinstance(config.population, int)
    assert isinstance(config.breeding_probability, float)
    assert isinstance(config.mutation_probability, float)
    assert isinstance(config.generations, int)
