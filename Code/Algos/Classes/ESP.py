import EdgeServer
import ED
from typing import List, Set
from MUMS import MUMS
from SingletonUM import SUM

class ESP:

    servers: List[EdgeServer]
    devices: List[ED]

    def response(self): #gather user response
        pass

    def SRA(self):
        pass

    def SUM(self, X: set, Nx: List[ED]):
        return SUM(X, Nx)

    def MUMS(self, EDs: List[ED], J: set, W: float, F: float, S: float):
        return MUMS(EDs, J, W, F, S)
