import os
import sys
import json
import argparse
import requests
import haversine
from datetime import datetime
from dateutil import tz
from haversine import haversine, Unit


my_parser = argparse.ArgumentParser()
my_parser.add_argument("-p", "-postal", type=str, help="ex: m5w1e6")
my_parser.add_argument("-lat", help="ex: 43.703344", type=float)
my_parser.add_argument("-long", help="ex: -79.524619", type=float)
my_parser.add_argument(
    "-d", "-distance", help="Search distance in KM", default=5.0, type=float,
)
my_parser.add_argument(
    "-r",
    "-report",
    action="store_true",
    help="report lat + long and stores found within search distance. will not check available pickup times",
)
my_parser.add_argument("-id", type=str, help="comma seperated store IDs ex: 1111,1122")

if len(sys.argv) == 1:
    my_parser.print_help(sys.stderr)
    sys.exit(1)

args = my_parser.parse_args()

postal_code = args.p
myLat = args.lat
myLong = args.long
within_km = args.d
report = args.r
my_ids = args.id

if my_ids:
    my_ids = my_ids.split(",")
    # Set these to True to bypass geo lookups
    myLat = True
    myLong = True

# If store ids are give, no need to worry about postal codes or lat/lot
else:
    if not postal_code and not myLat and not myLong:
        sys.exit(
            "Either postal code (-p) or latitude (-lat) and longitude (-long) values are required. Use -h for help"
        )

    if not postal_code:
        if not myLat or not myLong:
            sys.exit(
                "Both latitude (-lat) and longitude (-long) values are required. Use -h for help"
            )

mode = None

if report:
    mode = "report"

# f-strings requires python 3.6
MIN_PYTHON = (3, 6)
if sys.version_info < MIN_PYTHON:
    sys.exit("Python %s.%s or later is required.\n" % MIN_PYTHON)


from_zone = tz.gettz("UTC")
to_zone = tz.gettz("America/Toronto")


if not my_ids:
    if not myLat or not myLong:
        # Switch primary geo lookup to geocoder.ca as the results are more realiable
        geo_url_pri = "https://geocoder.ca/?geoit=xml&json=1&postal=" + postal_code
        # Use the NRC geo lookup service as a backup geo lookup
        geo_url_bak = (
            "https://geogratis.gc.ca/services/geolocation/en/locate?q=" + postal_code
        )

        geo_data = requests.get(geo_url_pri)
        # geocoder.ca can throttle requests. In this case, use the backup geolocation lookup.
        if geo_data.status_code == 200:
            geo_json = geo_data.json()
            myLat = float(geo_json["latt"])
            myLong = float(geo_json["longt"])
        else:
            geo_data = requests.get(geo_url_bak)
            geo_json = geo_data.json()
            coords = geo_json[0]["geometry"]["coordinates"]
            myLat = coords[1]
            myLong = coords[0]

myLatLong = (myLat, myLong)

if mode == "report":
    print(f"-lat {myLat} -long {myLong}")

stores_to_check = []

with open("locations.json") as inf:
    all_locs = json.load(inf)

# if store IDs are specified, no need to figure out stores based on distance
if my_ids:
    for ids in my_ids:
        for loc in all_locs["locations"]:
            store_id = loc["id"]
            if ids == store_id:
                # when using -id the distance to the store will be 0
                loc_distance = {"distance": 0}
                loc.update(loc_distance)
                stores_to_check.append(loc)
else:
    for loc in all_locs["locations"]:
        locLatLong = (loc["geoPoint"]["latitude"], loc["geoPoint"]["longitude"])
        distance = haversine(myLatLong, locLatLong)
        if distance <= within_km:
            # Add a distance key:value pair to the location object so that
            # locations can be sorted by distance after the list is created
            loc_distance = {"distance": distance}
            loc.update(loc_distance)
            stores_to_check.append(loc)

if stores_to_check:
    # Sort the list of locations by distance
    stores_to_check = sorted(stores_to_check, key=lambda s: s["distance"])

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
    loc_id = store["id"]
    address = store["address"]["formattedAddress"]
    storeBannerId = store["storeBannerId"]
    distance = round(store["distance"], 1)

    if mode == "report":
        print(f"{storeBannerId}, id: {loc_id}, {address}, approx {distance} KM away")
    else:
        base_url = store_urls[storeBannerId]
        headers = {
            "Site-Banner": storeBannerId
        }  # If this header isn't set, the site returns an error
        # Using the base_url and headers, build the full URL
        url = base_url + "/api/pickup-locations/" + loc_id + "/time-slots"
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
            output = f"{count} available at {storeBannerId} at {address} approx {distance} KM away"
            output += "\n"
            output += pickup_times
            print(output)


# Convert the UTC timestamps to localtime
def local_time(timestamp):
    utc = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
    utc = utc.replace(tzinfo=from_zone)
    local = utc.astimezone(to_zone)
    return str(local)


for store in stores_to_check:
    check_loblaws(store)
