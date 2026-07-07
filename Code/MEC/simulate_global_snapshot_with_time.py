import os
import copy
import random
import threading
from typing import List, Dict, Tuple

import pandas as pd

from Algos.Classes.EdgeServer import EdgeServer
from Algos.Classes.ED import ED
from MEC.HaverSineFormula import HaversineFormula
from MEC.Random_Direction_Model import RandomDirectionModel
from MEC.DisCNN import DisCNN
from MEC.N import initialize_EDs, initialize_ED_out


"""

GlobalSnapshotMUA.py

problem yea tha ki DMUA.py mea xyz() function har batch (10,20,30...100 eds)
ke liye alag se MUA() call kar rha tha, aur MUA() ke andar

    coverage_snapshots.clear()

chal rha tha + har _simulate_ed thread apna khud ka curr_time = 0.0 se start
kar rha tha. matlab har batch ki apni ek chhoti simulation ban rhi thi jiska
clock hamesha 0 se restart hota tha.

isi liye output mea "Time = 0.5 ... Time = 6.0" wala block 11 baar repeat ho
rha tha - vo 11 alag alag chhoti timelines thi, ek continuous simulation
nhi thi.

Solution -> ek hi baar mea, saare EDs ko ek single global clock ke sath 
simulate karo (threading barrier use karke sabko sync mea rakhna), aur ek
hi dict banao jisme time -> [eds jo coverage ke andar hai] store ho, poori
run ke lie (0.5, 1.0, 1.5, ... max_time tak)

is file ko DMUA.py wale hi folder mea rakhna (Code/MEC/) taki relative
imports same tarike se resolve ho jaye

"""


# Edge Server setup (same as DMUA.py mea kiya tha)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

user_coords_file_path = os.path.join(
    BASE_DIR,
    "MUA",
    "Dataset",
    "site-optus-melbCBD.csv"
)

edge_server_data = pd.read_csv(user_coords_file_path)

edge_server_lats = edge_server_data["LATITUDE"].head(5)
edge_server_longs = edge_server_data["LONGITUDE"].head(5)
edge_server_coords = pd.DataFrame((edge_server_lats, edge_server_longs))

server_lat, server_long = edge_server_coords[0]
es = EdgeServer(
    20,
    800,
    1024,
    server_lat,
    server_long,
    800  # server ka range meters mea
)

NoX = DisCNN(es)  # model caching + resource allocation ke baad ke offloaders


# Single global-clock simulation -> yehi mera naya function hai

