import requests

"""
Example to pull weather station data from Clowder Geostreams.

Geostreams has 3 levels of organization used for TERRA-REF:
    "sensors" are mapped to data collections - each plot is a sensor, so is weather station
    "streams" are time series for each sensor - each plot has streams for data products
    "datapoints" are fundamental entries that make up the time series

Example properties for Weather Station datapoints:
    {
        source: "https://terraref.ncsa.illinois.edu/clowder/datasets/5b469f234f0cef0cefe9917a",
        wind_speed: 0.4536704119850187,
        source_file: "5b469f234f0cf9d2772ef822",
        eastward_wind: 0.04034455966458417,
        northward_wind: 0.4290244850953516,
        air_temperature: 296.85026217228426,
        relative_humidity: 94.5689138576778,
        precipitation_rate: 0,
        surface_downwelling_shortwave_flux_in_air: 0,
        surface_downwelling_photosynthetic_photon_flux_in_air: 0
    }

    See: https://docs.terraref.org/user-manual/data-products/environmental-conditions
"""

clowder_url = "https://terraref.ncsa.illinois.edu/clowder/"
sensor_name = "UA-MAC AZMET Weather Station" # sensor_id = 438
stream_name = "Weather Observations (5 min bins)" # stream_id = 46431
season_no   = 6
output      = "Daily %s.csv" % sensor_name


# Get start and end dates for the season
def get_season_dates(season_number):
    if season_number == 4:
        return ("2017-04-20", "2017-09-18")
    elif season_number == 6:
        return ("2018-04-06", "2018-08-01")
    else:
        # This can be used to test on small scale
        return ("2018-07-01", "2018-07-10")

# Get sensor ID from Geostreams given the desired sensor name
def get_sensor_id(sensor_name):
    sens_url = clowder_url+"api/geostreams/sensors?sensor_name=%s" % sensor_name
    r = requests.get(sens_url)
    if r.status_code == 200:
        sensor_id = r.json()[0]['id']
        print("SENSOR [%s]: id %s" % (sensor_name, sensor_id))
        return sensor_id
    else:
        print("sensor not found")
        return None

# Get stream ID from Geostreams given the parent sensor ID and desired stream name
def get_stream_id(sensor_id, stream_name):
    strm_url = clowder_url+"api/geostreams/sensors/%s/streams" % sensor_id
    r = requests.get(strm_url)
    stream_id = None
    if r.status_code == 200:
        for strm_obj in r.json():
              if strm_obj['name'].startswith(stream_name):
                stream_id = strm_obj['stream_id']
                print("STREAM %s]: id %s" % (strm_obj['name'], stream_id))
                return stream_id
    if not stream_id:
        print("stream not found")
        return None

# Get datapoints from Geostreams between given dates for a specific stream
def get_datapoints(stream_id, start_date, end_date):
    dp_url = clowder_url+"api/geostreams/datapoints?stream_id=%s&since=%s&until=%s" % (stream_id, start_date, end_date)
    r = requests.get(dp_url)
    if r.status_code == 200:
        dp_list = r.json()
        print("RETRIEVED %s DATAPOINTS" % len(dp_list))
        return dp_list
    else:
        return None

# Download and write datapoints to a daily summary CSV.
def main():
    # Fetch data from Geostreams
    start_date, end_date = get_season_dates(season_no)
    sensor_id = get_sensor_id(sensor_name)
    stream_id = get_stream_id(sensor_id, stream_name)
    datapoints = get_datapoints(stream_id, start_date, end_date)

    # Create a dictionary of all 5-min observations per date
    print("Creating observation dictionary...")
    dailies = {}
    for datapoint in datapoints:
        dp_date = datapoint["start_time"][:10]
        if dp_date not in dailies:
            dailies[dp_date] = {
                "timestamps": [],
                "air_temperature": [],
                "wind_speed": [],
                "relative_humidity": [],
                "precipitation_rate": []
            }
        if datapoint["start_time"] not in dailies[dp_date]["timestamps"]:
            dailies[dp_date]["timestamps"].append(datapoint["start_time"])
            for property in ["air_temperature", "wind_speed", "relative_humidity", "precipitation_rate"]:
                if property in datapoint["properties"]:
                    dailies[dp_date][property].append(datapoint["properties"][property])

    # Aggregate daily records into single summary
    print("Summarizing daily observations...")
    def avg(val_list):
        if len(val_list) == 0:
            return
        return sum(val_list)/len(val_list)

    totals = {}
    for date in dailies:
        temps = dailies[date]["air_temperature"]
        winds = dailies[date]["wind_speed"]
        humid = dailies[date]["relative_humidity"]
        precp = dailies[date]["precipitation_rate"]

        totals[date] = {}

        if len(temps) > 0:
            totals[date]["air_temperature_min"] = min(temps)
            totals[date]["air_temperature_max"] = max(temps)
            totals[date]["air_temperature_avg"] = avg(temps)

        if len(winds) > 0:
            totals[date]["wind_speed_min"] = min(winds)
            totals[date]["wind_speed_max"] = max(winds)
            totals[date]["wind_speed_avg"] = avg(winds)


        if len(humid) > 0:
            totals[date]["relative_humidity_min"] = min(humid)
            totals[date]["relative_humidity_max"] = max(humid)
            totals[date]["relative_humidity_avg"] = avg(humid)

        if len(precp) > 0:
            totals[date]["precipitation_rate_min"] = min(precp)
            totals[date]["precipitation_rate_max"] = max(precp)
            totals[date]["precipitation_rate_avg"] = avg(precp)

    # Write daily summary to a CSV
    print("Writing %s..." % output)
    cols = ["date",
            "air_temperature_min", "air_temperature_max", "air_temperature_avg",
            "wind_speed_min", "wind_speed_max", "wind_speed_avg",
            "relative_humidity_min", "relative_humidity_max", "relative_humidity_avg",
            "precipitation_rate_min", "precipitation_rate_max", "precipitation_rate_avg"]
    with open(output, 'w') as out:
        out.write(",".join(cols)+"\n")
        dates = totals.keys()
        dates.sort()
        for date in dates:
            data = totals[date]
            out.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (
                date,
                data["air_temperature_min"] if "air_temperature_min" in data else "",
                data["air_temperature_max"] if "air_temperature_max" in data else "",
                data["air_temperature_avg"] if "air_temperature_avg" in data else "",
                data["wind_speed_min"] if "wind_speed_min" in data else "",
                data["wind_speed_max"] if "wind_speed_max" in data else "",
                data["wind_speed_avg"] if "wind_speed_avg" in data else "",
                data["relative_humidity_min"] if "relative_humidity_min" in data else "",
                data["relative_humidity_max"] if "relative_humidity_max" in data else "",
                data["relative_humidity_avg"] if "relative_humidity_avg" in data else "",
                data["precipitation_rate_min"] if "precipitation_rate_min" in data else "",
                data["precipitation_rate_max"] if "precipitation_rate_max" in data else "",
                data["precipitation_rate_avg"] if "precipitation_rate_avg" in data else ""
            ))

    print("Done.")


main()
