class TrackDetails:
    def __init__(self, name, distance, average_speed, max_speed, moving_time, stop_time, gpx_track):
        self.name = name
        self.distance = distance
        self.average_speed = average_speed
        self.max_speed = max_speed
        self.moving_time = moving_time
        self.stop_time = stop_time
        self.gpx_track = gpx_track  # This will store the actual GPX track object

    def __lt__(self, other):
        return (
            self.distance,
            self.max_speed,
            self.average_speed,
            -self.moving_time,  # We use negative because we want longer moving times to be considered "greater"
            self.stop_time
        ) < (
            other.distance,
            other.max_speed,
            other.average_speed,
            -other.moving_time,
            other.stop_time
        )
