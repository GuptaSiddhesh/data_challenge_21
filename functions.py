import math
import haversine as hs
from haversine import Unit


def average_distance(data):
    distances = data['DISTANCE'].to_numpy()

    my_sum = 0
    for i in range(len(distances)):

        if not math.isnan(float(distances[i])):
            my_sum += int(distances[i])

    return my_sum / len(distances)


def famous_start_stop(data, veo_data, dist):

    lon = veo_data['Lon'].to_numpy()
    lat = veo_data['Lat'].to_numpy()

    start_points_long = data['START LONG'].to_numpy()
    start_points_lat = data['START LAT'].to_numpy()
    end_points_long = data['END LONG'].to_numpy()
    end_points_lat = data['END LAT'].to_numpy()

    famous_start = [0] * 37
    famous_end = [0] * 37

    for i in range(len(lon)):

        loc1 = (float(lat[i]), float(lon[i]))

        for j in range(len(start_points_long)):

            loc2 = (float(start_points_lat[j]), float(start_points_long[j]))
            loc3 = (float(end_points_lat[j]), float(end_points_long[j]))

            if hs.haversine(loc1, loc2, unit=Unit.METERS) <= dist:
                famous_start[i] = famous_start[i] + 1

            if hs.haversine(loc1, loc3, unit=Unit.METERS) <= dist:
                famous_end[i] = famous_end[i] + 1

    sum_start = 0
    sum_end = 0
    for i in range(len(famous_start)):
        sum_start = sum_start + famous_start[i]
        sum_end = sum_end + famous_end[i]

    # random_start = 18382 - sum_start
    # random_end = 18382 - sum_end

    # print(random_start, random_end)

    veo_data['FAMOUS_START'] = famous_start
    veo_data['FAMOUS_END'] = famous_end
    start = veo_data[veo_data.FAMOUS_START == veo_data.FAMOUS_START.max()]
    
    end = veo_data[veo_data.FAMOUS_END == veo_data.FAMOUS_END.max()]
    
    return veo_data


def famous_route(data, veo_data, dist):

    lon = veo_data['Lon'].to_numpy()
    lat = veo_data['Lat'].to_numpy()

    start_points_long = data['START LONG'].to_numpy()
    start_points_lat = data['START LAT'].to_numpy()
    end_points_long = data['END LONG'].to_numpy()
    end_points_lat = data['END LAT'].to_numpy()

    length = len(start_points_long)

    fro = [""] * length
    to = [""] * length
    distance = [""] * length

    destination = veo_data['STATION'].to_numpy()

    for i in range(length):

        loc2 = (float(start_points_lat[i]), float(start_points_long[i]))

        for j in range(len(lon)):

            loc1 = (float(lat[j]), float(lon[j]))

            if fro[i] == "":
                if hs.haversine(loc1, loc2, unit=Unit.METERS) <= dist:
                    fro[i] = destination[j]
                    distance[i] = hs.haversine(loc1, loc2, unit=Unit.METERS)

            elif distance[i] > hs.haversine(loc1, loc2, unit=Unit.METERS):
                fro[i] = destination[j]

        if fro[i] == "":
            fro[i] = "unknown"

    distance = [""] * len(start_points_long)

    for i in range(length):

        loc2 = (float(end_points_lat[i]), float(end_points_long[i]))

        for j in range(len(lon)):

            loc1 = (float(lat[j]), float(lon[j]))

            if to[i] == "":
                if hs.haversine(loc1, loc2, unit=Unit.METERS) <= dist:
                    to[i] = destination[j]
                    distance[i] = hs.haversine(loc1, loc2, unit=Unit.METERS)

            elif distance[i] > hs.haversine(loc1, loc2, unit=Unit.METERS):
                distance[i] = hs.haversine(loc1, loc2, unit=Unit.METERS)
                to[i] = destination[j]

        if to[i] == "":
            to[i] = "unknown"

    map_path = {}

    for i in range(length):

        try:
            s = map_path[fro[i] + "-" + to[i]]
            map_path[fro[i]+"-"+to[i]] = s + 1
        except Exception as e:
            map_path[fro[i]+"-"+to[i]] = 1

    #print(map_path)

    start_unknown = [False] * length
    end_unknown = [False] * length

    for i in range(len(start_points_long)):
        if fro[i] == "unknown":
            start_unknown[i] = True
        if to[i] == "unknown":
            end_unknown[i] = True

    data['FROM'] = fro
    data['TO'] = to
    data['START_UNKNOWN'] = start_unknown
    data['END_UNKNOWN'] = end_unknown

    return map_path

  
def plot_map(data, veo_ride, dot_size):
    
    BBox = (-76.9804, -76.9001, 38.9685, 39.0152)
    cp = plt.imread("/content/drive/MyDrive/Data Challenge/Main Code/Maps/map.png")

    fig, ax = plt.subplots(figsize = (20,20))

    long = data['START LONG'].to_numpy()
    lat = data['START LAT'].to_numpy()
    temp_long = []
    temp_lat = []
    start_unknown = data['START_UNKNOWN'].to_numpy()

    for i in range(len(long)):
  
        if start_unknown[i] == True:
            temp_long.append(long[i])
            temp_lat.append(lat[i])

    ax.scatter(temp_long, temp_lat, zorder=1, color="RED",s=dot_size)
    ax.scatter(veo_data.Lon, veo_data.Lat, zorder=1)
    ax.imshow(cp, zorder=0, extent = BBox, aspect= 'equal')
