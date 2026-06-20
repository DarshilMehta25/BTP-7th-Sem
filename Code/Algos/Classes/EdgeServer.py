from dataclasses import dataclass

@dataclass
class EdgeServer:
    W: int
    F: int
    Storage: int #in MB
    # noise: float
    x: float #Latitude
    y: float #Longitude
    coverage_area: float #in meters

    def MUA(self):
        pass