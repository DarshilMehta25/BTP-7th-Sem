from dataclasses import dataclass
import numpy as np

@dataclass(frozen=True)
class Layers:
    output_of_layer: np.ndarray #Output size of each layer
    computation_per_layer: np.ndarray #In FLOPS

    def __hash__(self):
        return hash((tuple(self.computation_per_layer), tuple(self.output_of_layer)))

@dataclass(frozen=True)
class Model:
    name: str
    layers: Layers
    storage: float

    @property
    def no_of_layers(self) -> int: return len(self.layers.output_of_layers)

    def __hash__(self):
        return hash((self.name, self.layers))

    @property
    def no_of_layers(self) -> int: return len(self.layers.computation_per_layer)