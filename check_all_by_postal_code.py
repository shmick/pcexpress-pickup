import sys
import json
import requests
import haversine
from datetime import datetime
from dateutil import tz
from haversine import haversine, Unit

# f-strings requires python 3.6
MIN_PYTHON = (3, 6)
if sys.version_info < MIN_PYTHON:
    sys.exit("Python %s.%s or later is required.\n" % MIN_PYTHON)

postal_code = sys.argv[1]

if len(postal_code) < 3:
    print("Please provide a postal code")
    sys.exit(1)  # postal code required

from_zone = tz.gettz("UTC")
to_zone = tz.gettz("America/Toronto")

try:
    within_km = float(sys.argv[2])
except:
    within_km = float(5)

try:
    if sys.argv[3] == "report":
        mode = "report"
except:
    mode = ""

geo_url = "https://geogratis.gc.ca/services/geolocation/en/locate?q=" + postal_code
geo_url_bak = "https://geocoder.ca/?geoit=xml&json=1&postal=" + postal_code

geo_data = requests.get(geo_url)
geo_json = geo_data.json()
if geo_json:
    coords = geo_json[0]["geometry"]["coordinates"]
    myLat = coords[1]
    myLong = coords[0]
    myLatLong = (myLat, myLong)
# Secondary lookup if first postal code lookup returns empty
if not geo_json:
    geo_data = requests.get(geo_url_bak)
    geo_json = geo_data.json()
    myLat = float(geo_json["latt"])
    myLong = float(geo_json["longt"])
    myLatLong = (myLat, myLong)

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

    # CT =  ("Colleague Testing") test location entries
    # SD = shoppers drugmart, no timeslots exist for SD yet
    if "CT" in id or "SD" in id:
        return

    address = store["address"]["formattedAddress"]
    storeBannerId = store["storeBannerId"]

    if mode == "report":
        print(f"store: {storeBannerId}, location: {id}, address: {address}")
    else:
        base_url = store_urls[storeBannerId]
        headers = {
            "Site-Banner": storeBannerId
        }  # If this header isn't set, the site returns an error
        # Using the base_url and headers, build the full URL
        url = base_url + "/api/pickup-locations/" + id + "/time-slots"
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
