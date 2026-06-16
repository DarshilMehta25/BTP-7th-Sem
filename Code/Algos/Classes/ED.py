from dataclasses import dataclass
from .Model import Model
import numpy as np

Ic = 10**(-13) #defined gloabally, average channel coherance time

@dataclass(frozen=True)
class ED:

    local_comp_res: int #computation resources FLOPS #fli
    model: Model #Xi
    task_deadline: int #in  milli seconds #ti
    channel_coefficient: float #hi
    transmission_power: float #pi
    energy_consumption_param: float #kil
    transmision_antenna_power_eff_param: float #Bi #in milli watts

    ed_counter: int = 0
    
    @property
    def id(self) -> int: ED.ed_counter+=1; return ED.ed_counter

    #Coordinates of moving user, dynamically change everytime
    # @property
    # def x(self) -> int: self.change_location()[0]

    # @property
    # def y(self) -> int: self.change_location()[1]

    '''
    #Coordinates of mobile user
    x: int
    y: int
    '''

    def local_inference_time(self): #ril
        return sum(self.model.layers.computation_per_layer[:])

    def collab_local_inference_time(self, di: int): #ril(di)
        return sum(self.model.layers.computation_per_layer[:di]) #returns local inference cose corresponding to partition layer
    
    def offloading_decision(self, wi: float, fi: float, sigma: float):

        best_partition = -1
        best_delay = float('inf') #infinity
        best_rl = 0
        best_ru = 0
        # min_pi = float("inf")
        ai = 0

        # transmission rate
        rate = wi * np.log2(
                1 + (self.transmission_power * self.channel_coefficient) / (sigma + Ic)
            )
        
        #we will try every partition layer and then
        for di in range(self.model.no_of_layers):
            # local computation FLOPS
            # print(f"For layer {di}")
            T1 = self.collab_local_inference_time(di) #eqn (5)
            # print(T1)

            # edge computation FLOPS
            T2 = sum(self.model.layers.computation_per_layer[di + 1:]) #eqn (6)
            # print(T2)

            # local inference delay
            rl = T1 / self.local_comp_res #local inference time for ED

            # edge inference delay
            if fi == 0:
                re = float('inf')
            else:
                re = T2 / fi #inference time for EDi on edge server

            # upload delay -> depends on ED (differ)
            if rate == 0:
                ru = float('inf')
            else:
                ru = self.model.layers.output_of_layer[di] / rate #eqn (7)
                # print(f"ru {ru}")

            # total collaborative delay
            total_delay = rl + re + ru
            # print(f"total_delay: {total_delay}")

            # check deadline
            if total_delay <= self.task_deadline:
                ai = 1

                # choose best partition
                if total_delay < best_delay:
                    best_delay = total_delay
                    best_partition = di
                    best_rl = rl
                    best_ru = ru
            


        return best_partition,best_rl, best_ru, ai


    def simulate_inference_delay(self):
        pass

    def change_location(self):
        pass

    def initiate_handoff(self):
        pass