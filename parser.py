import gpxpy

def max_speed(track):
    """Compute the maximum speed of the track."""
    max_spd = 0
    for segment in track.segments:
        for i in range(len(segment.points) - 1):
            point1 = segment.points[i]
            point2 = segment.points[i+1]
            distance = haversine_distance(point1.latitude, point1.longitude, point2.latitude, point2.longitude)
            time_diff = (point2.time - point1.time).total_seconds()
            if time_diff > 0:  # Avoid division by zero+
                speed = distance / time_diff  # in meters per second
                max_spd = max(max_spd, speed)
    return max_spd * 3.6  # Convert from m/s to km/h

def haversine_distance(lat1, lon1, lat2, lon2):
    # Assuming this is the function you've used to compute haversine distance
    # Please insert your haversine formula logic here
    pass

def parse_gpx_file(file):
    with open(file, 'r', encoding="utf-8") as gpx_file:
        gpx = gpxpy.parse(gpx_file)
        return gpx
