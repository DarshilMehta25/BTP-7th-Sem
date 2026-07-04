from __future__ import annotations
import os

from Algos.Classes.EdgeServer import  EdgeServer
from MEC.N import initialize_EDs
# from MEC.MUA.test import in_range_user_coords
# import pandas as pd
from random import randint
import math
from Algos.Classes.ED import ED

# #Base file addresses
# edge_server_coords_file_path = "./Dataset/site-optus-melbCBD.csv"
# user_coords_file_path = "./Dataset/users-melbcbd-generated.csv"
#
# edge_server_data = pd.read_csv(filepath_or_buffer=edge_server_coords_file_path)
# users_data = pd.read_csv(filepath_or_buffer=user_coords_file_path) #Already in DF format just have to filter coordinates with server range
#
# edge_server_lats = edge_server_data["LATITUDE"].head(5) #Edge Server Latitude
# edge_server_longs = edge_server_data["LONGITUDE"].head(5) #Edge Server Longitude
# edge_server_coords = pd.DataFrame((edge_server_lats,edge_server_longs)) #Combined coordinates

import pandas as pd
import random

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

# print(users_data)
# print(*edge_server_lats)
# print(*edge_server_longs)
# print(edge_server_coords)

# server_lat, server_long = edge_server_coords[0] #Server Coorinates assigned
# es = EdgeServer(20,800,1024,server_lat,server_long,500) #coverage area kept 500meters can be changed later as per server configuration
















es = EdgeServer(
    20,
    800,
    1024,
    server_lat,
    server_long,
    500
)




















# print(es)
# print(es.coverage_area)
# print(server_lat)
# print(server_long)

def HaversineFormula(x1: float, y1: float, x2: float, y2: float) -> float: #returns distance b/w 2 coordinates in meters

    lat1, lon1, lat2, lon2 = map(math.radians, [x1, y1, x2, y2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))

    r = 6371.0 #radius of earth
    return c * r * 1000 #multiply with 100 to convert distance to meters


# print(user_lat, user_long)
# print(users_data.iloc[0])
# print(users_data.shape[0])

in_range_user_coords = [] #list of user coordinates within range of server
out_of_range_user_coords = [] #list of user coordinates out or range

for i in range(users_data.shape[0]-1):
    user_lat, user_long = users_data.iloc[i]
    dist = HaversineFormula(user_lat, user_long, server_lat, server_long)

    if(dist <= es.coverage_area):
        in_range_user_coords.append((user_lat, user_long))
    else:
        out_of_range_user_coords.append((user_lat, user_long))

# print(*in_range_user_coords)
# print(*out_of_range_user_coords)

# print(len(in_range_user_coords))
in_range_user_coords = in_range_user_coords[:20] #list size reduces to number of test users
# print(len(in_range_user_coords))

# Flow
# Make a function of random direction where once ED is passed, its coordinates change such that it goes out of range of server within (change every 0.5 sec -> coordinates)
# 3-6(task deadline) seconds to simulate mobile users
# No need to pass user coordinates as it is device position independent
# For using subset of users slice the ED list
# Make ED instances here from ED class
# ED ke instance idhar banadena as per requirement jo bhi attribute dalne ho dal dena abhi coordinates change karne se kaam hain
# This function does not return any value just change user coordinates
# Replace function use karke ED ko har ek baar pura replicate kar na hoga cuz attributes once defined are freezed

# def RandomDirectionModel(ed: ED):
#
#
#
#     pass










