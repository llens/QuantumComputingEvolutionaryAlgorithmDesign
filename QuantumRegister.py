
from __future__ import annotations
import numpy as np
from typing import List, Optional

class QuantumRegister:
    def __init__(self, name: str, size: int = 1):
        self.name = name
        self.size = size

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.name == other.name and self.size == other.size
