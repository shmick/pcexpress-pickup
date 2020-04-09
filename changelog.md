### 2020 April 9

* check for MYLAT and MYLONG environment variables to bypass geo lookup request. If the report option is used, it will give you the variables to use along with the locations.
```bash
$ python check_all_by_postal_code.py m5e1w6 2 report
export MYLAT="43.703344" ; export MYLONG="-79.524619"
store: superstore, location: 2800, address: 2549 Weston Rd Toronto, Ontario M9N 2A7, approx 0 KM away
store: nofrills, location: 3480, address: 245 Dixon Rd Etobicoke, Ontario M9P 2M4, approx 1 KM away
```
* geo lookup throttling fix

* renamed id variable to loc_id as `id()` is a built-in python function

* additional filtering of locations.json

### 2020 April 8

* fallback to NRC geo lookup in the event that geocode.ca throttles requests

* switch to geocode.ca as primary geo lookup for more reliable results

* store locations are displayed in order of distance closest to you 

* add secondary postal code lookup since the NRC geo lookup may return nothing

### 2020 April 6

* add Dockerfile and link to dockerhub

* add `report` mode to check_all_by_postal_code.py

* add postal_code variable

* check to ensure a minimum python version of 3.6 is being used

* change base_url to a dictionary lookup

### 2020 April 5

* merge [Lookup by PostCode / Specify Max Dist in KM feature](https://github.com/shmick/pcexpress-pickup/pull/1) ( Big thanks to [adam1](https://github.com/1adam) )

### 2020 April 1

* add LICENSE

* add stores.json and update locations.json

* initial commit