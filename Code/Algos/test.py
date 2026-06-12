from random import randint
from Classes.ED import ED
import numpy as np
from Classes.Model import Layers, Model
# from typing import Set, List
from MUMS import *
from Classes.ED import ED
from ServerRA import SRA

#storage is assumed to be in MBs
#computation resources for ED defined in MHz FLOPS

def layer(a:int):

    oi = [randint(10,50) for _ in range(0,a)] #Output data size of each layer in MBs
    oi.sort()
    oi.reverse()
    np.array(oi)

    fi = [randint(50,150) for _ in range (0,a)] #FLOPs
    fi.sort()
    fi.reverse()
    np.array(fi)

    return Layers(oi,fi)

# print(lm1)
# print(cm1)

mobilenet = Model(
    name="MobileNet",
    storage=250,  # MB
    layers= layer(5)
)

resnet18 = Model(
    name="ResNet18",
    storage=45.0,
    layers=Layers(
        computation_per_layer=np.array([
            5e7, 8e7, 1.2e8, 1.5e8, 1e8,
            8e7, 5e7, 3e7
        ]),
        output_of_layer=np.array([
            3e6, 2e6, 1.5e6, 1e6,
            5e5, 2e5, 5e4, 1e3
        ])
    )
)


resnet50 = Model(
    name="ResNet50",
    storage=98.0,
    layers=Layers(
        computation_per_layer=np.array([
            8e7, 1.2e8, 1.8e8, 2.5e8,
            2e8, 1.5e8, 1e8, 8e7,
            5e7, 3e7
        ]),
        output_of_layer=np.array([
            4e6, 3e6, 2e6, 1.5e6,
            1e6, 7e5, 4e5, 2e5,
            5e4, 1e3
        ])
    )
)













EDs = [

    # MobileNet users
    ED(
        local_comp_res=12,
        model=mobilenet,
        task_deadline=5,
        # local_computation_power=2,
        channel_coefficient=0.5,
        transmission_power=0.8,
        energy_consumption_param=0.5,
        transmision_antenna_power_eff_param=0.75
    ),

    ED(
        local_comp_res=1.2e9,
        model=mobilenet,
        task_deadline=700,
        # local_computation_power=2,
        channel_coefficient=1.2e-4,
        transmission_power=0.5,
        energy_consumption_param=1.1e-28,
        transmision_antenna_power_eff_param=0.80
    ),

    # ResNet18 users
    ED(
        local_comp_res=1.5e9,
        model=resnet18,
        task_deadline=1000,
        # local_computation_power=3,
        channel_coefficient=8e-5,
        transmission_power=0.6,
        energy_consumption_param=1.2e-28,
        transmision_antenna_power_eff_param=0.82
    ),

    ED(
        local_comp_res=2.2e9,
        model=resnet18,
        task_deadline=1200,
        # local_computation_power=3,
        channel_coefficient=1.5e-4,
        transmission_power=0.7,
        energy_consumption_param=1.3e-28,
        transmision_antenna_power_eff_param=0.85
    ),

    # ResNet50 users
    ED(
        local_comp_res=2.8e9,
        model=resnet50,
        task_deadline=1500,
        # local_computation_power=4,
        channel_coefficient=1.0e-4,
        transmission_power=0.8,
        energy_consumption_param=1.4e-28,
        transmision_antenna_power_eff_param=0.88
    ),

    ED(
        local_comp_res=4.0e9,
        model=resnet50,
        task_deadline=1800,
        # local_computation_power=5,
        channel_coefficient=2.0e-4,
        transmission_power=1.0,
        energy_consumption_param=1.5e-28,
        transmision_antenna_power_eff_param=0.90
    )
]

# ids = [devices.id for devices in EDs]
# print(*ids)

J = {mobilenet,resnet18,resnet50}
# print(utilized_storage(J))

# offloaders = pot_offloaders(EDs, model1)
# print(offloaders)

# print(maxutil(EDs,J))

# print([i for i in MUMS(EDs, J, 0, 0, 512)])

# cached_model = MUMS(EDs, J, 0, 0, 512)[0]
# model =  MUMS(EDs, J, 0, 0, 512)

# print(MUMS(EDs, J, 0, 0, 512))

# l = [1,2,3]
# s = {4,5,6}
# s = list(s)

# print(l+s)




#assumption - all devices pass in argument are potential


# if __name__ == '__main__':
#     UxNoX, Wi_list, Fi_list = SRA(EDs[0], 300, 500)
#     print(UxNoX)
#     print(*Wi_list)
#     print(*Fi_list)

# print(mobilenet.no_of_layers)
# print(resnet18.no_of_layers)
# print(resnet50.no_of_layers)

# def reduce(a:int):
#     global a = a-1
#     return a
# a = 69
# print(a)
# print(reduce(a))
# print(a)