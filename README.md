# pcexpress-pickup
A script to check for available pickup times at PC Express locations

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
$ docker run shmick/pcexpress-pickup -p m6h2b4 3
```

## Build and run your own container
```bash
$ git clone https://github.com/shmick/pcexpress-pickup
$ cd pcexpress-pickup/
$ docker build -t pcexpress-pickup:latest .
$ docker run pcexpress-pickup -p m6h2b4 3
```

### example output - lookup by Postal Code and (optional) Distance in KM (default 5)
```
$ python check_all_by_postal_code.py m5e1w6 3
12 pickup times available at loblaw at 10 Lower Jarvis St Toronto, Ontario M5E 1Z2 approx 0 KM away
2020-04-22 08:00:00-04:00
<...>
2020-04-22 19:00:00-04:00

15 pickup times available at loblaw at 60 Carlton St Toronto, Ontario M5B 1L1 approx 1 KM away
2020-04-18 11:00:00-04:00
<...>
2020-04-22 19:00:00-04:00

36 pickup times available at loblaw at 585 Queen St W Toronto, ON M5V 2B7 approx 2 KM away
2020-04-18 18:00:00-04:00
<...>
2020-04-20 11:00:00-04:00
```

### generate a report of the stores that match your postal code and search distance
```
$ python check_all_by_postal_code.py m5e1w6 3 report
store: loblaw, location: 1079, address: 10 Lower Jarvis St Toronto, Ontario M5E 1Z2, approx 0 KM away
<...>
store: independentcitymarket, location: 0479, address: 55 Bloor St W Toronto, Ontario M4W 1A5, approx 2 KM away
```

### example output of older check.py script
```
$ python check.py 
5 pickup times available at rcss at 15900 Bayview Ave Aurora, Ontario L4G 7Y3
2020-04-14 10:00:00-04:00
2020-04-14 12:00:00-04:00
<...>

7 pickup times available at nofrills at 9325 Yonge St Richmond Hill, Ontario L4C 0A8
2020-04-14 09:00:00-04:00
2020-04-14 10:00:00-04:00
<...>

5 pickup times available at nofrills at 14800 Yonge St #162 Aurora, Ontario L4G 1N3
2020-04-14 09:00:00-04:00
2020-04-14 11:00:00-04:00
<...>
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