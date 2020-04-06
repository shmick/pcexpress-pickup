import sys
import json
import requests
import haversine

# from xml.dom.minidom import parseString
from datetime import datetime
from dateutil import tz
from haversine import haversine, Unit

from_zone = tz.gettz("UTC")
to_zone = tz.gettz("America/Toronto")

try:
    within_km = float(sys.argv[2])
except:
    within_km = float(5)


geo_url = "https://geogratis.gc.ca/services/geolocation/en/locate?q=" + sys.argv[1]
geo_data = requests.get(geo_url)
geo_json = geo_data.json()
coords = geo_json[0]["geometry"]["coordinates"]
pLat = coords[1]
pLong = coords[0]
myLatLong = (pLat, pLong)

stores_to_check = []

with open("locations.json") as inf:
    all_locs = json.load(inf)

for loc in all_locs["locations"]:
    locLatLong = (loc["geoPoint"]["latitude"], loc["geoPoint"]["longitude"])
    if haversine(myLatLong, locLatLong) <= within_km:
        stores_to_check.append(loc)

store_urls = {
    "bloor": "https://www.bloorstreetmarket.ca",
    "box": "https://www.boxfoodstores.ca",
    "independent": "https://www.yourindependentgrocer.ca",
    "dominion": "https://www.newfoundlandgrocerystores.ca",
    "extra": "https://www.extrafoods.ca",
    "fortinos": "https://www.fortinos.ca",
    "loblaw": "https://www.loblaws.ca",
    "independentcitymarket": "https://www.independentcitymarket.ca",
    "provigo": "https://www.provigo.ca",
    "rass": "https://www.atlanticsuperstore.ca",
    "saveeasy": "https://www.saveeasy.ca",
    "superstore": "https://www.superstore.ca",
    "valumart": "https://www.valumart.ca",
    "zehrs": "https://www.zehrs.ca",
    "maxi": "https://www.maxi.ca",
    "nofrills": "https://www.nofrills.ca",
    "wholesaleclub": "https://www.wholesaleclub.ca",
    "tntsupermarket": "https://www.tntsupermarket.com",
}


def check_loblaws(store):
    id = store["id"]

    # not entirely sure what this is for ("Colleague Testing")
    if "CT" in id:
        return

    address = store["address"]["formattedAddress"]
    storeBannerId = store["storeBannerId"]
    base_url = store_urls[storeBannerId]
    headers = {
        "Site-Banner": storeBannerId
    }  # If this header isn't set, the site returns an error

    # Using the base_url and headers, build the full URL
    url = f"{base_url}/api/pickup-locations/{id}/time-slots"
    # Make the HTTP request
    r = requests.get(url, headers=headers)
    # Use the builtin JSON decoder
    data = r.json()
    # We only want to process the timeSlots entries from the output
    try:
        timeslots = data["timeSlots"]
    except:
        return

    # Initialze an empty string to store the pickup_times
    pickup_times = ""

    # Loop through the results
    for startTime in timeslots:
        # Get a list of pickup times where the "available" value is not False
        if not startTime.get("available") is False:
            # Convert the UTC times to local time
            start_time = local_time(startTime["startTime"])
            # Append the converted start_time to the results
            pickup_times += start_time
            pickup_times += "\n"

    if pickup_times:
        count = pickup_times.count("\n")
        output = f"{count} pickup times available at {storeBannerId} at {address}"
        output += "\n"
        output += pickup_times

        print(output)


# Convert the UTC timestamps to localtime
def local_time(timestamp):
    utc = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
    utc = utc.replace(tzinfo=from_zone)
    local = utc.astimezone(to_zone)
    return str(local)


for tStore in stores_to_check:
    check_loblaws(tStore)
