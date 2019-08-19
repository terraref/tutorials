Second Walkthrough Notes
================
Kristina Riemer

python modules: terrautils requests io

## Video 1:

``` shell
python3
```

``` python
from terrautils.products import get_sensor_list, unique_sensor_names
```

returns all sensors in geostream database ~45,000 sensors in list bunch
of info about each

``` python
url = 'https://terraref.ncsa.illinois.edu/clowder/'
key = ''

sensors = get_sensor_list(None, url, key)
type(sensors)
len(sensors)
sensors[1]
```

this isolates from name key value, removing number in parentheses which
is the sensor\_id only unique values too

``` python
names = unique_sensor_names(sensors)
```

requests library is similar to jsonlite R one from last week, pulling
data from online using API `get` to retrieve data

filename and id to get actual files? how are these related to what came
before with terrautils? how to get file urls? are these from just
example data on clowder? change stream = FALSE to get actual file? just
do for one

`open` and `write` are `io` functions? wb = write and
binary

``` python
single_r = requests.get(filesurl + files[1]['id'], params=params, stream=True)

with open(files[1]['filename'], 'wb') as o:
  for chunk in single_r.iter_content(chunk_size=1024):
    if chunk:
      o.write(chunk)
```

``` python
import requests
from io import open

single_r = requests.get('https://terraref.ncsa.illinois.edu/clowder/files/5c507cb84f0cfd2aedf5a75a', params={'key': ''})

with open('rgb_geotiff_L1_ua-mac_2018-06-02__14-12-05-077_left.tif', 'wb') as o:
    for chunk in single_r.iter_content(chunk_size=1024):
        if chunk:
            o.write(chunk)
```

``` python
import requests
from io import open

single_r = requests.get('https://terraref.ncsa.illinois.edu/clowder/api/files/5c507cb84f0cfd2aedf5a75a', params={'key': ''})

with open('rgb_geotiff_L1_ua-mac_2018-06-02__14-12-05-077_left.tif', 'wb') as o:
    for chunk in single_r.iter_content(chunk_size=1024):
        if chunk:
            o.write(chunk)
```
