from QuantumComputer import QuantumComputer, Programs, State, Gate, QuantumRegister, Probability, StateNotSeparableException
import numpy as np
from unittest.mock import patch
import pytest
import unittest # Import unittest for TestCase

class TestStateMethods(unittest.TestCase):
    def setUp(self):
        self.two_qubits_00=np.kron(State.zero_state,State.zero_state)
        self.two_qubits_01=np.kron(State.zero_state,State.one_state)
        self.two_qubits_10=np.kron(State.one_state,State.zero_state)
        self.two_qubits_11=np.kron(State.one_state,State.one_state)

        self.three_qubits_000=np.kron(self.two_qubits_00,State.zero_state)
        self.three_qubits_001=np.kron(self.two_qubits_00,State.one_state)
        self.three_qubits_010=np.kron(self.two_qubits_01,State.zero_state)
        self.three_qubits_011=np.kron(self.two_qubits_01,State.one_state)
        self.three_qubits_100=np.kron(self.two_qubits_10,State.zero_state)
        self.three_qubits_101=np.kron(self.two_qubits_10,State.one_state)
        self.three_qubits_110=np.kron(self.two_qubits_11,State.zero_state)
        self.three_qubits_111=np.kron(self.two_qubits_11,State.one_state)

        self.four_qubits_0000=np.kron(self.three_qubits_000,State.zero_state)
        self.four_qubits_0001=np.kron(self.three_qubits_000,State.one_state)
        self.four_qubits_0010=np.kron(self.three_qubits_001,State.zero_state)
        self.four_qubits_0011=np.kron(self.three_qubits_001,State.one_state)
        self.four_qubits_0100=np.kron(self.three_qubits_010,State.zero_state)
        self.four_qubits_0101=np.kron(self.three_qubits_010,State.one_state)
        self.four_qubits_0110=np.kron(self.three_qubits_011,State.zero_state)
        self.four_qubits_0111=np.kron(self.three_qubits_011,State.one_state)
        self.four_qubits_1000=np.kron(self.three_qubits_100,State.zero_state)
        self.four_qubits_1001=np.kron(self.three_qubits_100,State.one_state)
        self.four_qubits_1010=np.kron(self.three_qubits_101,State.zero_state)
        self.four_qubits_1011=np.kron(self.three_qubits_101,State.one_state)
        self.four_qubits_1100=np.kron(self.three_qubits_110,State.zero_state)
        self.four_qubits_1101=np.kron(self.three_qubits_110,State.one_state)
        self.four_qubits_1110=np.kron(self.three_qubits_111,State.zero_state)
        self.four_qubits_1111=np.kron(self.three_qubits_111,State.one_state)

        self.five_qubits_00000=np.kron(self.four_qubits_0000,State.zero_state)
        self.five_qubits_00001=np.kron(self.four_qubits_0000,State.one_state)
        self.five_qubits_00010=np.kron(self.four_qubits_0001,State.zero_state)
        self.five_qubits_00011=np.kron(self.four_qubits_0001,State.one_state)
        self.five_qubits_00100=np.kron(self.four_qubits_0010,State.zero_state)
        self.five_qubits_00101=np.kron(self.four_qubits_0010,State.one_state)
        self.five_qubits_00110=np.kron(self.four_qubits_0011,State.zero_state)
        self.five_qubits_00111=np.kron(self.four_qubits_0011,State.one_state)
        self.five_qubits_01000=np.kron(self.four_qubits_0100,State.zero_state)
        self.five_qubits_01001=np.kron(self.four_qubits_0100,State.one_state)
        self.five_qubits_01010=np.kron(self.four_qubits_0101,State.zero_state)
        self.five_qubits_01011=np.kron(self.four_qubits_0101,State.one_state)
        self.five_qubits_01100=np.kron(self.four_qubits_0110,State.zero_state)
        self.five_qubits_01101=np.kron(self.four_qubits_0110,State.one_state)
        self.five_qubits_01110=np.kron(self.four_qubits_0111,State.zero_state)
        self.five_qubits_01111=np.kron(self.four_qubits_0111,State.one_state)
        self.five_qubits_10000=np.kron(self.four_qubits_1000,State.zero_state)
        self.five_qubits_10001=np.kron(self.four_qubits_1000,State.one_state)
        self.five_qubits_10010=np.kron(self.four_qubits_1001,State.zero_state)
        self.five_qubits_10011=np.kron(self.four_qubits_1001,State.one_state)
        self.five_qubits_10100=np.kron(self.four_qubits_1010,State.zero_state)
        self.five_qubits_10101=np.kron(self.four_qubits_1010,State.one_state)
        self.five_qubits_10110=np.kron(self.four_qubits_1011,State.zero_state)
        self.five_qubits_10111=np.kron(self.four_qubits_1011,State.one_state)
        self.five_qubits_11000=np.kron(self.four_qubits_1100,State.zero_state)
        self.five_qubits_11001=np.kron(self.four_qubits_1100,State.one_state)
        self.five_qubits_11010=np.kron(self.four_qubits_1101,State.zero_state)
        self.five_qubits_11011=np.kron(self.four_qubits_1101,State.one_state)
        self.five_qubits_11100=np.kron(self.four_qubits_1110,State.zero_state)
        self.five_qubits_11101=np.kron(self.four_qubits_1110,State.one_state)
        self.five_qubits_11110=np.kron(self.four_qubits_1111,State.zero_state)
        self.five_qubits_11111=np.kron(self.four_qubits_1111,State.one_state)

    def test_separate_state_non_computational_basis(self):
        plus_plus_state = np.kron(State.plus_state, State.plus_state)
        separated = State.separate_state(plus_plus_state)
        self.assertEqual(len(separated), 2)
        self.assertTrue(np.allclose(separated[0], State.plus_state))
        self.assertTrue(np.allclose(separated[1], State.plus_state))

    def test_separate_state_entangled_raises_exception(self):
        with self.assertRaises(StateNotSeparableException):
            State.separate_state(State.bell_state)

    def test_get_first_qubit(self):
        zero_one_state = np.kron(State.zero_state, State.one_state)
        first_qubit = State.get_first_qubit(zero_one_state)
        self.assertTrue(np.allclose(first_qubit, State.zero_state))

    def test_get_second_qubit(self):
        zero_one_state = np.kron(State.zero_state, State.one_state)
        second_qubit = State.get_second_qubit(zero_one_state)
        self.assertTrue(np.allclose(second_qubit, State.one_state))

    def test_get_third_qubit(self):
        zero_zero_one_state = np.kron(State.zero_state, np.kron(State.zero_state, State.one_state))
        third_qubit = State.get_third_qubit(zero_zero_one_state)
        self.assertTrue(np.allclose(third_qubit, State.one_state))

    def test_get_fourth_qubit(self):
        state_0001 = np.kron(np.kron(State.zero_state, State.zero_state), np.kron(State.zero_state, State.one_state))
        fourth_qubit = State.get_fourth_qubit(state_0001)
        self.assertTrue(np.allclose(fourth_qubit, State.one_state))

    def test_get_fifth_qubit(self):
        state_00001 = np.kron(np.kron(np.kron(State.zero_state, State.zero_state), np.kron(State.zero_state, State.zero_state)), State.one_state)
        fifth_qubit = State.get_fifth_qubit(state_00001)
        self.assertTrue(np.allclose(fifth_qubit, State.one_state))

    def test_string_from_state_raises_exception_for_non_computational_basis(self):
        plus_state = State.plus_state
        with self.assertRaises(StateNotSeparableException):
            State.string_from_state(plus_state)

    def test_string_from_state_computational_basis(self):
        # Test with a single qubit
        self.assertEqual(State.string_from_state(State.zero_state), '0')
        self.assertEqual(State.string_from_state(State.one_state), '1')
        # Test with multiple qubits (e.g., |01>)
        self.assertEqual(State.string_from_state(self.two_qubits_01), '01')
        self.assertEqual(State.string_from_state(self.three_qubits_110), '110')
        self.assertEqual(State.string_from_state(self.five_qubits_10101), '10101')

    def test_change_to_w_basis(self):
        zero_state = State.zero_state
        expected_state = Gate.H @ Gate.T @ Gate.H @ Gate.S @ zero_state
        transformed_state = State.change_to_w_basis(zero_state)
        self.assertTrue(np.allclose(transformed_state, expected_state))

    def test_change_to_v_basis(self):
        one_state = State.one_state
        expected_state = Gate.H @ Gate.Tdagger @ Gate.H @ Gate.S @ one_state
        transformed_state = State.change_to_v_basis(one_state)
        self.assertTrue(np.allclose(transformed_state, expected_state))

    def test_state_get_bloch_precision(self):
        # Directly test State.get_bloch for known states
        self.assertTrue(np.allclose(State.get_bloch(State.plus_state), np.array((1.0, 0.0, 0.0)), atol=1e-3))
        self.assertTrue(np.allclose(State.get_bloch(State.zero_state), np.array((0.0, 0.0, 1.0)), atol=1e-3))

    def test_is_fully_separable_true(self):
        # A simple separable state, e.g., |0>
        separable_state = State.zero_state
        self.assertTrue(State.is_fully_separable(separable_state))
        # A multi-qubit separable state in computational basis, e.g., |01>
        multi_qubit_separable = np.kron(State.zero_state, State.one_state)
        self.assertTrue(State.is_fully_separable(multi_qubit_separable))

    def test_is_fully_separable_false(self):
        # An entangled state, e.g., Bell state, should return False
        entangled_state = State.bell_state
        self.assertFalse(State.is_fully_separable(entangled_state))
        # A separable state not in computational basis, e.g. |+>|+>
        plus_plus_state = np.kron(State.plus_state, State.plus_state)
        self.assertFalse(State.is_fully_separable(plus_plus_state))


