from dataclasses import dataclass
from typing import List, Set, Dict
from Algos.Classes.ED import ED
from Classes.Model import Model


@dataclass
class Temp:
    model: Model
    name: str
    storage: float
    marginal_util: float
    count_eds: int