# Generating file lists by plot

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
