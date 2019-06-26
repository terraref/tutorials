import os, requests, csv
from datetime import datetime

"""
Translate data downloaded using get_traits_from_bety.r into:

    culivarID, sitename, day, trait

"""

season_no    = 6
trait        = "canopy_height"
value_column = "mean" # column containing actual measurement

# Overwrite this filename if necessary
bety_data = "season%s_%s.csv" % (season_no, trait)
out_data = bety_data.replace(".csv", "_formatted.csv")


# Load mapping from sitename (plot) to cultivar (genotype)
def load_cultivar_lookups(season_no):
    if season_no == 4:
        source_file = "cultivars_s4_2017.csv"
    elif season_no == 6:
        source_file = "cultivars_s6_2018.csv"
    else:
        print("No cultivar lookup available for Season %s" % season_no)

    if not os.path.exists(source_file):
        print("Cannot find lookup file %s" % source_file)
        exit()

    lookup = {}
    with open(source_file, 'r') as source_data:
        for l in source_data.readlines():
            (sitename, cultivar) = l.rstrip().split(",")
            lookup[sitename] = cultivar

    return lookup

# Get start and end dates for the season
def get_season_dates(season_number):
    if season_number == 4:
        return ("2017-04-20", "2017-09-18")
    elif season_number == 6:
        return ("2018-04-06", "2018-08-01")
    else:
        # This can be used to test on small scale
        return ("2018-07-01", "2018-07-10")

# Get days since start of season
def get_days_since(start_date, row_date):
    date_format = "%Y-%m-%d"
    start = datetime.strptime(start_date, date_format)
    end = datetime.strptime(row_date, date_format)
    delta = end - start
    # First day of season should be Day 1, not Day 0
    return delta.days + 1


def main():
    lookups = load_cultivar_lookups(season_no)
    start_day = get_season_dates(season_no)[0]

    print("Reformatting %s into %s" % (bety_data, out_data))
    out = open(out_data, 'w')
    out.write("cultivar,sitename,day,%s\n" % trait)
    with open(bety_data, 'r') as input:
        csv_reader = csv.DictReader(input, delimiter=",")
        curr_row = 0
        for row in csv_reader:
            if curr_row > 0:
                cols = [
                    lookups[row["sitename"]],
                    row["sitename"],
                    str(get_days_since(start_day, row["raw_date"][:10])),
                    str(row[value_column])
                ]
                out.write(",".join(cols)+"\n")
            curr_row += 1
    out.close()

    print("Done.")

main()
