from Classes.EdgeServer import EdgeServer
from Classes.ED import ED
from typing import List

import os,sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
# print(sys.path)
from MUMS import MUMS
from SingletonUM import SUM
from ServerRA import SRA
from dataclasses import dataclass

@dataclass
class ESP:

    servers: List[EdgeServer]
    
    def SRA(self,NoX:List[ED], es: EdgeServer):
        return SRA(NoX, es)
        
    def SUM(self, Nx: List[ED], W:float, F:float):
        return SUM(Nx, W, F)

    def MUMS(self, EDs: List[ED], J: set, es: EdgeServer):
        return MUMS(EDs, J, es)
