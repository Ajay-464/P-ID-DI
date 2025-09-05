from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class Equipment:
    tag: str
    type: str
    connections: Dict[str, str]

@dataclass
class PID_Data:
    equipment: List[Equipment]
