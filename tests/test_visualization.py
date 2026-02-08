from quantum_ea.visualization import quantum_gate_output_switch
from quantum_ea.gates import GateType


def test_identity_symbol():
    assert quantum_gate_output_switch(GateType.IDENTITY) == '|'


def test_t_gate_symbol():
    assert quantum_gate_output_switch(GateType.T_GATE) == 'T'


def test_hadamard_symbol():
    assert quantum_gate_output_switch(GateType.HADAMARD) == 'H'


def test_cnot_down_symbol():
    assert quantum_gate_output_switch(GateType.CNOT_DOWN) == '. - (+)'


def test_cnot_up_symbol():
    assert quantum_gate_output_switch(GateType.CNOT_UP) == '(+) - .'
