from dataclasses import dataclass
from .Model import Model

@dataclass(frozen=True)
class ED:
    ed_counter = 0

    local_comp_res: int #computation resources FLOPS
    model: Model 
    task_deadline: int
    local_computation_power: int
    allocated_bw: float = 0
    allocated_comp_resources: float = 0
    
    @property
    def id(self) -> int: ED.ed_counter+=1; return ED.ed_counter

    '''
    #Coordinates of mobile user
    x: int
    y: int
    '''

    def local_inference_time(self, collab_infer: bool):
        if(collab_infer):
            T1 = sum(self.model.layers.computation_per_layer[:layer_partition_pt])/self.local_computation_power
        else:
            T1 = sum(self.model.layers.computation_per_layer)/self.local_computation_power
        return T1


    def offloading_decision(self):
        offloading_decisions = 0
        layer_partition_pt = 0

        pass

    def simulate_inference_delay(self):
        pass

    def change_location(self):
        pass

    def initiate_handoff(self):
        pass
