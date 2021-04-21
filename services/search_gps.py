import math
POINT_GPS_LAT = 100 # 1 vi do = 100km
POINT_GPS_LONG = 90 # 1 kinh do = 90km
POINT_GPS = 50 * math.sqrt(2)

def get_distance(long1, lat1, long2, lat2):

    if (long1 * long2 * lat1 * lat2 == 0):
        print(f'long1 = {long1}; lat1 = {lat1}; long2 = {long2}; lat2 = {lat2}; pointGPS = {point}')
        return POINT_GPS

    distance = (long1 - long2) * (long1 - long2)
    distance += (lat1 - lat2) * (lat1 - lat2)
    distance = math.sqrt(distance)
    point = POINT_GPS * distance
    print(f'long1 = {long1}; lat1 = {lat1}; long2 = {long2}; lat2 = {lat2}; distance = {distance}; pointGPS = {point}')
    return point  