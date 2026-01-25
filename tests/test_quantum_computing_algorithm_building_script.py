import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the parent directory to the sys.path to allow imports from the project root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from quantum_computing_algorithm_building_script import run_algorithm
from target_generation import ExampleType # Import ExampleType

class TestQuantumComputingAlgorithmBuildingScript(unittest.TestCase):

    @patch('quantum_computing_algorithm_building_script.setup_example_problem')
    @patch('quantum_computing_algorithm_building_script.EvolutionaryAlgorithm')
    @patch('quantum_computing_algorithm_building_script.Config')
    def test_run_algorithm(self, MockConfig, MockEvolutionaryAlgorithm, MockSetupExampleProblem):
        # Mock Config to return a dummy instance
        mock_config_instance = MagicMock()
        MockConfig.return_value = mock_config_instance

        # Mock setup_example_problem to return dummy input_set and targets
        MockSetupExampleProblem.return_value = (MagicMock(), MagicMock())

        # Mock EvolutionaryAlgorithm and its evolve_algorithm method
        mock_ea_instance = MagicMock()
        MockEvolutionaryAlgorithm.return_value = mock_ea_instance

        # Call the function to be tested
        run_algorithm()

        # Assert that Config was instantiated
        MockConfig.assert_called_once()

        # Assert that setup_example_problem was called with expected arguments
        MockSetupExampleProblem.assert_called_once_with(
            ExampleType.Fourier, # Use the actual Enum member
            ["q0", "q1", "q2"],
            10
        )

        # Assert that EvolutionaryAlgorithm was instantiated with the mocked config
        MockEvolutionaryAlgorithm.assert_called_once_with(mock_config_instance)

        # Assert that evolve_algorithm was called with the correct arguments
        mock_ea_instance.evolve_algorithm.assert_called_once_with(
            MockSetupExampleProblem.return_value[0], # mocked input_set
            MockSetupExampleProblem.return_value[1], # mocked targets
            ["q0", "q1", "q2"]
        )

if __name__ == '__main__':
    unittest.main()
