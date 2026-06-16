from random import randint
<<<<<<< HEAD
from Algos.Classes.ED import ED
import numpy as np
from Algos.Classes.Model import Layers, Model
# from typing import Set, List
from Algos.MUMS import *
from Algos.Classes.ED import ED
from Algos.ServerRA import SRA
from Algos.SingletonUM import SUM
=======
from Classes.ED import ED
import numpy as np
from Classes.Model import Layers, Model
# from typing import Set, List
from MUMS import *
from Classes.ED import ED
from ServerRA import SRA
from SingletonUM import SUM
>>>>>>> 57098279b8d8c16bd1b326f527733df340d21a7e

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

# ids = [devices.id for devices in EDs]
# print(*ids)

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

# result = SUM(EDs, 20e6, 800e9)

# total_utility = result[0]
# offloaders = result[1]

# print(total_utility)
# for device in offloaders:
#     print(device.id)