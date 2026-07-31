from Algos.Classes.EdgeServer import EdgeServer
from Algos.Classes.Model import (Model)
from Algos.Classes.ED import ED
from typing import List, Set, Dict, Tuple
from Algos.MUMS import pot_offloaders
from Algos.SingletonUM import SUM
from Temp import Temp
import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

user_coords_file_path = os.path.join(
    BASE_DIR,
    "MUA",
    "Dataset",
    "site-optus-melbCBD.csv"
)

edge_server_data = pd.read_csv(user_coords_file_path)

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

def demanded_models_potoffls(demanded_models: Set[Model], eds: List[ED]) -> Dict[Model, List[ED]]: #returns dictionary of models mapped to its potential offloaders inside Edge Server

    model_potoffl = dict()
    for model in demanded_models:
        model_potoffl[model] = list(pot_offloaders(eds,model))

    return model_potoffl

def model_util(es: EdgeServer, model_potoffl: Dict[Model, List[ED]]) -> Dict[Model, float]: #calculate marginal utility
    model_util = dict()

    for model in model_potoffl:
        # print(model)
        pot_offfls = model_potoffl[model]
        # print(pot_offfls)
        model_util[model] = SUM(pot_offfls,es.W, es.F)[0]/model.storage #calculating marginal utility per model

    # model_list = sorted(model_util, key= model_util.get, reverse=True) #list of models sorted in non-increasing order as per marginal utility

    return model_util

def fill_temp(pot_offl: Dict[Model, List[ED]], model_util_dict: Dict[Model, float], snapshot: List[ED]): #returns list of temp class
    list_temp = list()

    for model in model_util_dict:
        pot_offls = len(pot_offloaders(snapshot, model))
        marginal_util = model_util_dict[model]
        temp = Temp(model.storage, marginal_util, pot_offls)
        list_temp.append(temp)

    return list_temp


def DynMCS(es: EdgeServer, snapshot: List[ED]):
    print(snapshot)
    # handoff_eds = [eds for eds in es.EDs not in snapshot] #handed off eds jo edge server ki list me hain but snapshot mein nai
    # handin_eds = [eds for eds in snapshot not in es.EDs] #handed in eds jo edge server ki list me nai hain but snapshot main hain
    demanded_models = {eds.model for eds in snapshot} #set of new models demanded by eds which are currently inside Edge Server instance
    # print([models.name for models in demanded_models])
    model_potoffl = demanded_models_potoffls(demanded_models, snapshot)
    # print(model_potoffl)
    model_util_dict = model_util(es, model_potoffl) #list of models sorted in non-increasing order according to marginal utility

    temp_list = fill_temp(model_potoffl, model_util_dict, snapshot) #list of temp class
    print(temp_list)

# if __name__ == "__main__":
#     DisCNN(es, )
#     DynMCS(es, )