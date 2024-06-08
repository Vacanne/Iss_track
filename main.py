import requests
from datetime import datetime

# Define your location's latitude and longitude
MY_LAT = 38.423733
MY_LONG = 27.142826

def is_iss_overhead():
    """
    Check if the ISS is currently overhead (within +/- 5 degrees latitude and longitude of your location).
    Returns True if the ISS is overhead, otherwise False.
    """
    # Make a request to the ISS current location API
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    
    # Parse the JSON response
    data = response.json()
    iss_longitude = float(data["iss_position"]["longitude"])
    iss_latitude = float(data["iss_position"]["latitude"])

    # Check if the ISS is within +/- 5 degrees of your location
    if MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and MY_LONG - 5 <= iss_longitude <= MY_LONG + 5:
        return True
    return False

def is_night():
    """
    Check if it is currently night time at your location.
    Returns True if it is night time, otherwise False.
    """
    # Define parameters for the sunrise-sunset API request
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }
    
    # Make a request to the sunrise-sunset API
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    
    # Parse the JSON response
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    
    # Get the current time
    time_now = datetime.now().hour

    # Check if the current time is before sunrise or after sunset
    if time_now >= sunset or time_now <= sunrise:
        return True
    return False

# Check if the ISS is overhead and if it is night time
if is_iss_overhead() and is_night():
    print("ISS is right over your head, look up 👆")
else:
    print("You can't see the ISS right now :(")
