from Algos.Classes.EdgeServer import  EdgeServer
import pandas as pd
# from random import randint
import math
from MEC import N
import random
from Algos.Classes.ED import ED
from typing import Iterator, Optional
from dataclasses import replace

edge_server_coords_file_path = "./Dataset/site-optus-melbCBD.csv"
user_coords_file_path = "./Dataset/users-melbcbd-generated.csv"

edge_server_data = pd.read_csv(filepath_or_buffer=edge_server_coords_file_path)
users_data = pd.read_csv(filepath_or_buffer=user_coords_file_path) #Already in DF format just have to filter coordinates with server range

edge_server_lats = edge_server_data["LATITUDE"].head(5) #Edge Server Latitude
edge_server_longs = edge_server_data["LONGITUDE"].head(5) #Edge Server Longitude
edge_server_coords = pd.DataFrame((edge_server_lats,edge_server_longs)) #Combined coordinates

server_lat, server_long = edge_server_coords[0] #Server Coorinates assigned
es = EdgeServer(20,800,1024,server_lat,server_long,500) #coverage area kept 500meters can be changed later as per server configuration

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

EARTH_RADIUS_M = 6_371_000.0   # meters, matches the HaversineFormula in site script
DEFAULT_DT = 0.5               # seconds between coordinate updates (as requested)
DEFAULT_MIN_SPEED = 50.0        # m/s, slow walking pace
DEFAULT_MAX_SPEED = 100.0        # m/s, fast walk / light jog
DEFAULT_MIN_SEGMENT = 0.5      # seconds a (heading, speed) pair is held before
DEFAULT_MAX_SEGMENT = 2.5      # being redrawn -- this is T_{j+1} - T_j in the paper
MAX_TURN = math.pi / 3

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

def handoff_decision(ed: ED, es: EdgeServer):

    if(HaversineFormula(ed.x,ed.y,es.x,es.y) <= es.coverage_area): #calculates distance of the ED from Edge Server
        return False #Handoff not required, if within range of server
    else:
        return True #If ED outside coverage area, then handoff required

def initiate_handoff(ed: ED, es: EdgeServer):

   if(handoff_decision(ed,ed)):
       es.Utility -= ed.price_paid
       ed = ed.replace(ed, price_paid = 0)
       return

   else:
       return


def MUA():
    pass
