from dataclasses import dataclass

@dataclass
class EdgeServer:

    W: int
    F: int
    Storage: int #in MB

    x: float #Latitude
    y: float #Longitude

    coverage_area: float #in meters

    Utility: float = 0.0 #Utility due to all offloaders maximizing utility connected to Edge Server

    def MUA(self):
        pass