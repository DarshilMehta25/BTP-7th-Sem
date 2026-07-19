from dataclasses import dataclass, field
from typing import Set
from Algos.Classes.Model import Model

@dataclass
class EdgeServer:

    W: int
    F: int
    Storage: int #in MB

    x: float #Latitude
    y: float #Longitude

    coverage_area: float #in meters

    Utility: float = 0.0 #Utility due to all offloaders maximizing utility connected to Edge Server

    X: Set[Model] = field(default_factory=set) #set of cached models

    def MUA(self):
        pass