from __future__ import annotations
import os

from Algos.Classes.EdgeServer import  EdgeServer
from MEC.N import initialize_EDs, initialize_ED_out
# edge_server_coords = pd.DataFrame((edge_server_lats,edge_server_longs)) #Combined coordinates

import pandas as pd
import random
import math

# Edge Server Coordinates (Melbourne CBD approx)
server_lat = -37.8136
server_long = 144.9631

# Create 100 users within ~300m radius
users = []

for _ in range(100):
    lat = server_lat + random.uniform(-0.002, 0.002)
    lon = server_long + random.uniform(-0.002, 0.002)
    users.append([lat, lon])

users_data = pd.DataFrame(users, columns=["LATITUDE", "LONGITUDE"])


#server ki position hardcode ki hai
server_lat = -37.8136
server_long = 144.9631

es = EdgeServer(
    20,
    800,
    1024,
    server_lat,
    server_long,
    500
)


def HaversineFormula(x1: float, y1: float, x2: float, y2: float) -> float: #returns distance b/w 2 coordinates in meters

    lat1, lon1, lat2, lon2 = map(math.radians, [x1, y1, x2, y2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))

    r = 6371.0 #radius of earth
    return c * r * 1000 #multiply with 100 to convert distance to meters


in_range_user_coords = [] #list of user coordinates within range of server
out_of_range_user_coords = [] #list of user coordinates out or range

for i in range(users_data.shape[0]-1):
    user_lat, user_long = users_data.iloc[i]
    dist = HaversineFormula(user_lat, user_long, server_lat, server_long)

    if(dist <= es.coverage_area):
        in_range_user_coords.append((user_lat, user_long))
    else:
        out_of_range_user_coords.append((user_lat, user_long))

in_range_user_coords = in_range_user_coords[:20] #list size reduces to number of test users



import math
import random
from dataclasses import replace
from typing import Iterator, Optional

from Algos.Classes.ED import ED


# ---------------------------------------------------------------------------
# Tunable defaults -- override via function args, don't hardcode-edit these
# unless you want to change the defaults for every caller.
# ---------------------------------------------------------------------------
EARTH_RADIUS_M = 6_371_000.0   # meters, matches the HaversineFormula in site script
DEFAULT_DT = 0.5               # seconds between coordinate updates (as requested)
DEFAULT_MIN_SPEED = 50.0        # m/s, slow walking pace
DEFAULT_MAX_SPEED = 100.0        # m/s, fast walk / light jog
DEFAULT_MIN_SEGMENT = 0.5      # seconds a (heading, speed) pair is held before
DEFAULT_MAX_SEGMENT = 2.5      # being redrawn -- this is T_{j+1} - T_j in the paper
MAX_TURN = math.pi / 3         # max heading change per new segment (radians)


def _meters_to_lat_long_delta(dx_north_m: float, dy_east_m: float, lat_deg: float) -> tuple[float, float]:

    d_lat = (dx_north_m / EARTH_RADIUS_M) * (180.0 / math.pi)
    d_lon = (dy_east_m / (EARTH_RADIUS_M * math.cos(math.radians(lat_deg)))) * (180.0 / math.pi)
    return d_lat, d_lon





"""

1. Random Direction Model 
 
 
Why? -> to change the eds coordinates -> dynamic scenerio create karne ke lie
How? -> step1. initial distance hoga ed ka edge server se - call it as d1 and coordinates as (x1,y1)
        step2. 






"""





