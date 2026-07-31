# from __future__ import annotations
from dataclasses import dataclass, field
from typing import Set, List
from Algos.Classes.Model import Model
from Algos.Classes.ED import ED

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
    EDs: List[ED] = field(default_factory=list) #list of connected devices at any instant

    # def MUA(self):
    #     pass