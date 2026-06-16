from dataclasses import dataclass

@dataclass
class EdgeServer:
    W: int
    F: int
    Storage: int
    # noise: float
    # x: int
    # y: int
    # coverage_area: float

    def simulate_collab_inference_time(self):
        pass

    def MUA(self):
        pass