def RandomDirectionModel(
    ed: ED,
    es: EdgeServer,
    duration: Optional[float] = None,
    dt: float = DEFAULT_DT,
    min_speed: float = DEFAULT_MIN_SPEED,
    max_speed: float = DEFAULT_MAX_SPEED,
    min_segment: float = DEFAULT_MIN_SEGMENT,
    max_segment: float = DEFAULT_MAX_SEGMENT,
    seed: Optional[int] = None,
) -> Iterator[ED]:


    #concept of seed
    rng = random.Random(seed)

    elapsed = 0.0
    total_time = duration if duration is not None else rng.uniform(3.0, 6.0) #seelct karega randomly ki kitne time tak ed move kar , final cordinates kya hoge after  this time === main moto




    """
    
    1. my thetha of edge server vo fix hai, humne fix kar rkha hai -> means theta also fix
    2. possibilities kya chihye aapne proj mea -> eds move kare across all the directions 
                                a. vo toh phele bhi kar rhi thi -> north east wale mea? what is different -> direction reverse!!!!!!
                                b. theta ka use karke hum direction bhi reverse kar rhe hai uske extra kuch nhi karna pad rha 
                                        for that reason humne theta ka concept use kiya
                                
                                THETA KA CONCEPT KYA HAI YHA
                                    i changed theta for every ed in such a way so that
                                    i) 40% ed towards server jaye -> means inside the coverage area they will approach
                                    ii) 40% will move away from the coverage area
                                    iii) 20% will choose randomly their way of movement
                                
                            so that we will be able to cover all the possible scenerios -> system ko dynamic bna sake
                                
    """


    choice = rng.random()
    base_theta = math.atan2(es.y - ed.y, es.x - ed.x) #edge server
    if choice < 0.4:
        # 40% move roughly toward server
        theta = base_theta + rng.uniform(-math.pi / 6, math.pi / 6)

    elif choice < 0.8:
        # 40% move roughly away
        theta = base_theta + math.pi + rng.uniform(-math.pi / 6, math.pi / 6)

    else:
        # 20% move anywhere
        theta = rng.uniform(0, 2 * math.pi)


    """
    
    
    speed = distance / time
    distance = speed * time
    
    speed yea choose btw => 50 - 100 m/s 
    
    1. while loop will -> elapsed check karega abhi iska kitna time remaining hai aur kab tak iske direc or coord change karne to get final one
    2. step choose karega randomly btw min (0.5 or the left time) 
    3. dist_m = speed * time (speed = randomly chosen between min_speed and max_speed (50-100m/s))
    4. fir us distance ko theta change karega  -> distance ko polar coordinate mea change kar rha hai
    5. convert the distance into lat, long using meter_to_lat_long_delta
    
    
    
    
    Segement ka kya concept hai
            - segment ek time hai for which the ed continue to move in the same direction for a while (until the segment finishes)
            - after the segment finished and the time is still remaining for the ed to change its coordinates so it will change its current position by a theta
            - it will create new segment means aab yea nye theta se move karga for the next segment
            
    
    in conclusion
        ed aapna speed decide karega jisse wo run karega, 
        segment decide karega ki kitne time tak us direction mea run karna hai, 
        step decide karega ka ki kitne step se move karna hai
        
        1. aur for the time total_time (let say ed choose kiya 5 sec)
        2. speed decide karunge kya hogi (let say 60 m/s)
        3. segment decide karega ( let say 2sec ) 2sec tak wo same dir mea motion karega and after seg end theta changa ed ka for the next segmebent 
                total_time = 5sec => 0-2sec (1st dir) => 2-4sec (2nd dir) => 4-5sec (3rd dir)
        4. in the end of the 5th sec we are having the final coordinates of the ed
         
    
    """

    speed = rng.uniform(min_speed, max_speed)
    segment_remaining = rng.uniform(min_segment, max_segment)

    current = ed

    while elapsed < total_time:


        step = min(dt, total_time - elapsed) #check for 0.5 or remaining time if less then 0.5 so choose step accordingly

        # advance position for this micro-step at the current (theta, speed)
        dist_m = speed * step   # (50-100 m/s rand * step)
        dx_north = dist_m * math.cos(theta)   # ED.x == latitude  == north
        dy_east = dist_m * math.sin(theta)    # ED.y == longitude == east
        d_lat, d_lon = _meters_to_lat_long_delta(dx_north, dy_east, current.x) #converting the distance into lat long

        current = replace(current, x=current.x + d_lat, y=current.y + d_lon)
        elapsed += step
        segment_remaining -= step



        #update 3->
        #yeild current ki jagah...elapsed time bhi dekh lenge
        yield current

        # time for a new relative direction / speed? (this is a T_j event)
        if segment_remaining <= 0:
            # gamma_j (eq. 26): a bounded turn rather than a full uniform
            # redraw, so the path looks like a real pedestrian/vehicle
            # track instead of reversing direction every segment.
            gamma = rng.uniform(-MAX_TURN, MAX_TURN)
            theta = (theta + gamma) % (2 * math.pi)
            speed = rng.uniform(min_speed, max_speed)
            segment_remaining = rng.uniform(min_segment, max_segment)

from MEC.J import J

