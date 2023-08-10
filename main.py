import glob
import os
import pandas as pd
from models import TrackDetails
from parser import parse_gpx_file, max_speed
from display import display_tracks

# Constants
MS_TO_KMH_CONVERSION = 3.6
KM_CONVERSION = 1000
SECONDS_IN_HOUR = 3600

# Directory where all GPX files are
gpx_dir = './data/gpx_2023_july/'

# Get all GPX files in the directory
gpx_files = glob.glob(os.path.join(gpx_dir, '*.gpx'))

SORT_KEYS = {
    "distance": lambda x: x.distance,
    "max_speed": lambda x: x.max_speed,
    "avg_speed": lambda x: x.average_speed,
    "moving_time": lambda x: x.moving_time,
    "stop_time": lambda x: x.stop_time
}


def sort_tracks(tracks, key, reverse=True, limit=1):
    return sorted(tracks, key=SORT_KEYS[key], reverse=reverse)[:limit]


def sort_by_distance(track):
    return track.distance


def get_track_details_from_gpx(file_path):
    gpx = parse_gpx_file(file_path)
    track_details_list = []
    for track in gpx.tracks:
        distance = track.length_3d() / 1000  # Convert to kilometers
        moving_data = track.get_moving_data()
        total_time = (
                moving_data.moving_time + moving_data.stopped_time) if moving_data.moving_time + moving_data.stopped_time > 0 else 1
        avg_speed = distance / (total_time / 3600)
        track_max_speed = moving_data.max_speed * 3.6

        track_detail = TrackDetails(track.name, distance, avg_speed, track_max_speed, moving_data.moving_time,
                                    moving_data.stopped_time, track)
        track_details_list.append(track_detail)

    return track_details_list


if __name__ == '__main__':
    all_track_details = []

    # Process each GPX file to extract details
    for file in gpx_files:
        track_details_for_file = get_track_details_from_gpx(file)
        all_track_details.extend(track_details_for_file)

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
    top_10_by_distance = sort_tracks(all_track_details, "distance")
    top_10_by_max_speed = sort_tracks(all_track_details, "max_speed")
    top_10_by_avg_speed = sort_tracks(all_track_details, "avg_speed")
    top_10_by_moving_time = sort_tracks(all_track_details, "moving_time")
    top_10_by_stop_time = sort_tracks(all_track_details, "stop_time")
    # Displaying the sorted tracks
    print("\nTop 10 Tracks by Average Speed:\n")
    display_tracks(top_10_by_avg_speed)

    print("Top 10 Tracks by Maximum Speed:\n")
    display_tracks(top_10_by_max_speed)

    print("Top 10 Tracks by Distance:\n")
    display_tracks(top_10_by_distance)

    print("Top 10 Tracks by Moving Time:\n")
    display_tracks(top_10_by_moving_time)

    print("Top 10 Tracks by Stop Time:\n")
    display_tracks(top_10_by_stop_time)