def simulate_global_coverage(
    all_eds: List[ED],
    es_ref: EdgeServer,
    dt: float = 0.5,
    max_time: float = 10.0,
) -> Tuple[Dict[float, List[int]], Dict[float, List[ED]]]:
    """

    step1. saare EDs ko ek single global clock ke sath simulate karo,
           dt (default 0.5 sec) ke gap se, max_time tak

    step2. return karega DO dicts (ek tuple ke andar) ->

           i)  global_snapshots        -> { timestamp -> [stable_id, ...] }
           ii) global_snapshots_states -> { timestamp -> [ED object, ...] }

           dono same tick, same order ke corresponding hai. ids wale se
           quick lookup / print ho jata hai, EDs wale se actual coordinates
           (x, y) ya koi bhi field chahiye ho toh mil jayega.

           yea ek genuinely continuous timeline hai, DMUA.py wale MUA()
           baar baar call karne jaisa nhi - vo toh har call pe clock hi
           restart kar deta tha (coverage_snapshots.clear() + curr_time=0)


    IMPORTANT -> ED.id use mat karna identity ke liye agar ED.py mea fix
    nhi laga hai, vo galat hai:

        purana (galat) version:
            @property
            def id(self) -> int: ED.ed_counter += 1; return ED.ed_counter

        yea koi stored per-device id nhi tha. .id read karte hi ek
        SHARED CLASS-LEVEL counter +1 ho jata tha, jo bhi value abhi
        counter ki hai vo return ho jati thi. same object ka .id do
        baar read karo toh do alag number aayenge, aur vo counter saare
        ED instances ke beech shared hai (poore process mea ek hi hai)

        isi liye pehle jo bhi "ED IDs: [...]" print hota tha usme kabhi
        bhi ek hi ED do alag timestamps pe repeat nhi hota tha - yea real
        result nhi tha device movement ka, bas property ka side-effect
        tha jisse aisa lagna hi tha

        (agar Algos/Classes/ED.py mea id fix kar diya hai - ed_counter ko
        __post_init__ mea ek hi baar assign karke - toh ab ed.id bhi
        trust kar sakte ho, but yaha bhi stable_id (list ka fixed index)
        use kar rha hu taki ED.py fix ho ya na ho, yea function hamesha
        sahi chale)


    Notes / assumptions:

    i) abhi assume kiya hai ki saare EDs t=0 pe hi move karna start karte hai. agar EDs alag alag real time pe "arrive" karte hai (jaise
      naya batch t=5s pe aata hai), toh har ED ko apna arrival_time chahiye hoga aur usse pehle wale ticks skip karne padenge - abhi
      ke liye vo cover nhi kiya hai, agar chahiye toh bata dena

    ii) ED coverage se bahar chala jaye tab bhi vo move karta rhega, wapis andar aa sakta hai baad mea - jaise original per-tick check mea
      hota tha. sirf tab rukega jab uska generator khatam ho jaye (StopIteration) ya koi exception aaye - us case mea vo "inactive"
      mark ho jayega but baaki threads ka barrier sync nhi tootega

    iii) duration=max_time explicitly RandomDirectionModel ko diya hai taki har ED poori simulation tak move karta rahe, warna vo apna khud ka
      random 3-6 sec ka lifetime lekar beech mea hi ruk jata (jo
      RandomDirectionModel ka default hai jab duration nhi diya jaye)

    """

    n = len(all_eds)
    if n == 0:
        return {}, {}

    # step2. har ED ko ek fixed, stable identity de rahe hai (uska index
    # hi id ban gaya) - yea ED.id ke bharose nhi hai, khud independent hai
    stable_ids = list(range(1, n + 1))

    n_steps = int(round(max_time / dt))

    # step3. har ED ka apna generator bana rahe hai, duration=max_time
    # explicitly de rahe hai taki beech mea khud se na ruk jaye
    generators = [
        RandomDirectionModel(ed, es_ref, duration=max_time, dt=dt)
        for ed in all_eds
    ]

    active = [True] * n  # kis ED ka generator abhi bhi chalu hai

    # tick_result[idx] = (coverage ke andar hai kya, uska stable_id, moved ed)
    tick_result = [(False, None, None)] * n

    # step4. do barriers use kar rahe hai -> ek "sabko ek sath chalao" ke
    # liye, ek "sabka is tick ka kaam khatam hua" confirm karne ke liye
    step_barrier = threading.Barrier(n + 1)
    done_barrier = threading.Barrier(n + 1)

    def worker(idx: int):
        gen = generators[idx]
        sid = stable_ids[idx]

        for _ in range(n_steps):
            step_barrier.wait()  # yaha ruka rahega jab tak "go" signal na mile

            if active[idx]:
                try:
                    state = next(gen)  # ED ka naya (moved) copy is tick ka
                    dist = HaversineFormula(state.x, state.y, es_ref.x, es_ref.y)
                    inside = dist <= es_ref.coverage_area

                    if inside:
                        tick_result[idx] = (True, sid, state)
                    else:
                        tick_result[idx] = (False, None, None)

                except StopIteration:
                    # is ED ka movement khatam ho gaya, ab aage kuch nhi
                    active[idx] = False
                    tick_result[idx] = (False, None, None)

                except Exception:
                    # koi bhi aur error aaye toh bhi baaki threads ka
                    # barrier atakna nhi chahiye - isliye yaha bhi bas
                    # inactive mark kar rahe hai, aage nhi bhej rahe
                    active[idx] = False
                    tick_result[idx] = (False, None, None)
            else:
                tick_result[idx] = (False, None, None)

            done_barrier.wait()  # bata do "mera is tick ka kaam ho gaya"

    threads = [threading.Thread(target=worker, args=(i,), daemon=True) for i in range(n)]
    for t in threads:
        t.start()

    global_snapshots: Dict[float, List[int]] = {}
    global_snapshots_states: Dict[float, List[ED]] = {}

    # step5. main thread yaha har tick ko release karega aur result collect karega
    for step in range(1, n_steps + 1):
        t_stamp = round(step * dt, 2)

        step_barrier.wait()  # ab sabko is tick ke lie chalne do
        done_barrier.wait()  # sabka kaam khatam hone ka wait karo

        inside_ids = [sid for (inside, sid, _state) in tick_result if inside]
        inside_states = [state for (inside, _sid, state) in tick_result if inside]

        global_snapshots[t_stamp] = inside_ids
        global_snapshots_states[t_stamp] = inside_states

    for t in threads:
        t.join()

    # step6. dono dicts ko tuple mea return kar rahe hai - koi function
    # attribute wala hack nhi, seedha proper return, dono dict clean
    # rehte hai aur function dobara call karne pe overwrite nhi hote
    return global_snapshots, global_snapshots_states




# Runner -> yaha se sab chalu hoga

def run(max_time: float = 10.0, dt: float = 0.5):

    # step1. saare EDs le lo - jo NoX (offloaders, andar wale) hai + jo
    # bahar (out of range) hai unko bhi mila do, phir shuffle kar do
    all_eds = NoX + initialize_ED_out(es)
    random.shuffle(all_eds)

    print(f"Total EDs = {len(all_eds)}")

    # step2. deepcopy isliye taki original NoX / es data corrupt na ho
    eds = copy.deepcopy(all_eds)
    es_copy = copy.deepcopy(es)

    # step3. ab single global clock wali simulation chalao -> ab dono
    # milenge, ids wala dict aur ED objects wala dict, saath mea
    snapshots, snapshot_states = simulate_global_coverage(
        eds, es_copy, dt=dt, max_time=max_time
    )

    # step4. print kar do result (ids + coordinates dono)
    print_snapshots(snapshots, snapshot_states)

    return snapshots, snapshot_states






#yhe se dekh lena agar aur kuch chiye toh @darshil

def print_snapshots(
    snapshots: Dict[float, List[int]],
    snapshot_states: Dict[float, List[ED]] = None,
) -> None:
    # bas print karne ka kaam
    for t in sorted(snapshots):
        print(f"\n========== Time = {t:.1f} sec ==========")
        print(f"Number of EDs inside = {len(snapshots[t])}")
        print("ED inside the coverage area (ids):", snapshots[t])

        # agar ED objects bhi diye hai toh unke coordinates bhi dikha do
        if snapshot_states is not None:
            coords = [(ed.x, ed.y) for ed in snapshot_states[t]]






if __name__ == "__main__":
    run()