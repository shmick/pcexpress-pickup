import requests
from datetime import datetime
from dateutil import tz

from_zone = tz.gettz("UTC")
to_zone = tz.gettz("America/Toronto")

loblaws_dict = {
    "1208": "10909 Yonge St Richmond Hill, Ontario L4C 3E3",
    "1028": "301 High Tech Rd Richmond Hill, Ontario L4B 4R2",
}

rcss_dict = {
    "1030": "15900 Bayview Ave Aurora, Ontario L4G 7Y3",
}

nofrills_dict = {
    "0770": "9325 Yonge St Richmond Hill, Ontario L4C 0A8",
    "3652": "14800 Yonge St #162 Aurora, Ontario L4G 1N3",
}


def check_loblaws(storeBannerId, id):

    if storeBannerId == "loblaws":
        base_url = "https://www.loblaws.ca"
        # If this header isn't set, the site returns an error
        headers = {"Site-Banner": "loblaw"}
        address = loblaws_dict[id]

    if storeBannerId == "rcss":
        base_url = "https://www.realcanadiansuperstore.ca"
        # If this header isn't set, the site returns an error
        headers = {"Site-Banner": "superstore"}
        address = rcss_dict[id]

    if storeBannerId == "nofrills":
        base_url = "https://www.nofrills.ca"
        # If this header isn't set, the site returns an error
        headers = {"Site-Banner": "nofrills"}
        address = nofrills_dict[id]

    # Using the base_url and headers, build the full URL
    url = f"{base_url}/api/pickup-locations/{id}/time-slots"
    # Make the HTTP request
    r = requests.get(url, headers=headers)
    # Use the builtin JSON decoder
    data = r.json()
    # We only want to process the timeSlots entries from the output
    timeslots = data["timeSlots"]
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


check_loblaws("loblaws", "1208")
check_loblaws("loblaws", "1028")
check_loblaws("rcss", "1030")
check_loblaws("nofrills", "0770")
check_loblaws("nofrills", "3652")
