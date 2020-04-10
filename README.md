# pcexpress-pickup
A script to check for available pickup times at PC Express locations

## Usage
```bash
$ python check_all_by_postal_code.py -h
usage: check_all_by_postal_code.py [-h] [-p P] [-lat LAT] [-long LONG] [-d D] [-r]

optional arguments:
  -h, --help         show this help message and exit
  -p P, -postal P    ex: m5w1e6
  -lat LAT           ex: 43.703344
  -long LONG         ex: -79.524619
  -d D, -distance D  Search distance in KM
  -r, -report        report lat + long and stores found within search distance. will not check available pickup times
```

### Report a list of stores available within a 10KM radius
```bash
$ python check_all_by_postal_code.py -p m5e1w6 -d 10 -r
-lat 43.703344 -long -79.524619
superstore, id: 2800, 2549 Weston Rd Toronto, Ontario M9N 2A7, approx 0.9 KM away
<...>
fortinos, id: 0096, 3940 Hwy 7 RR 2 Vaughan, Ontario L4L 9C3, approx 9.8 KM away
```

### Use -lat and -long to avoid doing a postal code lookup each time
```bash
$ python check_all_by_postal_code.py -lat 43.703344 -long -79.524619 -d 10 
9 available at nofrills at 245 Dixon Rd Etobicoke, Ontario M9P 2M4 approx 1.8 KM away
2020-04-14 09:00:00-04:00
<...>
2020-04-23 19:00:00-04:00

1 available at loblaw at 270 The Kingsway Etobicoke, Ontario M9A 3T7 approx 4.7 KM away
2020-04-23 16:00:00-04:00

1 available at loblaw at 3671 Dundas St W Toronto, Ontario M6S 2T3 approx 4.8 KM away
2020-04-23 16:00:00-04:00
```

## Installation using a python3 virtual environment - python 3.6 or newer required
```bash
$ git clone https://github.com/shmick/pcexpress-pickup
$ python3 -m venv pcexpress-pickup/
$ cd pcexpress-pickup/
$ source bin/activate
$ pip install -r requirements.txt 
```

## Run via Docker
```bash
$ docker run shmick/pcexpress-pickup -lat 43.703344 -long -79.524619
8 available at nofrills at 245 Dixon Rd Etobicoke, Ontario M9P 2M4 approx 1.8 KM away
2020-04-23 12:00:00-04:00
2020-04-23 13:00:00-04:00
2020-04-23 14:00:00-04:00
2020-04-23 15:00:00-04:00
2020-04-23 16:00:00-04:00
2020-04-23 17:00:00-04:00
2020-04-23 18:00:00-04:00
2020-04-23 19:00:00-04:00

1 available at loblaw at 3671 Dundas St W Toronto, Ontario M6S 2T3 approx 4.8 KM away
2020-04-23 16:00:00-04:00
```

## Build and run your own container
```bash
$ git clone https://github.com/shmick/pcexpress-pickup
$ cd pcexpress-pickup/
$ docker build -t pcexpress-pickup:latest .
$ docker run shmick/pcexpress-pickup
```

# Notes
https://www.pcexpress.ca/bundle.js contains a list of all pcexpress pickup locations as well as plenty of other store and location metadata. 

Active stores locations have been extracted to locations.json, which is what the utility uses.

The entire unfiltered location dataset has been saved to unfiltered-locations.json

### location sample data
```json
{
  "locations": [
    {
      "id": "0925",
      "contactNumber": "7096430850",
      "name": "Prince Rupert Street",
      "storeId": "0925",
      "storeBannerId": "dominion",
      "locationType": "STORE",
      "pickupType": "STORE",
      "bufferTimeInHours": 2,
      "partner": null,
      "visible": true,
      "isShoppable": true,
      "geoPoint": {
        "latitude": 48.546052,
        "longitude": -58.582397
      },
      "address": {
        "country": "Canada",
        "region": "Newfoundland and Labrador",
        "town": "Stephenville",
        "line1": "62 Prince Rupert St",
        "line2": null,
        "postalCode": "A2N 3W7",
        "formattedAddress": "62 Prince Rupert St Stephenville, Newfoundland and Labrador A2N 3W7"
      },
      "timeZone": "Canada/Newfoundland",
      "features": []
    },
    {
      "id": "0927",
      "contactNumber": "7096513437",
      "name": "Laurell Road",
      "storeId": "0927",
      "storeBannerId": "dominion",
      "locationType": "STORE",
      "pickupType": "STORE",
      "bufferTimeInHours": 2,
      "partner": null,
      "visible": true,
      "isShoppable": true,
      "geoPoint": {
        "latitude": 48.949657,
        "longitude": -54.60071
      },
      "address": {
        "country": "Canada",
        "region": "Newfoundland and Labrador",
        "town": "Gander",
        "line1": "100 Laurell Rd",
        "line2": null,
        "postalCode": "A1V 2V5",
        "formattedAddress": "100 Laurell Rd Gander, Newfoundland and Labrador A1V 2V5"
      },
      "timeZone": "Canada/Newfoundland",
      "features": []
    }
  ]
}
```