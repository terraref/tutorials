# Generating file lists by plot

The terrautils python package has a new products module that aid in connecting
plot boundaries stored within betydb with file-based data products available
from the workbench or Globus.

## Getting started

After installing terrautils, you should be able to import the *prooduct* module.
```
from terrautils.products import get_sensor_list, unique_sensor_names
from terrautils.products import get_file_listing, extract_file_paths
```

The get\_sensor\_list and get\_file\_listing both require connection, url,
and key parameters. *Connection* can be 'None', the *url* (called host in the
code) should be something like https://terraref.ncsa.illinois.edu/clowder/.
The *key* is a unique access key for the Clowder api.

## Getting the sensor list
The first thing to get is the sensor name. This can be retreived using the
get\_sensor\_list function. This function returns the full record which may
be useful in some cases but also includes sensor names that include a plot id
number. The utility function unique_sensor_names accpets the sensor list and
provides a list of names suitable for use in the get_file_listing function.

```
sensors = get_sensor_list(None, url, key)
names = unique_sensor_names(sensors)
```

Names will now contain a list of sensor names support by the Clowder geostreams
API. The currently available sensors are:

* IR Surface Temperature
* Thermal IR GeoTIFFs Datasets
* flirIrCamera Datasets
* (EL) sensor\_weather\_station
* Irrigation Observations
* Canopy Cover
* Energy Farm Observations SE
* (EL) sensor\_par
* scanner3DTop Datasets
* Weather Observations
* Energy Farm Observations NE
* RGB GeoTIFFs Datasets
* (EL) sensor\_co2
* stereoTop Datasets
* Energy Farm Observations CEN

## Getting a list of files

The geostreams API can be used to get a list of datasets that overlap a
specific plot boundary and, optionally, limited by a time range. Iterating 
over the datasets allows the paths to all the files to be extracted.

```
sensor = 'Thermal IR GeoTIFFs Datasets'
sitename = 'MAC Field Scanner Season 1 Field Plot 101 W'
datasets = get_file_listing(None, url, key, sensor, sitename)
files = extract_file_paths(datasets)
```


# Alternative method
The following method demonstrates the same approach using the Clowder API. This
approach is useful for understanding the data layout and when the Python
terrautils package is not available.

## Finding plot ID
```
SENSOR_NAME = "MAC Field Scanner Season 1 Field Plot 101 W"
GET https://terraref.ncsa.illinois.edu/clowder/api/geostreams/sensors?sensor_name={SENSOR_NAME}
```

This returns a JSON object with an 'id' parameter. You can use this ID parameter to specify the right data stream.

## Finding stream ID within a plot
The names are formatted as "<Sensor Group> Datasets (<Sensor ID>)".
```
SENSOR_ID = 3355
STREAM_NAME = "Thermal IR GeoTIFFs Datasets ({SENSOR_ID})"
GET https://terraref.ncsa.illinois.edu/clowder/api/geostreams/streams?stream_name={STREAM_NAME}
```

This returns a JSON object with an 'id' parameter. You can use this ID parameter to get the right datapoints.

## Listing Clowder file IDs for that plot & sensor stream
```
STREAM_ID = "11586"
GET https://terraref.ncsa.illinois.edu/clowder/api/geostreams/datapoints?stream_id={STREAM_ID}
```

This returns a list of datapoint JSON objects, each with a 'properties' parameter that looks like:
```
properties: {
    dataset_name: "Thermal IR GeoTIFFs - 2016-05-09__12-07-57-990",
    source_dataset: "https://terraref.ncsa.illinois.edu/clowder/datasets/59fc9e7d4f0c3383c73d2905"
},
```

The source_dataset URL can be used to view the dataset in Clowder.

You can also filter the datapoints by date:
```
GET https://terraref.ncsa.illinois.edu/clowder/api/geostreams/datapoints?stream_id={STREAM_ID}&since=2017-01-02&until=2017-06-10
```

## Getting ROGER file path from dataset
Given a source dataset URL, we can call the API to get the files and their paths.
```
SOURCE_DATASET = "https://terraref.ncsa.illinois.edu/clowder/datasets/59fc9e7d4f0c3383c73d2905"
# Add /api after /clowder, and add /files at the end of the URL
GET "https://terraref.ncsa.illinois.edu/clowder/api/datasets/59fc9e7d4f0c3383c73d2905/files"
```

This returns a list of files in the dataset and their paths if available:
```
[
    {
        size: "346069",
        date-created: "Fri Nov 03 11:51:13 CDT 2017",
        id: "59fc9e814f0c3383c73d2962",
        filepath: "/home/clowder/sites/ua-mac/Level_1/ir_geotiff/2016-05-09/2016-05-09__12-07-57-990/ir_geotiff_L1_ua-mac_2016-05-09__12-07-57-990.png",
        contentType: "image/png",
        filename: "ir_geotiff_L1_ua-mac_2016-05-09__12-07-57-990.png"
    },
    {
        size: "1231298",
        date-created: "Fri Nov 03 11:51:16 CDT 2017",
        id: "59fc9e844f0c3383c73d2980",
        filepath: "/home/clowder/sites/ua-mac/Level_1/ir_geotiff/2016-05-09/2016-05-09__12-07-57-990/ir_geotiff_L1_ua-mac_2016-05-09__12-07-57-990.tif",
        contentType: "image/tiff",
        filename: "ir_geotiff_L1_ua-mac_2016-05-09__12-07-57-990.tif"
    }
]
```

Depending on permissions you may need to provide authentication to get this list.
