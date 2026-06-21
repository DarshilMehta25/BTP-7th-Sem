from Algos.SingletonUM import SUM
from test2 import EDs, models
from MUMS import MUMS

# if __name__ == '__main__':
#     UxSUM, conformed_off=SingletonUM.SUM(test2.EDs, 20e6, 800e9)
#     print("running sum.......")
#     print(UxSUM)
#     for i in conformed_off:
#         print(i.id)

if __name__ == "__main__" :
    X, NxO, UxNxO = MUMS(EDs, models, 20, 800, 1024)
    for i in X:
        print(i.name, " ", i.storage, " ", i.layers)
    for i in NxO:
        print(i.id," ",i.model.name," ",i.local_comp_res)
    print(UxNxO)