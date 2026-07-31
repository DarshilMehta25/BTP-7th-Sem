from dataclasses import dataclass,field
from typing import List, Set, Dict
from Algos.Classes.ED import ED

@dataclass
class Temp:
    storage: float
    marginal_util: float
    count_eds: int