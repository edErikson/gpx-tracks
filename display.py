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
