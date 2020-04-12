import os
import sys
import json
import argparse
import requests
import haversine
from datetime import datetime
from dateutil import tz
from haversine import haversine, Unit

MIN_PYTHON = (3, 6)  # Python 3.6
args = sys.argv[1:]
geo_pri = "https://geocoder.ca/?geoit=xml&json=1&postal="
geo_bak = "https://geogratis.gc.ca/services/geolocation/en/locate?q="
store_locations = "./locations.json"


def parse_args(args):
    parser = argparse.ArgumentParser()

    parser.add_argument("-p", "-postal", type=str, help="ex: m5w1e6")
    parser.add_argument("-lat", help="ex: 43.703344", type=float)
    parser.add_argument("-long", help="ex: -79.524619", type=float)
    parser.add_argument(
        "-d", "-distance", help="Search distance in KM", default=5.0, type=float,
    )
    parser.add_argument(
        "-r",
        "-report",
        action="store_true",
        help="report lat + long and stores found within search distance. will not check available pickup times",
    )
    parser.add_argument("-id", type=str, help="comma seperated store IDs ex: 1111,1122")
    parser.add_argument(
        "--verbose", action="store_true", help=argparse.SUPPRESS,
    )
    args = parser.parse_args(args)
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    return args


def get_ids(my_ids):
    if my_ids:
        my_ids = my_ids.split(",")
    return my_ids


def check_params(postal_code, myLat, myLong):
    if not postal_code and not myLat and not myLong:
        sys.exit(
            "Either postal code (-p) or latitude (-lat) and longitude (-long) values are required. Use -h for help"
        )

    if not postal_code:
        if not myLat or not myLong:
            sys.exit(
                "Both latitude (-lat) and longitude (-long) values are required. Use -h for help"
            )


def geo_lookup(postal_code):
    geo_url_pri = geo_pri + postal_code
    try:
        geo_data = requests.get(geo_url_pri)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
    # geocoder.ca can throttle requests. In this case, use the backup geolocation lookup.
    if geo_data.status_code == 200:
        geo_json = geo_data.json()
        myLat = float(geo_json["latt"])
        myLong = float(geo_json["longt"])
    else:
        geo_url_bak = geo_bak + postal_code
        try:
            geo_data = requests.get(geo_url_bak)
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
        geo_json = geo_data.json()
        coords = geo_json[0]["geometry"]["coordinates"]
        myLat = coords[1]
        myLong = coords[0]

    myLatLong = (myLat, myLong)
    # if verbose:
    #     print(f"geo json: {geo_json}")
    return myLatLong


def get_latlog(postal_code, myLat, myLong, report):
    myLatLong = None
    if postal_code:
        if not myLat or not myLong:
            myLatLong = geo_lookup(postal_code)
    if myLat and myLong:
        myLatLong = (myLat, myLong)
    if report and not my_ids:
        print(f"-lat {myLatLong[0]} -long {myLatLong[1]}")
    return myLatLong


def check_stores_by_id(my_ids, all_locs):
    stores_to_check = []
    for ids in my_ids:
        for loc in all_locs["locations"]:
            store_id = loc["id"]
            if ids == store_id:
                # when using -id the distance to the store will be 0
                loc_distance = {"distance": 0}
                loc.update(loc_distance)
                stores_to_check.append(loc)
    return stores_to_check


def check_stores_by_geo(myLatLong, all_locs, within_km):
    stores_to_check = []
    for loc in all_locs["locations"]:
        locLatLong = (loc["geoPoint"]["latitude"], loc["geoPoint"]["longitude"])
        distance = haversine(myLatLong, locLatLong)
        if distance <= within_km:
            # Add a distance key:value pair to the location object so that
            # locations can be sorted by distance after the list is created
            loc_distance = {"distance": distance}
            loc.update(loc_distance)
            stores_to_check.append(loc)
    return stores_to_check


def stores_to_check(store_locations):
    with open(store_locations) as inf:
        all_locs = json.load(inf)
    stores_to_check = []
    # if store IDs are specified, no need to figure out stores based on distance
    if my_ids:
        stores_to_check = check_stores_by_id(my_ids, all_locs)
    else:
        myLatLong = get_latlog(postal_code, myLat, myLong, report)
        stores_to_check = check_stores_by_geo(myLatLong, all_locs, within_km)

    if stores_to_check:
        # Sort the list of locations by distance
        stores_to_check = sorted(stores_to_check, key=lambda s: s["distance"])
    return stores_to_check


def check_loblaws(store):
    loc_id = store["id"]
    address = store["address"]["formattedAddress"]
    storeBannerId = store["storeBannerId"]
    distance = round(store["distance"], 1)

    if report:
        print(f"{storeBannerId}, id: {loc_id}, {address}, approx {distance} KM away")
    else:
        if verbose:
            print(
                f"checking {storeBannerId}, id: {loc_id}, {address}, approx {distance} KM away"
            )
        base_url = store_urls[storeBannerId]
        headers = {
            "Site-Banner": storeBannerId
        }  # If this header isn't set, the site returns an error
        url = base_url + "/api/pickup-locations/" + loc_id + "/time-slots"
        try:
            r = requests.get(url, headers=headers)
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
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
from_zone = tz.gettz("UTC")
to_zone = tz.gettz("America/Toronto")


def local_time(timestamp):
    utc = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
    utc = utc.replace(tzinfo=from_zone)
    local = utc.astimezone(to_zone)
    return str(local)


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


def check_python_ver(info):
    if info < MIN_PYTHON:
        sys.exit("Python %s.%s or later is required.\n" % MIN_PYTHON)


if __name__ == "__main__":
    check_python_ver(sys.version_info)
    args = parse_args(args)
    postal_code = args.p
    myLat = args.lat
    myLong = args.long
    within_km = args.d
    report = args.r
    my_ids = args.id
    verbose = args.verbose

    if verbose:
        print(args)

    my_ids = get_ids(my_ids)
    if not my_ids:
        check_params(postal_code, myLat, myLong)

    stores_to_check = stores_to_check(store_locations)
    for store in stores_to_check:
        check_loblaws(store)
