from Algos.Classes.EdgeServer import EdgeServer
from Algos.Classes.ED import ED
from typing import List, Set, Dict
from Algos.MUMS import pot_offloaders
from Algos.SingletonUM import SUM
from Classes.Model import Model
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
        temp = Temp(model,model.name,model.storage, marginal_util, pot_offls)
        list_temp.append(temp)

    return list_temp

def DynMCS(es: EdgeServer, snapshot: List[ED]):

    demanded_models = {eds.model for eds in snapshot} #set of new models demanded by eds which are currently inside Edge Server instance
    # print([models.name for models in demanded_models])
    model_potoffl = demanded_models_potoffls(demanded_models, snapshot)
    # print(model_potoffl)
    model_util_dict = model_util(es, model_potoffl) #list of models sorted in non-increasing order according to marginal utility

    temp_list: List[Temp] = fill_temp(model_potoffl, model_util_dict, snapshot) #list of temp class
    # print(temp_list)

    # 01 KNAP HERE we will use
    final_utility_list = []

    for temp in temp_list:

        # utility =  1/temp.storage + 0.3 * temp.marginal_util + 0.2 * temp.count_eds #inver. prop to storage (mathm. formula)

        # Cache Score (Benefit-to-Cost / Utility Density)
        #
        # Computes the caching priority of each model using a benefit-per-unit-storage
        # objective. The score is directly proportional to the model's demand
        # (number of requesting Edge Devices) and its marginal utility, while being
        # inversely proportional to the storage space required by the model.
        #
        #                   CountEDs × MarginalUtility
        # CacheScore = ------------------------------------
        #                      Storage
        #
        # where:
        #   CountEDs       : Number of Edge Devices requesting the model (Demand).
        #   MarginalUtility: Performance gain obtained by caching the model.
        #   Storage        : Cache space occupied by the model.
        #
        # This formulation prioritizes models that:
        #   • are requested by many Edge Devices,
        #   • provide higher computational utility,
        #   • require less cache storage.
        #
        # The metric is inspired by the classical Benefit-to-Cost (BCR) /
        # Utility Density formulation widely used in resource allocation,
        # cache placement, and knapsack-based optimization problems.
        # Since it is parameter-free, it avoids introducing arbitrary weights
        # or tuning coefficients while naturally balancing benefit against
        # limited edge cache capacity.
        #
        # Edge cases:
        #   • CountEDs <= 0        -> CacheScore = 0
        #   • MarginalUtility <= 0 -> CacheScore = 0
        #   • Storage <= 0         -> Model is considered invalid and CacheScore = 0

        if temp.storage <= 0 or temp.count_eds <= 0 or temp.marginal_util <= 0:
            utility = 0.0
        else:
            utility = (temp.count_eds * temp.marginal_util) / temp.storage


        final_utility_list.append((temp.model,utility,temp.name,temp.storage))

    final_utility_list.sort(reverse=True, key=lambda x: x[1]) #list sorted according to utility in particular
    # print(final_utility_list)

    #now we will assign the models according to utility to the edge server
    list_of_models = []
    temp_storage=es.Storage
    # print(temp_storage)
    for model, utility, model_name, storage in final_utility_list:
        if storage <= temp_storage:
            list_of_models.append(model) #taklif, yaha list me model name i.e string dal rahe model class dalna hain
            temp_storage -= storage

    # print(list_of_models)

    # Remove only models that are no longer needed
    for model in list(es.X):  # iterate over a copy
        if model not in list_of_models:
            es.X.remove(model)

    # Add only new models
    for model in list_of_models:
        if model not in es.X:
            es.X.add(model)