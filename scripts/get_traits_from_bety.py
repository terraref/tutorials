import requests

bety_api = "https://terraref.ncsa.illinois.edu/bety/api/v1/search"
bety_key = "SECRET"


sitename = "Season 6" # Can also specify particular plots here
traits = ["canopy_cover", "canopy_height"]

for t in traits:
    print("Requesting %s" % t)
    full_url = "%s?trait=%s&sitename=~%s&limit=10000&key=%s" % (bety_api, t, sitename, bety_key)
    r = requests.get(full_url, timeout=None)
    if r.status_code == 200:
        print("Writing results to CSV")
        data = r.json()["data"]
        with open("%s %s.csv" % (sitename, t), 'w') as out:
            out.write("date,sitename,trait,description,value\n")
            for entry in data:
                vals = entry["traits_and_yields_view"]
                out.write("%s,%s,%s,%s,%s\n" % (vals["date"],
                                             vals["sitename"],
                                             vals["trait"],
                                             vals["trait_description"],
                                             vals["mean"]))
        print("%s done." % t)

    else:
        print("%s request failed (%s)" % (t, r.status_code))

print("Done.")