class TestQuantumComputerMethods(unittest.TestCase):
    def setUp(self):
        self.qc = QuantumComputer()

    def test_execute_cnot(self):
        self.qc.execute(Programs.program_test_cnot.code)
        self.assertTrue(self.qc.qubit_states_equal("q0,q1,q2,q3,q4", State.state_from_string("01100")))

    def test_reset(self):
        self.qc.apply_gate(Gate.X, "q0")
        self.assertTrue(self.qc.qubit_states_equal("q0", State.one_state))
        self.qc.reset()
        self.assertTrue(self.qc.qubit_states_equal("q0", State.zero_state))

    def test_get_ordering(self):
        self.assertEqual(self.qc.get_ordering(), [0, 1, 2, 3, 4])

    def test_is_in_canonical_ordering(self):
        self.assertTrue(self.qc.is_in_canonical_ordering())

    def test_get_requested_state_order_single_qubit(self):
        self.qc.apply_gate(Gate.X, "q0")
        state = self.qc.get_requested_state_order("q0")
        # Expected state for all 5 qubits, with q0 as 1 and others as 0
        expected_state = np.kron(State.one_state, np.kron(State.zero_state, np.kron(State.zero_state, np.kron(State.zero_state, State.zero_state))))
        self.assertTrue(np.allclose(state, expected_state))

    def test_get_requested_state_order_multiple_qubits(self):
        self.qc.apply_gate(Gate.X, "q0")
        self.qc.apply_gate(Gate.X, "q1")
        state = self.qc.get_requested_state_order("q0,q1")
        # Expected state for all 5 qubits, with q0 and q1 as 1 and others as 0
        expected_state = np.kron(State.one_state, np.kron(State.one_state, np.kron(State.zero_state, np.kron(State.zero_state, State.zero_state))))
        self.assertTrue(np.allclose(state, expected_state))

    def test_get_requested_state_order_entangled_qubits(self):
        self.qc.execute(Programs.program_test_cnot.code) # This makes q1 and q2 entangled, q0 is X-ed, so 11000
        state = self.qc.get_requested_state_order("q1,q2")
        # Expected state for q1 and q2 after CNOT, others are 0
        # The actual state of the quantum computer after program_test_cnot is 01100
        expected_state = np.kron(State.zero_state, np.kron(State.one_state, np.kron(State.one_state, np.kron(State.zero_state, State.zero_state))))
        self.assertTrue(np.allclose(state, expected_state))

    def test_probabilities_equal(self):
        self.qc.apply_gate(Gate.H, "q0")
        self.assertTrue(self.qc.probabilities_equal("q0", Probability.get_probabilities(State.plus_state)))

    def test_bloch_coords_equal(self):
        self.qc.bloch("q0")
        self.assertTrue(self.qc.bloch_coords_equal("q0", (0, 0, 1)))

    def test_measure(self):
        self.qc.apply_gate(Gate.X, "q0")
        self.qc.measure("q0")
        self.assertTrue(self.qc.qubit_states_equal("q0", State.one_state))

    def test_execute_blue_state(self):
        self.qc.execute(Programs.program_blue_state.code)
        blue_state = Gate.H @ Gate.S @ Gate.T @ Gate.H @ Gate.T @ Gate.H @ Gate.S @ Gate.T @ Gate.H @ Gate.T @ Gate.H @ Gate.T @ Gate.H @ State.zero_state
        self.assertTrue(self.qc.bloch_coords_equal("q1", State.get_bloch(blue_state)))

    def test_execute_xyz_measure(self):
        self.qc.execute(Programs.program_test_XYZMeasureIdSdagTdag.code)
        self.assertTrue(self.qc.qubit_states_equal("q0", State.zero_state))
        self.assertTrue(self.qc.qubit_states_equal("q1", State.one_state))
        self.assertTrue(self.qc.qubit_states_equal("q2", State.one_state))
        self.assertTrue(self.qc.qubit_states_equal("q3", State.zero_state))
        self.assertTrue(self.qc.qubit_states_equal("q4", State.one_state))

    def test_apply_two_qubit_gate_CNOT_separate_qubits_becomes_entangled(self):
        self.qc.apply_gate(Gate.X, "q0")
        self.qc.apply_two_qubit_gate_CNOT("q0", "q1")
        self.assertTrue(self.qc.qubit_states_equal("q0,q1,q2,q3,q4", State.state_from_string("11000")))
        q0 = self.qc.qubits.get_quantum_register_containing("q0")
        self.assertTrue(q0.is_entangled())

    def test_apply_two_qubit_gate_CNOT_already_entangled(self):
        self.qc.execute("h q[0]; cx q[0], q[1];")  # Creates a Bell state, entangling q0 and q1
        q0_reg = self.qc.qubits.get_quantum_register_containing("q0")
        q1_reg = self.qc.qubits.get_quantum_register_containing("q1")

        # Now apply another CNOT between already entangled q0 and q1 (control q0, target q1)
        self.qc.apply_two_qubit_gate_CNOT("q0", "q1")

        # Expect the state to be 1/sqrt(2) * (|00> + |10>) for q0,q1 and |000> for q2,q3,q4
        expected_state_q0q1 = 1/np.sqrt(2) * (np.kron(State.zero_state, State.zero_state) + np.kron(State.one_state, State.zero_state))
        full_expected_state = np.kron(expected_state_q0q1, np.kron(State.zero_state, np.kron(State.zero_state, State.zero_state)))
        self.assertTrue(np.allclose(self.qc.qubit_states_equal("q0,q1,q2,q3,q4", full_expected_state), True))

    def test_entangle_quantum_registers_already_entangled_groups(self):
        self.qc.execute("h q[0]; cx q[0], q[1];")  # q0 and q1 entangled
        self.qc.execute("h q[2]; cx q[2], q[3];")  # q2 and q3 entangled

        # Now entangle q1 (part of q0-q1 group) and q2 (part of q2-q3 group)
        q1_reg = self.qc.qubits.get_quantum_register_containing("q1")
        q2_reg = self.qc.qubits.get_quantum_register_containing("q2")
        self.qc.qubits.entangle_quantum_registers(q1_reg, q2_reg)

        # All four q0,q1,q2,q3 should now be in one entangled group
        # Check that q0 (which was part of the first group) is now entangled
        q0_reg_after_entangle = self.qc.qubits.get_quantum_register_containing("q0")
        self.assertTrue(q0_reg_after_entangle.is_entangled())
        # Check that the number of qubits in this entangled group is 4
        self.assertEqual(q0_reg_after_entangle.get_num_qubits(), 4)

    def test_pretty_print_probabilities_two_qubit_state(self):
        import sys
        from io import StringIO
        two_qubit_state = np.kron(State.zero_state, State.zero_state) # |00> state
        expected_output_part = "<state>=" # The exact value might vary due to floating point, but the string should be there

        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            Probability.pretty_print_probabilities(two_qubit_state)
            output = mock_stdout.getvalue()
            self.assertIn(expected_output_part, output)

    def test_explicit_expectation_x(self):
        # State.plus_state in X-basis is |0>, so expectation_x should be 1
        self.assertAlmostEqual(Probability.expectation_x(State.plus_state), 1.0)
        # State.minus_state in X-basis is |1>, so expectation_x should be -1
        self.assertAlmostEqual(Probability.expectation_x(State.minus_state), -1.0)
        # A superposition like State.zero_state in X-basis is 1/sqrt(2)(|0>+|1>), so expectation_x should be 0
        self.assertAlmostEqual(Probability.expectation_x(State.zero_state), 0.0)

    def test_explicit_expectation_y(self):
        # State.plusi_state in Y-basis is |0>, so expectation_y should be 1
        self.assertAlmostEqual(Probability.expectation_y(State.plusi_state), 1.0)
        # State.minusi_state in Y-basis is |1>, so expectation_y should be -1
        self.assertAlmostEqual(Probability.expectation_y(State.minusi_state), -1.0)
        # A superposition like State.zero_state in Y-basis is 1/sqrt(2)(|0> + i|1>), so expectation_y should be 0
        self.assertAlmostEqual(Probability.expectation_y(State.zero_state), 0.0)

    def test_num_qubits_invalid_shape_not_power_of_2(self):
        # Create a state with a dimension that is not a power of 2, e.g., 3x1
        invalid_state = np.array([[1], [0], [0]])
        with self.assertRaisesRegex(Exception, "unrecognized state shape - state dimension is not a power of 2"):
            QuantumRegister.num_qubits(invalid_state)

    def test_num_qubits_invalid_shape_not_column_vector(self):
        # Create a state with more than 5 qubits (e.g., 6 qubits, dimension 2^6 = 64)
        # Using a 64x1 matrix to represent a 6-qubit state
        invalid_state = np.zeros((64, 1))
        invalid_state[0, 0] = 1 # Set one element to 1 for a valid state representation
        with self.assertRaisesRegex(Exception, "unrecognized state shape"):
            QuantumRegister.num_qubits(invalid_state)

    def test_probabilities_equal_else_branch(self):
        self.qc.reset()
        self.qc.apply_gate(Gate.H, "q0") # q0 is |+>
        expected_probabilities = [0.0] * 32
        expected_probabilities[0] = 0.5 # for |00000>
        expected_probabilities[16] = 0.5 # for |10000>
        self.assertTrue(self.qc.probabilities_equal("q0,q2", expected_probabilities))

    def test_qubit_states_equal_raises_exception_for_non_increasing_order(self):
        self.qc.reset()
        with self.assertRaisesRegex(Exception, "at this time, requested qubits must be in increasing order"):
            self.qc.qubit_states_equal("q1,q0", State.zero_state) # Passing a dummy state

    def test_qubit_states_equal_else_branch(self):
        self.qc.reset()
        self.qc.apply_gate(Gate.X, "q0") # q0 is |1>
        # q1, q2, q3, q4 are |0>
        
        # Combined state for all 5 qubits: |10000>
        expected_state = np.kron(State.one_state, np.kron(State.zero_state, np.kron(State.zero_state, np.kron(State.zero_state, State.zero_state))))

        # Calling qubit_states_equal for "q0,q2" should trigger the else branch
        # because the current system is in canonical ordering and q0,q2 is not a single entangled group,
        # and it will combine the states of all 5 qubits.
        self.assertTrue(self.qc.qubit_states_equal("q0,q2", expected_state))

    def test_get_quantum_register_containing_raises_exception(self):
        qc = QuantumComputer()
        with self.assertRaisesRegex(Exception, "qubit q5 not found in"):
            qc.qubits.get_quantum_register_containing("q5")



if __name__ == '__main__':
    unittest.main()