"""
random_direction.py

Random Direction Mobility Model (RDM) for mobile Edge Devices (ED), based on:

    P. Nain, D. Towsley, B. Liu, Z. Liu, "Properties of Random Direction Models"

Movement pattern (Sec. II of the paper, generalized to 2D in Sec. IV):

    * At time T_j a new relative direction gamma_j and a new speed s_j are drawn.
    * The absolute heading evolves additively (eq. 26):
          theta_j = (theta_{j-1} + gamma_j) mod 2*pi
    * Position evolves at constant speed during [T_j, T_{j+1}) (eq. 28):
          X(t) = X(T_j) + s_j * (t - T_j) * (cos theta_j, sin theta_j)

ADAPTATION NOTE: the paper bounds the mobile to [0,1) or [0,1)^2 and handles
boundary hits via wrap-around (Sec II-A / IV-A) or reflection (Sec II-B / IV-B).
That doesn't apply here -- EDs roam a real, unbounded lat/long plane around a
fixed EdgeServer, and we *want* them to be able to leave the coverage circle
so `initiate_handoff()` has something to react to. So no boundary handling is
implemented; if you later want EDs confined to a bounding box, the wrap-around/
reflection formulas (eq. 4/6 in the paper) can be folded in on top of this.

ED is a frozen dataclass, so nothing is mutated in place. Each simulated step
produces a brand-new ED via dataclasses.replace(), and RandomDirectionModel is
a *generator* -- it yields a new ED every `dt` seconds. The caller drives the
loop and decides what to do with each state (store the trajectory, check
distance to an EdgeServer, trigger initiate_handoff(), etc).




"""

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
    """
    Convert a local-plane displacement in meters (north, east) into a
    (delta_latitude, delta_longitude) offset in degrees, evaluated at the
    given latitude (small-displacement approximation, same scale used by
    a Haversine-based distance check).
    """
    d_lat = (dx_north_m / EARTH_RADIUS_M) * (180.0 / math.pi)
    d_lon = (dy_east_m / (EARTH_RADIUS_M * math.cos(math.radians(lat_deg)))) * (180.0 / math.pi)
    return d_lat, d_lon


def RandomDirectionModel(
    ed: ED,
    # es: EdgeServer,
    duration: Optional[float] = None,
    dt: float = DEFAULT_DT,
    min_speed: float = DEFAULT_MIN_SPEED,
    max_speed: float = DEFAULT_MAX_SPEED,
    min_segment: float = DEFAULT_MIN_SEGMENT,
    max_segment: float = DEFAULT_MAX_SEGMENT,
    seed: Optional[int] = None,
) -> Iterator[ED]:
    """
    Random Direction mobility generator for a single ED.

    Yields a brand-new ED every `dt` seconds with updated (x, y) =
    (latitude, longitude), for `duration` seconds of simulated time.

    Parameters
    ----------
    ed : ED
        Starting state of the device (must already carry x, y).
    duration : float, optional
        Total simulated time in seconds. Defaults to a random value in
        [3, 6) seconds, matching the "3-6 second" test window you noted.
    dt : float
        Coordinate-update granularity in seconds (default 0.5s).
    min_speed, max_speed : float
        Speed range (m/s) redrawn at each new movement segment.
    min_segment, max_segment : float
        How long (seconds) a (heading, speed) pair is held before a new
        one is drawn -- T_{j+1} - T_j in the paper's notation.
    seed : int, optional
        Seed for a reproducible trajectory (handy for tests).

    Yields
    ------
    ED
        A new ED instance per dt-step, identical to the input except for
        updated x (latitude) and y (longitude).
    """
    rng = random.Random(seed)

    elapsed = 0.0
    total_time = duration if duration is not None else rng.uniform(3.0, 6.0)

    # theta_0 drawn uniformly in [0, 2*pi) -- matches the paper's stationary
    # result (Prop. 4.1): start the device "already mixed" in heading.
    # move initially away from server
    #
    # print(type(ed.x)," ",ed.x)
    # print(type(ed.y)," ",ed.y)

    north = ed.x - server_lat
    # north = ed.x - es.x
    # east = ed.y - es.y
    east = ed.y - server_long

    theta = math.atan2(east, north)
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


    for idx, ed in enumerate(eds, start=1):

        # print("\n" + "=" * 60)
        # print(f"ED {idx}")


        initial_distance = HaversineFormula(
            ed.x,
            ed.y,
            es.x,
            es.y
        )

        # print(f"Initial Distance: {initial_distance:.2f} m")

        handoff = False

        for state in RandomDirectionModel(ed):

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

            if dist > es.coverage_area:

                print(
                    f"HANDOFF REQUIRED "
                    f"(Distance={dist:.2f} m)"
                )

                handoff = True
                break

        if not handoff:
            print("ED remained inside coverage area")




    #let us now generalize this
    # x = len(eds)
