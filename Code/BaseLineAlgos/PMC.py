from Algos.Classes.EdgeServer import EdgeServer
from typing import List, Set
from Algos.Classes.ED import ED
from Algos.Classes.Model import Model
from Algos.MUMS import pot_offloaders, utilized_storage
from Classes.Model import Model
import pandas as pd
from MEC.N import initialize_EDs

edge_server_data = pd.read_csv("../MEC/MUA/Dataset/site-optus-melbCBD.csv")

edge_server_lats = edge_server_data["LATITUDE"].head(5)  # Edge Server Latitude
edge_server_longs = edge_server_data["LONGITUDE"].head(5)  # Edge Server Longitude
edge_server_coords = pd.DataFrame((edge_server_lats, edge_server_longs))  # Combined coordinates

server_lat, server_long = edge_server_coords[0]  # Server Coorinates assigned
es = EdgeServer(
    20,
    800,
    1024,
    server_lat,
    server_long,
    800 #Server Range in Meters
)

def model_pot_offls(models: Set[Model], eds: List[ED]) -> List[Model]: #list returning models in order of increasing EDs
    dic = dict()

    for model in models:
        dic[model] = len(pot_offloaders(eds, model))

    list_models = sorted(dic, key=dic.get, reverse=True) #list of model in non-increasing order of number of potential offloaders
    return list_models

def PMC(es: EdgeServer, eds: List[ED]):

    """
    Practial Model Caching -> Caches Model based on Maximum EDs until either all models are cached from cloud or server storage is exhausted
    """

    # print("PMC invoked")
    demamded_models = {ed.model for ed in eds}
    # print("Demanded Models: ")
    # print({models.name for models in demamded_models})
    max_model_potoffl = model_pot_offls(demamded_models, eds)
    es.X.clear() #clear cache of already filled

    # print(es.X)
    # print("Edge Server Cache cleared")
    i=0

    while(i<len(max_model_potoffl)):

        server_storage_left = es.Storage - utilized_storage(es.X) #storage left in server
        next_model = max_model_potoffl[i] #next model in list
        occupy_storage = next_model.storage #server storage it will occupy

        if(occupy_storage <= server_storage_left): #constraint for storage accomodation
            es.X.add(next_model)
            i+=1 #advance to next model

        else: #server cannot accomodate next model, however it does not mean it cannot accomodate following models, but according to the strategy the following models are not required by as many EDs as this one so caching it will not give utility as much as caching this one as number of potential offloading devices will decrease as we move further in list.
            break

if __name__ == "__main__":
    eds = initialize_EDs(es,50)
    PMC(es,eds)
    print("Cached Models: ")
    print({models.name for models in es.X})
    print(es.Storage - utilized_storage(es.X))

