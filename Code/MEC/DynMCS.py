from Algos.Classes.EdgeServer import EdgeServer
from Algos.Classes.Model import (Model)
from Algos.Classes.ED import ED
from typing import List, Set, Dict
from Algos.MUMS import pot_offloaders
from Algos.SingletonUM import SUM

def demanded_models_potoffls(demanded_models: Set[Model], eds: List[ED]): #returns dictionary of models mapped to its potential offloaders inside Edge Server

    model_potoffl = dict()
    for model in demanded_models:
        model_potoffl[model] = list(pot_offloaders(eds,model))

    return model_potoffl

def model_util(es: EdgeServer, model_potoffl: Dict[Model, List[ED]]) -> List[Model]: #calculate marginal utility
    model_util = dict()

    for model in model_potoffl:
        model_util[model] = SUM(model_potoffl[model],es.W,es.F)/model.storage #calculating marginal utility per model

    model_list = sorted(model_util, key= model_util.get, reverse=True) #list of models sorted in non-increasing order as per marginal utility
    return model_list

    
def DynMCS(es: EdgeServer, snapshot: List[ED]):
    handoff_eds = [eds for eds in es.EDs not in snapshot] #handed off eds jo edge server ki list me hain but snapshot mein nai
    handin_eds = [eds for eds in snapshot not in es.EDs] #handed in eds jo edge server ki list me nai hain but snapshot main hain

    demanded_models = {eds.model for eds in snapshot} #set of new models demanded by eds which are currently inside Edge Server instance

    model_potoffl = demanded_models_potoffls(demanded_models, snapshot)

    model_list = model_util(es, model_potoffl) #list of models sorted in non-increasing order according to marginal utility