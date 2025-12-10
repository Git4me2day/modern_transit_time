import sys
import datetime
import subprocess

def read_local_time(output_str):
    """Extract the local time from the output string."""
    try:
        _, local_time_str = output_str.split(": ", 1)
        local_time = datetime.datetime.strptime(local_time_str.strip(), "%Y-%m-%d %H:%M:%S.%f")
        return local_time
    except ValueError:
        print("Error parsing local time from the provided string.")
        sys.exit(1)

def get_image_timestamp(image_path):
    """Extract the timestamp from the FITS image."""
    from astropy.io import fits

    with fits.open(image_path) as hdul:
        header = hdul[0].header
        date_time_str = header['DATE-OBS']
        image_time = datetime.datetime.strptime(date_time_str, "%Y-%m-%dT%H:%M:%S")
    return image_time

def adjust_system_time(new_time):
    """Adjust the system time to the new time."""
    time_str = new_time.strftime("%m%d%H%M%Y.%S")
    subprocess.run(['sudo', 'date', time_str])

def main(output_str, image_path):
    # Read the local time from the output string
    local_time = read_local_time(output_str)

    # Get the timestamp from the image
    image_time = get_image_timestamp(image_path)

    # Calculate the time difference
    time_difference = local_time - image_time
    current_time = datetime.datetime.now()
    adjusted_time = current_time + time_difference

    # Adjust the system time
    adjust_system_time(adjusted_time)
    print(f"System time adjusted to: {adjusted_time}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python adjust_system_time.py '<output_str>' <image_path>")
        sys.exit(1)
    
    output_str = sys.argv[1]
    image_path = sys.argv[2]
    main(output_str, image_path)
