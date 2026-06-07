from random import randint
from Classes.ED import ED
import numpy as np
from Classes.Model import Layers, Model
# from typing import Set, List
from MUMS import *
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


model1 = Model("VGG-16",layer(16) , 250)
model2 = Model("VGG-19", layer(19), 270)
model3 = Model("ResNet-50",layer(50) , 298)
model4 = Model("ResNet-18", layer(18), 224)
model5 = Model("ResNet-34", layer(34), 260)

ed1 = ED(100, model1)
ed2 = ED(60, model2)
ed3 = ED(100, model2)
ed4 = ED(200, model2)
ed5 = ED(40, model4)
ed6 = ED(50, model4)
ed7 = ED(80, model5)
ed8 = ED(120, model5)
ed9 = ED(150, model2)
ed10 = ED(20, model1)

EDs = [ed1, ed2, ed3, ed4, ed5, ed6, ed7, ed8, ed9, ed10]

# ids = [devices.id for devices in EDs]
# print(*ids)

J = set([model1, model2, model3, model4, model5])
# print(utilized_storage(J))

# offloaders = pot_offloaders(EDs, model1)
# print(offloaders)

# print(maxutil(EDs,J))

print([i for i in MUMS(EDs, J, 0, 0, 512)])
# print(MUMS(EDs, J, 0, 0, 512))

# l = [1,2,3]
# s = {4,5,6}
# s = list(s)

# print(l+s)