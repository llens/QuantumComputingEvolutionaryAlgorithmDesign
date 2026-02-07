from QuantumRegister import QuantumRegister
class QuantumRegisterSet:
    """A collection of QuantumRegisters, accessible by name."""
    def __init__(self, registers):
        self.registers = {r.name: r for r in registers}

    def intersection(self, other_set):
        """Returns the intersection of two QuantumRegisterSets."""
        intersection_names = self.registers.keys() & other_set.registers.keys()
        return QuantumRegisterSet([self.registers[name] for name in intersection_names])

    def size(self):
        """Returns the number of registers in the set."""
        return len(self.registers)
