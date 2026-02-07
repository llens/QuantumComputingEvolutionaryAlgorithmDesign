import unittest
from QuantumRegister import QuantumRegister
from QuantumRegisterSet import QuantumRegisterSet

class TestQuantumRegisterSet(unittest.TestCase):
    def setUp(self):
        self.q0 = QuantumRegister("q0")
        self.q1 = QuantumRegister("q1")
        self.q2 = QuantumRegister("q2")

    def test_init(self):
        qrs = QuantumRegisterSet([self.q0, self.q1])
        self.assertEqual(qrs.size(), 2)
        # Test that duplicate registers are not added
        qrs_dup = QuantumRegisterSet([self.q0, self.q1, self.q0])
        self.assertEqual(qrs_dup.size(), 2)

    def test_size(self):
        qrs = QuantumRegisterSet([self.q0, self.q1, self.q2])
        self.assertEqual(qrs.size(), 3)
        qrs_empty = QuantumRegisterSet([])
        self.assertEqual(qrs_empty.size(), 0)

    def test_intersection(self):
        qrs1 = QuantumRegisterSet([self.q0, self.q1])
        qrs2 = QuantumRegisterSet([self.q1, self.q2])
        intersection_qrs = qrs1.intersection(qrs2)
        self.assertEqual(intersection_qrs.size(), 1)
        self.assertIn(self.q1.name, intersection_qrs.registers)

        # Test intersection with no common elements
        qrs3 = QuantumRegisterSet([self.q0])
        qrs4 = QuantumRegisterSet([self.q2])
        intersection_qrs_none = qrs3.intersection(qrs4)
        self.assertEqual(intersection_qrs_none.size(), 0)

        # Test intersection with self
        intersection_qrs_self = qrs1.intersection(qrs1)
        self.assertEqual(intersection_qrs_self.size(), 2)

if __name__ == '__main__':
    unittest.main()