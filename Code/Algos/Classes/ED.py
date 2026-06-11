from dataclasses import dataclass
from .Model import Model
import numpy as np

Ic = 10**(-13) #defined gloabally, average channel coherance time

@dataclass(frozen=True)
class ED:
    ed_counter: int = 0

    local_comp_res: int #computation resources FLOPS
    model: Model 
    task_deadline: int
    local_computation_power: int
    channel_coefficient: int
    transmission_power: float
    energy_consumption_param: float
    transmision_antenna_power_eff_param: float
    
    @property
    def id(self) -> int: ED.ed_counter+=1; return ED.ed_counter

    #Coordinates of moving user, dynamically change everytime
    @property
    def x(self) -> int: self.change_location()[0]

    @property
    def y(self) -> int: self.change_location()[1]

    '''
    #Coordinates of mobile user
    x: int
    y: int
    '''

    def local_inference_time(self, di: int):
        return sum(self.model.layers.computation_per_layer[:di]) #returns local inference cose corresponding to partition layer
    
    def offloading_decision(self, wi: float, fi: float, sigma: float):
        best_partition = -1
        best_delay = float('inf') #infinity
        best_rl = 0
        best_ru = 0
        ai = 0

        #we will try every partition layer and then
        for di in range(self.model.layers):
            # local computation FLOPS
            T1 = sum(self.model.layers.computation_per_layer[:di + 1]) #eqn (5)

            # edge computation FLOPS
            T2 = sum(self.model.layers.computation_per_layer[di + 1:]) #eqn (6)

            # local inference delay
            rl = T1 / self.local_comp_res #local inference time for ED

            # edge inference delay
            if fi == 0:
                re = float('inf')
            else:
                re = T2 / fi #inference time for EDi on edge server

            # transmission rate
            rate = wi * np.log2(
                1 + (self.transmission_power * self.channel_coefficient) / (sigma + Ic)
            )

            # upload delay -> depends on ED (differ)
            if rate == 0:
                ru = float('inf')
            else:
                ru = self.model.layers.output_of_layer[di] / rate #eqn (7)

            # total collaborative delay
            total_delay = rl + re + ru

            # check deadline
            if total_delay <= self.task_deadline:
                ai = 1
                
                # choose best partition
                if total_delay < best_delay:
                    best_delay = total_delay
                    best_partition = di
                    best_rl = rl
                    best_ru = ru

        return best_partition, best_delay, best_rl, best_ru, ai


    def simulate_inference_delay(self):
        pass

    def change_location(self):
        pass

    def initiate_handoff(self):
        pass