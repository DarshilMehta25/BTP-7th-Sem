from dataclasses import dataclass

@dataclass
class EdgeServer:
    W: int
    F: int
    Storage: int #in MB
    # noise: float
    # x: int
    # y: int
    coverage_area: float #in meters

    def MUA(self):
        pass