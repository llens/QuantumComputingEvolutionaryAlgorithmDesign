
import unittest
import numpy as np
from QuantumComputer import QuantumComputer, State

class TestQuantumComputer(unittest.TestCase):
    def setUp(self):
        self.qc = QuantumComputer(num_qubits=2)

    def test_apply_gate(self):
        self.qc.apply_gate('h', 0)
        state = self.qc.get_state()
        # The state should be |+>
        expected_state = np.array([1/np.sqrt(2), 1/np.sqrt(2), 0, 0])
        self.assertTrue(np.allclose(state.data, expected_state))

    def test_apply_two_qubit_gate_CNOT(self):
        self.qc.apply_gate('h', 0)
        self.qc.apply_two_qubit_gate_CNOT(0, 1)
        state = self.qc.get_state()
        # The state should be the Bell state |Φ+>
        expected_state = np.array([1/np.sqrt(2), 0, 0, 1/np.sqrt(2)])
        self.assertTrue(np.allclose(state.data, expected_state))

    def test_measure(self):
        self.qc.apply_gate('h', 0)
        self.qc.measure(0, 0)
        counts = self.qc.run(shots=1024)
        # The counts should be approximately equal for '0' and '1'
        self.assertIn('00', counts)
        self.assertIn('01', counts)
        self.assertEqual(sum(counts.values()), 1024)

    def test_reset(self):
        self.qc.apply_gate('h', 0)
        self.qc.reset()
        state = self.qc.get_state()
        expected_state = np.array([1, 0, 0, 0])
        self.assertTrue(np.allclose(state.data, expected_state))

if __name__ == '__main__':
    unittest.main()
