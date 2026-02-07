
import numpy as np
from qiskit import QuantumCircuit, transpile, ClassicalRegister
from qiskit_aer import AerSimulator
from qiskit.quantum_info import Statevector

class Gate:
    # Qiskit gates will be applied directly in the QuantumComputer class
    pass

class State:
    @staticmethod
    def state_from_string(qubit_state_string):
        num_qubits = len(qubit_state_string)
        state_vector = np.zeros(2**num_qubits, dtype=int)
        index = int(qubit_state_string, 2)
        state_vector[index] = 1
        return state_vector

class QuantumRegister:
    def __init__(self, name, size=1):
        self.name = name
        self.size = size

class QuantumRegisterSet:
    def __init__(self, registers):
        self.registers = {r.name: r for r in registers}

    def get_register(self, name):
        return self.registers.get(name)

class QuantumComputer:
    def __init__(self, num_qubits=5):
        self.num_qubits = num_qubits
        self.circuit = QuantumCircuit(num_qubits)
        self.simulator = AerSimulator()

    def apply_gate(self, gate_name, target_qubit):
        if hasattr(self.circuit, gate_name):
            getattr(self.circuit, gate_name)(target_qubit)
        else:
            raise AttributeError(f"Gate '{gate_name}' not found in Qiskit.")

    def apply_two_qubit_gate_CNOT(self, control_qubit, target_qubit):
        self.circuit.cx(control_qubit, target_qubit)

    def measure(self, qubit, cbit=None):
        if cbit is None:
            cbit = qubit
        # Ensure the classical bit exists
        if self.circuit.num_clbits == 0:
            self.circuit.add_register(ClassicalRegister(self.num_qubits))
        self.circuit.measure(qubit, cbit)
    
    def get_state(self):
        # Create a copy of the circuit to avoid adding operations to the main circuit
        temp_circuit = self.circuit.copy()
        temp_circuit.save_statevector()
        result = self.simulator.run(temp_circuit).result()
        return result.get_statevector(temp_circuit)

    def run(self, shots=1024):
        compiled_circuit = transpile(self.circuit, self.simulator)
        job = self.simulator.run(compiled_circuit, shots=shots)
        result = job.result()
        return result.get_counts(compiled_circuit)

    def reset(self):
        self.circuit = QuantumCircuit(self.num_qubits)
        
    def probabilities_equal(self, name, prob, atol=1e-8):
        # This is a simplified implementation. 
        # A full implementation would require mapping the qubit names to indices 
        # and comparing the probabilities of the resulting statevector.
        statevector = self.get_state()
        probabilities = np.abs(statevector.data)**2
        return np.allclose(probabilities, prob, atol=atol)

    def qubit_states_equal(self, name, state, atol=1e-8):
        # This is a simplified implementation.
        # A full implementation would require mapping the qubit names to indices
        # and comparing the statevector.
        statevector = self.get_state()
        return np.allclose(statevector.data, state, atol=atol)

    def bloch_coords_equal(self, name, coords, atol=1e-8):
        # Qiskit does not directly provide Bloch coordinates for multi-qubit states.
        # This would require calculating the expectation values of Pauli operators.
        # This is a placeholder implementation.
        return False
