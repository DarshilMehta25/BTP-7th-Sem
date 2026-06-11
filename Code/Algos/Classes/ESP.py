import EdgeServer
import ED
from typing import List, Set
from MUMS import MUMS
from SingletonUM import SUM
from ServerRA import SRA
from dataclasses import dataclass

@dataclass
class ESP:

    servers: List[EdgeServer]
    devices: List[ED] #Pehle saare device pass kardenge jo connected hain ESP se

    def response(self): #gather user response
        pass

    def SUM(self, Nx: List[ED], W:float, F:float):
        return SUM(Nx, W, F)

    def MUMS(self, EDs: List[ED], J: set, W: float, F: float, S: float):
        return MUMS(EDs, J, W, F, S)
