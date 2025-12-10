# Convert Celestial coordinates to local time from a fits image that 
# contains the correct data
# Created by WAH on 05-21-2024
# It takes a fits image file as a command line parameter

import datetime
import sys
from astropy.io import fits
from astropy.time import Time
from astropy.coordinates import Angle
from astropy.coordinates import SkyCoord
import astropy.units as u

def lst_to_gst(lst, longitude):
    """Convert Local Sidereal Time (LST) to Greenwich Sidereal Time (GST)."""
    gst = lst - longitude / 15.0
    gst %= 24.0  # Ensure it is within 0-24 hours
    return gst

def gst_to_ut(gst, date):
    """Convert Greenwich Sidereal Time (GST) to Universal Time (UT)."""
    # Calculate the Julian Date for 0h UT of the given date
    jd = Time(date).jd
    jd_0h = int(jd - 0.5) + 0.5

    # Calculate GST at 0h UT for the given date
    T = (jd_0h - 2451545.0) / 36525.0
    gst_0h_ut = 6.697374558 + 2400.051336 * T + 0.000025862 * T**2
    gst_0h_ut %= 24.0

    # Calculate the number of sidereal hours since 0h UT
    sidereal_hours_since_0h_ut = gst - gst_0h_ut
    sidereal_hours_since_0h_ut %= 24.0

    # Convert sidereal hours to solar (UT) hours
    ut_hours_since_0h_ut = sidereal_hours_since_0h_ut / 1.00273790935
    return ut_hours_since_0h_ut

def convert_lst_to_local_time(lst, longitude, date):
    """Convert Local Sidereal Time (LST) to Local Time."""
    gst = lst_to_gst(lst, longitude)
    ut_hours = gst_to_ut(gst, date)

    # Convert UT hours to a datetime object
    date_0h = datetime.datetime.strptime(date, "%Y-%m-%d")
    local_time = date_0h + datetime.timedelta(hours=ut_hours)
    return local_time

def extract_image_info(image_path):
    with fits.open(image_path) as hdul:
        header = hdul[0].header
        date_time_str = header['DATE-OBS']
        longitude = header.get('SITELONG', 0.0)  # Assuming longitude is provided in the header
        if 'CRVAL1' in header:
            ra = Angle(header['CRVAL1'], unit=u.hourangle).deg
            #ra = header['CRVAL1']
        else:
            raise ValueError("The image does not contain the required RA information.")
        
    return date_time_str, longitude, ra

def main(image_path):
    # Extract information from the image
    date_time_str, longitude, ra = extract_image_info(image_path)

    # Extract the date part from the timestamp
    date = date_time_str.split('T')[0]

    # Calculate the Local Sidereal Time (LST) which is approximately equal to RA
    lst = ra / 15.0  # Convert RA from degrees to hours

    # Convert LST to local time
    local_time = convert_lst_to_local_time(lst, longitude, date)
    print(f"Local Time: {local_time}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script_name.py <image_path>")
        sys.exit(1)
    
    image_path = sys.argv[1]
    main(image_path)
