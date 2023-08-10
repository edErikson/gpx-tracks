import gpxpy
import os
import math
import glob
import pandas as pd

# Directory where all GPX files are
gpx_dir = './data/gpx_2023_july/'

# Get all GPX files in the directory
gpx_files = glob.glob(os.path.join(gpx_dir, '*.gpx'))


# Structure to hold track details
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


def sort_by_distance(track):
    return track.distance


def sort_by_max_speed(track):
    return track.max_speed


def sort_by_avg_speed(track):
    return track.average_speed


def sort_by_moving_time(track):
    return -track.moving_time  # negative to sort in descending order


def sort_by_stop_time(track):
    return -track.stop_time  # negative to sort in descending order


def display_track_details(track):
    """Print the details of a given track."""
    print(f"Track Name: {track.name}")
    print(f"Total Distance: {track.distance:.3f} km")
    print(f"Average Speed: {track.average_speed:.3f} km/h")
    print(f"Maximum Speed: {track.max_speed:.3f} km/h")

    hours, remainder = divmod(track.moving_time, 3600)
    minutes, seconds = divmod(remainder, 60)
    moving_time_hms = f"{int(hours)}:{int(minutes):02}:{int(seconds):02}"

    hours, remainder = divmod(track.stop_time, 3600)
    minutes, seconds = divmod(remainder, 60)
    stopped_time_hms = f"{int(hours)}:{int(minutes):02}:{int(seconds):02}"

    print(f"Total Moving Time: {moving_time_hms}")
    print(f"Total Stop Time: {stopped_time_hms}")
    print("-" * 40)


def display_tracks(track_list):
    """Display details for a list of tracks."""
    for track in track_list:
        display_track_details(track)



if __name__ == '__main__':
    print(gpx_files)

    all_track_details = []

    # Process each GPX file to extract details
    for file in gpx_files:
        with open(file, 'r', encoding="utf-8") as gpx_file:
            gpx = gpxpy.parse(gpx_file)
            for track in gpx.tracks:
                distance = track.length_3d() / 1000  # Convert to kilometers
                moving_data = track.get_moving_data()
                total_time = (
                            moving_data.moving_time + moving_data.stopped_time) if moving_data.moving_time + moving_data.stopped_time > 0 else 1  # Avoid division by zero
                avg_speed = distance / (total_time / 3600)  # Convert total_time to hours
                track_max_speed = moving_data.max_speed * 3.6  # Convert from m/s to km/h

                # Add the current track's details to the list
                track_detail = TrackDetails(track.name, distance, avg_speed, track_max_speed, moving_data.moving_time,
                                            moving_data.stopped_time, track)
                all_track_details.append(track_detail)

    top_10_by_distance = sorted(all_track_details, key=sort_by_distance, reverse=True)[:3]
    top_10_by_max_speed = sorted(all_track_details, key=sort_by_max_speed, reverse=True)[:3]
    top_10_by_avg_speed = sorted(all_track_details, key=sort_by_avg_speed, reverse=True)[:3]
    top_10_by_moving_time = sorted(all_track_details, key=lambda x: x.moving_time, reverse=True)[:3]
    top_10_by_stop_time = sorted(all_track_details, key=lambda x: x.stop_time, reverse=True)[:3]
    print("\nTop 10 Tracks by Average Speed:\n")
    display_tracks(top_10_by_avg_speed)
    print("Top 10 Tracks by Maximum Speed:\n")
    display_tracks(top_10_by_max_speed)
    print("Top 10 Tracks by Mocving Time:\n")
    display_tracks(top_10_by_moving_time)
    print("Top 10 Tracks by Stop Time:\n")
    display_tracks(top_10_by_stop_time)

    # Create a list of dictionaries with each track's details
    data = []
    for track in all_track_details:
        total_time = track.moving_time + track.stop_time
        data.append({
            'Track Name': track.name,
            'Total Distance (km)': track.distance,
            'Moving Time (s)': track.moving_time,
            'Stop Time (s)': track.stop_time,
            'Total Time (s)': total_time,
            'Average Speed (km/h)': track.average_speed,
            'Max Speed (km/h)': track.max_speed
        })

    # Create a DataFrame from the data
    df = pd.DataFrame(data)
    print(df)