if __name__ == "__main__":

    # Assign first two generated users to two EDs
    # lat1, lon1 = in_range_user_coords[0]
    # lat2, lon2 = in_range_user_coords[1]

    # eds = [
    #
    #     ED(
    #         local_comp_res=12e9, #yea mene int se float kiya hai
    #         model=models[0],
    #         task_deadline=5,
    #         channel_coefficient=0.5,
    #         transmission_power=80e-3,
    #         energy_consumption_param=0.5,
    #         transmision_antenna_power_eff_param=0.75,
    #         x=lat1,
    #         y=lon1
    #     ),
    #
    #
    #
    #
    #     ED(
    #         local_comp_res=10e9,
    #         model=models[0],
    #         task_deadline=2,
    #         channel_coefficient=0.2,
    #         transmission_power=25e-3,
    #         energy_consumption_param=0.7,
    #         transmision_antenna_power_eff_param=0.80,
    #         x=lat2,
    #         y=lon2
    #     )
    #
    # ]


    eds = initialize_EDs(es) #eds inside coverage area
    eds_out=initialize_ED_out(es) #eds outside coverage area
    ed_in_out=random.sample(eds,25)+random.sample(eds_out,25) #dono ko add kar and then shuffle -> random inside + outside coverage area
    random.shuffle(ed_in_out)

    #mark this as update 1 darshil
    # coverage_snapshots = {} #to get the snapshot of eds in the coverage area of the edge server



    for idx, ed in enumerate(ed_in_out, start=1):


        """
        
        1. mujhe har ed uski coordinates hai vo change karne hai after sometime 
           s.t. yea dynamic lge
        2. uske lihye ed_in_out list usme se iterate kar rhe hai one by one 
        3. kya kar rhe hai ? -> har ed kar after sometime coordinate change kar rhe hai
        4. threading use kar rhee hai jisme 10-10 patch [ed1,ed2,...ed10] rhega aur har kuch list eg. 50 eds - ideally 5 thread banegi
        5. return after sometime distance from edge server se [ new coordinates ]
        6. har ed ka apna ek initial distance initalized hai, initial coordinate hai....
            ed in ke liye indide mea
            ed out ke liye outside coverage area
            
            
            
        """



        # print("\n" + "=" * 60)
        # print(f"ED {idx}")

        #intial distance calc from edge server of ed
        initial_distance = HaversineFormula(
            ed.x,
            ed.y,
            es.x,
            es.y
        )

        #update 2 ->
        #current simulation time ed ka
        # current_time = round(RandomDirectionModel.DEFAULT_DT if False else 0, 1)


        # print(f"Initial Distance: {initial_distance:.2f} m")

        handoff = True

        for state in RandomDirectionModel(ed,es): #update 4-> every time after running we checking for curr time as well

            # print("ed.x =", state.x, type(ed.x))
            # print("ed.y =", state.y, type(ed.y))
            # print("es.x =", es.x, type(es.x))
            # print("es.y =", es.y, type(es.y))

            # print("Old:", state.x, state.y)

            dist = HaversineFormula(
                state.x,
                state.y,
                es.x,
                es.y
            )



            # #update 5->
            # #snapshot add kar rha hai for ed
            # #afar kuch aur details chahiye then update it from here @darshil
            # if current_time not in coverage_snapshots:
            #     coverage_snapshots[current_time] = []
            #
            # if dist <= es.coverage_area:
            #     coverage_snapshots[current_time].append({
            #         "ed_id": idx,
            #         "state": state,
            #         "distance": dist
            #     })




            # print(
            #     f"Lat={state.x:.6f}, "
            #     f"Lon={state.y:.6f}, "
            #     f"Distance={dist:.2f} m"
            # )

            if dist <= es.coverage_area:

                print(
                    f"HANDOFF REQUIRED "
                    f"(Distance={dist:.2f} m)"
                )

                handoff = False
                break

        if not handoff:
            print("ED remained inside coverage area")

        # print(sorted(coverage_snapshots.keys()))




    #let us now generalize this
    # x = len(eds)






"""

#12:00PM 07-07-2026

1. after ever 0.5 how many eds are there in the coverage are (list of the ed -> particular ed)
2. how many are doing handoff after ever 0.5 sec
3. how many are doing hand-in after ever 0.5 sec


After every 0.5s: Number of EDs handin, 
Number of Eds handoff, 
List of particular ED in form of List which are inside server area at particular instance of time

"""