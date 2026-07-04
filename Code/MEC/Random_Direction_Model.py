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

    rng = random.Random(seed)

    elapsed = 0.0
    total_time = duration if duration is not None else rng.uniform(3.0, 6.0)







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











    speed = rng.uniform(min_speed, max_speed)
    segment_remaining = rng.uniform(min_segment, max_segment)

    current = ed

    while elapsed < total_time:
        step = min(dt, total_time - elapsed)

        # advance position for this micro-step at the current (theta, speed)
        dist_m = speed * step
        dx_north = dist_m * math.cos(theta)   # ED.x == latitude  == north
        dy_east = dist_m * math.sin(theta)    # ED.y == longitude == east
        d_lat, d_lon = _meters_to_lat_long_delta(dx_north, dy_east, current.x)

        current = replace(current, x=current.x + d_lat, y=current.y + d_lon)
        elapsed += step
        segment_remaining -= step

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


    eds = initialize_EDs(es)
    eds_out=initialize_ED_out(es)
    ed_in_out=random.sample(eds,25)+random.sample(eds_out,25)
    random.shuffle(ed_in_out)


    for idx, ed in enumerate(ed_in_out, start=1):

        # print("\n" + "=" * 60)
        # print(f"ED {idx}")


        initial_distance = HaversineFormula(
            ed.x,
            ed.y,
            es.x,
            es.y
        )

        # print(f"Initial Distance: {initial_distance:.2f} m")

        handoff = True

        for state in RandomDirectionModel(ed,es):

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




    #let us now generalize this
    # x = len(eds)
