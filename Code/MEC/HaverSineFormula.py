import math

def HaversineFormula(x1: float, y1: float, x2: float, y2: float) -> float: #returns distance b/w 2 coordinates in meters

    lat1, lon1, lat2, lon2 = map(math.radians, [x1, y1, x2, y2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))

    r = 6371.0 #radius of earth
    return c * r * 1000 #multiply with 100 to convert distance to meters