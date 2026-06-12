from EdgeServer import EdgeServer
from ED import ED 
from typing import List, Set
from MUMS import MUMS
from SingletonUM import SUM
from ServerRA import SRA
from dataclasses import dataclass

@dataclass
class ESP:

    servers: List[EdgeServer]
    devices: List[ED] #Pehle saare device pass kardenge jo connected hain ESP se

    def SRA(NoX:List[ED], W:float, F: float):
        return SRA(NoX, W, F)
    def SUM(self, Nx: List[list: ED], W:float, F:float):
        return SUM(Nx, W, F)

    def MUMS(self, EDs: List[list: ED], J: set, W: float, F: float, S: int):
        return MUMS(EDs, J, W, F, S)
