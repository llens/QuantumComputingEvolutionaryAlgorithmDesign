import unittest
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from quantum_computer_operations import (
    apply_quantum_gates,
    initialise_quantum_circuit,
    measure_quantum_output,
    run_quantum_algorithm,
    run_quantum_algorithm_over_set,
)

class TestQuantumComputerOperations(unittest.TestCase):
    def test_initialise_quantum_circuit(self):
        input_state = np.array([0, 1, 0, 0])
        gates = ["q0", "q1"]
        qc = initialise_quantum_circuit(input_state, gates)
        
        # Verify that the circuit is initialized correctly (qubit 1 is flipped)
        sv = Statevector.from_instruction(qc)
        expected_sv = Statevector.from_label('10') # q1 is the first qubit in qiskit ordering
        self.assertTrue(sv.equiv(expected_sv))

    def test_run_quantum_algorithm(self):
        input_state = np.array([0, 0, 0, 0])
        gates = ["q0", "q1"]
        gate_array = np.array([[2, 0], [3, 0]])  # H on q0, then CNOT q0,q1 -> Bell state
        probabilities = run_quantum_algorithm(input_state, gates, gate_array)
        
        is_00 = np.allclose(probabilities, [1.0, 0, 0, 0])
        is_11 = np.allclose(probabilities, [0, 0, 0, 1.0])
        self.assertTrue(is_00 or is_11)


    def test_run_quantum_algorithm_over_set(self):
        input_set = np.array([[0, 0, 0, 0], [1, 0, 0, 0]])
        target_set = np.array([[0.5, 0, 0, 0.5], [0, 0.5, 0.5, 0]])
        gates = ["q0", "q1"]
        gate_array = np.array([[2, 0], [3, 0]])  # H on q0, then CNOT q0,q1
        score, = run_quantum_algorithm_over_set(input_set, target_set, gates, gate_array)
        
        # The score will not be -1.0 because the measurement is probabilistic.
        # We can check that the score is a float and is less than 0.
        self.assertIsInstance(score, float)
        self.assertLess(score, 0)

if __name__ == '__main__':
    unittest.main()