# pcexpress-pickup
A script to check for available pickup times at PC Express locations

### installation using a python3 virtual environment
```bash
$ git clone https://github.com/shmick/pcexpress-pickup
$ python3 -m venv pcexpress-pickup/
$ cd pcexpress-pickup/
$ source bin/activate
$ pip install -r requirements.txt 
```

### example output - lookup by Postal Code and (optional) Distance in KM (default 5)
```
$ python check_all_by_postal_code.py m6h2b4 3 
2 pickup times available at nofrills at 222 Lansdowne Ave Toronto, Ontario M6K 3C6
2020-04-19 13:00:00-04:00
2020-04-19 15:00:00-04:00
<...>
```

### generate a report of the stores that match your postal code and search distance
```
$ python check_all_by_postal_code.py m6h2b4 3 report
store: loblaw, location: 1029, address: 650 Dupont St Toronto, Ontario M6G 4B1
store: loblaw, location: 1154, address: 2280 Dundas St W Toronto, Ontario M6R 1X3
store: loblaw, location: 1212, address: 396 St Clair Ave W Toronto, Ontario M5P 3N3
store: nofrills, location: 3926, address: 222 Lansdowne Ave Toronto, Ontario M6K 3C6
store: nofrills, location: 0730, address: 900 Dufferin St Toronto, Ontario M6H 4A9
<...>
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

## Build and run your own container
```bash
$ git clone https://github.com/shmick/pcexpress-pickup
$ cd pcexpress-pickup/
$ docker build -t pcexpress:latest .
$ docker run --rm pcexpress -p m6h2b4 3
```

# Notes
https://www.pcexpress.ca/bundle.js contains a list of all pcexpress pickup locations and variety of locatio metadata. 

The store locations have been extracted to locations.json

### location sample data
```json
[
    {
        "id": "1000",
        "contactNumber": "4167033419",
        "name": "Queen Street West",
        "storeId": "1000",
        "storeBannerId": "loblaw",
        "locationType": "STORE",
        "pickupType": "STORE",
        "bufferTimeInHours": 2,
        "partner": null,
        "visible": true,
        "isShoppable": true,
        "geoPoint": {
            "latitude": 43.647355,
            "longitude": -79.401696
        },
        "address": {
            "country": "Canada",
            "region": "ON",
            "town": "Toronto",
            "line1": "585 Queen St W",
            "line2": null,
            "postalCode": "M5V 2B7",
            "formattedAddress": "585 Queen St W Toronto, ON M5V 2B7"
        },
        "timeZone": "EST5EDT",
        "features": []
    },
    {
        "id": "1032",
        "contactNumber": "9052941680",
        "name": "Bullock Drive",
        "storeId": "1032",
        "storeBannerId": "loblaw",
        "locationType": "STORE",
        "pickupType": "STORE",
        "bufferTimeInHours": 2,
        "partner": null,
        "visible": true,
        "isShoppable": true,
        "geoPoint": {
            "latitude": 43.874193,
            "longitude": -79.284753
        },
        "address": {
            "country": "Canada",
            "region": "Ontario",
            "town": "Markham",
            "line1": "200 Bullock Dr",
            "line2": null,
            "postalCode": "L3P 1W2",
            "formattedAddress": "200 Bullock Dr Markham, Ontario L3P 1W2"
        },
        "timeZone": "EST5EDT",
        "features": []
    }
]   
```


### Activate locations and store banners

```json
activeLocations: [
                    "loblaw",
                    "superstore",
                    "nofrills",
                    "fortinos",
                    "independent",
                    "zehrs",
                    "independentcitymarket",
                    "rass",
                    "dominion",
                    "provigo",
                    "maxi",
                    "valumart",
                    "wholesaleclub"
                ]
```

```                       
rass: {key: "rass",label: "Atlantic SuperStore",value:!0,activeOn: "Sat, 01 Jan 2000 00:00:00 UTC"
dominion: {key: "dominion",label: "Dominion Stores in Newfoundland and Labrador",value:!0,activeOn: "Sat, 01 Jan 2000 00:00:00 UTC"
fortinos: {key: "fortinos",label: "Fortinos",value:!0,activeOn: "Sat, 01 Jan 2000 00:00:00 UTC"
independent: {key: "independent",label: "Your Independent Grocer",value:!0,activeOn: "Sat, 01 Jan 2000 00:00:00 UTC"
loblaw: {key: "loblaw",label: "Loblaws",value:!0,activeOn: "Sat, 01 Jan 2000 00:00:00 UTC"
provigo: {key: "provigo",label: "Provigo",value:!0,activeOn: "Sat, 01 Jan 2000 00:00:00 UTC"
superstore: {key: "superstore",label: "Real Canadian Superstore",value:!0,activeOn: "Sat, 01 Jan 2000 00:00:00 UTC"
valumart: {key: "valumart",label: "Valu-mart",value:!0,activeOn: "Sat, 01 Jan 2000 00:00:00 UTC"
zehrs: {key: "zehrs",label: "Zehrs",value:!0,activeOn: "Sat, 01 Jan 2000 00:00:00 UTC"
maxi: {key: "maxi",label: "Maxi",value:!0,activeOn: "Tues, 05 June 2018 4:00:00 UTC"
nofrills: {key: "nofrills",label: "No Frills",value:!0,activeOn: "Tues, 05 June 2018 4:00:00 UTC"
independentcitymarket: {key: "independentcitymarket",label: "City Market",value:!0,activeOn: "Sat, 01 Jan 2000 00:00:00 UTC"
wholesaleclub: {key: "wholesaleclub",label: "Wholesale Club",value:!0,activeOn: "Sat, 01 Jan 2000 00:00:00 UTC"
```
