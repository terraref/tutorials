Third Walkthrough Notes
================
Kristina Riemer

summarize what happened last time

## Video 1: Plot Single RGB Image

Go to globus.org and login. In Terraref Collection, go to ua-mac for the
Arizona site data, Level\_1\_Plots for data organized by date, and
rgb\_geotiff for RGB images. We want to look at single image for May 1,
2018 in a particular plot. Select 2018-05-01 and then MAC Field Scanner
Season 6 Range 19 Column 1. Select a random file to download. Use
Transfer or Sync to button and select own endpoint and Downloads folder
to transfer to computer.

While that’s downloading, which will take a minute, open up Vice app in
CyVerse Discovery Environment. Use instance of TERRA REF Rstudio 3.6.0
that’s already running. Select Import button in RStudio IDE and browse
to location of newly downloaded file and hit OK. This will take a moment
to load. (Might need to plot locally because it may take too long)

Geotiff files are gridded spatial data, which are of raster format. So
use raster R package to read into R using `raster`. And then can look at
how it looks with `plot`.

``` r
library(raster)
single_RGB <- raster("rgb_geotiff_L1_ua-mac_2018-05-01__11-24-40-779_left.tif")
plot(single_RGB)
```

## Video 2: Access Full Field Images

That’s just a single image taken in that particular plot on the first of
May. If we want all the images from a day combined, there’s processed
data files that hold that in Clowder.

Go to <https://terraref.ncsa.illinois.edu/clowder/> to access Clowder.
We’re using all public images so do not need to log in. Navigate to a
file by going Spaces -\> Sample Data 2019 -\> (may have to “View All
Datasets”) Season 6 May 2018 full field RGB Geotiffs -\> click on first
one.

This is called a mosiac. Combines all the images from that day, even if
they aren’t continous. This is a lower resolution version of all images,
it would be a much larger file if not. The file we just plotted is
within this.

We could download this file manually using Download button. Instead,
going to do programmatically using Python like we did last time (to set
us up later to download a set of these).

Go to Vice app. In command line (Terminal tab), start up Python. First
set up connection to URL with requests library. Type in the first part
of the URL, and then copy and paste the unique part.

``` python
python3
import requests

file_url = 'https://terraref.ncsa.illinois.edu/clowder/api/files/5c81a03e4f0c0ca8052b2635?dataset=5c81709a4f0c78f6486d686c&space=5c50512a4f0c436195b9ad67'
api_key = {'key': ''}
file_request = requests.get(file_url, api_key)
file_request
```

Then read in `open` function. Set up file name by copy and pasting from
file page. Read in in chunks, which will take a minute.

``` python
from io import open

file_name = 'fullfield_L1_ua-mac_2018-05-01_rgb_stereovis_ir_sensors_fullfield_sorghum6_shade_may2018_thumb.tif'
with open(file_name, 'wb') as object:
     for chunk in file_request.iter_content(chunk_size=1024):
             if chunk:
                     object.write(chunk)
```

We can then plot this like we did for the other RGB image. Start new R
script to hold all code. Because this is a larger image, it will take a
minute to plot. Can see that long and skinny shape of the entire field.

``` r
library(raster)
full_field <- raster("fullfield_L1_ua-mac_2018-05-01_rgb_stereovis_ir_sensors_fullfield_sorghum6_shade_may2018_thumb.tif")
plot(full_field)
```

## Video 3: Clip Full Field Image

We’re only interested in that one plot that we looked at an image from
before. So we need to clip this raster down to only the extent of that
plot.

We need to get a vector for that plot. We will pull the site information
using the `traits` package like we did before. Set up options and use
`betydb_query`.

First get plot vector. Now pulling site info from Bety, like we did for
trait data.

``` r
library(traits)
options(betydb_url = "https://terraref.ncsa.illinois.edu/bety/",
        betydb_api_version = 'beta', 
        betydb_key = '9999999999999999999999999999999999999999')

plot_data <- betydb_query(table     = "sites",  
                      sitename  = "MAC Field Scanner Season 6 Range 19 Column 10")
```

We can look at that dataframe, contains all the information for that
location, including site and plot info.

These data are pulled from our database, which is called BETYdb. If
Google “terra ref betydb”, it will be the first hit. This is a pretty
nice interface to data, and another way to explore what is available.
There is a schema for this database, which contains all the tables and
info about their columns, data types, and relationships. Click Docs and
Schema to look at this. If we click on Sites table, then can see overlap
with column names. This can be a useful tool.

Need to make a spatial object out of the plot info. Use sf package to do
this, which is the vector analogue of raster package. First function
include argument to set coordinate reference system as WGS84.
Multipolygon object to points to spatial object.

``` r
library(sf)
site_shape <- st_as_sfc(plot_data$geometry, crs = 4326)
site_poly <- st_cast(site_shape, "POINT")
site_clip <- as(site_poly, "Spatial")
```

Replot fullfield with plot vertices. Can do sanity check for this
location by comparing to traitvis app map.

``` r
plot(full_field)
points(site.clip)
```

Can use `crop` from raster package to cut down to our desired plot only.
Expects first argument is raster to be clipped, and second object
specifies extent.

``` r
full_field_crop <- crop(full_field, site.clip)
plot(full_field_crop)
```

## Video 4: Calculate Greenness Index

Let’s say we want to calculate a greenness index for this plot. These
RGB images have three bands, can see under band. `raster` reads in first
band, which is red, if none is specified.

We want to read in both the red and green band to do calculation. Change
band argument for both raster objects. Crop them both to get just plot
extent, and can plot to see that they’re different.

``` r
full_field

full_field_red <- raster("fullfield_L1_ua-mac_2018-05-01_rgb_stereovis_ir_sensors_fullfield_sorghum6_shade_may2018_thumb.tif", band = 1)
full_field_green <- raster("fullfield_L1_ua-mac_2018-05-01_rgb_stereovis_ir_sensors_fullfield_sorghum6_shade_may2018_thumb.tif", band = 2)

crop_red <- crop(full_field_red, site_clip)
crop_green <- crop(full_field_green, site_clip)

plot(crop_red)
plot(crop_green)
```

Now that we have our clipped red and green rasters, we can calculate an
index called the normalized green-red difference index. Adding two
rasters, subtracting two rasters, and then dividing them.

Add and subtract is between each corresponding cell of the raster, then
`cellStats` does operation across all cell values.

``` r
add <- crop_red + crop_green
numerator <- cellStats(add, stat = "sum")
subtract <- crop_red - crop_green
denominator <- cellStats(subtract, stat = "sum")
greenness <- numerator / denominator
```

## Video 5: Repeat Calculation on Multiple Files

So now we have a greenness value for this plot for a single date in May.
We can repeat this for several dates across the month, in a more
efficient way. First I set up an object containing the copy and paste
values (URL and file name) from each Clowder file of interest. Did for
four dates across the month.

Each file is a dictionary with id and filename, and they’re put into the
list
`files`.

``` python
files = [{"id": "5c81a03e4f0c0ca8052b2635?dataset=5c81709a4f0c78f6486d686c&space=", 
"filename": "fullfield_L1_ua-mac_2018-05-01_rgb_stereovis_ir_sensors_fullfield_sorghum6_shade_may2018_thumb.tif"}, 
{"id": "5c81a0314f0c78f6486d68ef?dataset=5c81709a4f0c78f6486d686c&space=", 
"filename": "ullfield_L1_ua-mac_2018-05-02_rgb_stereovis_ir_sensors_fullfield_sorghum6_shade_may2018_thumb.tif"}, 
{"id": "5c819ffd4f0c0ca8052b25c0?dataset=5c81709a4f0c78f6486d686c&space=", 
"filename": "ullfield_L1_ua-mac_2018-05-18_rgb_stereovis_ir_sensors_fullfield_sorghum6_sun_may2018_thumb.tif"}, 
{"id": "5c819fe04f0c82bd931b4b5d?dataset=5c81709a4f0c78f6486d686c&space=", 
"filename": "fullfield_L1_ua-mac_2018-05-28_rgb_stereovis_ir_sensors_plots_sorghum6_shade_rgb_eastedge_mn_thumb.tif"}]
```

Connect to URL with requests and download with `open` like before, all
in a big for loop for each of the files.

This will take a minute because it’s doing what we did before for three
files.

``` python
for file in files: 
  file_request = requests.get('https://terraref.ncsa.illinois.edu/clowder/api/files/' + file["id"], api_key)
  with open(file["filename"], 'wb') as object: 
    for chunk in file_request.iter_content(chunk_size=2014): 
      if chunk: 
        object.write(chunk)
```

Now that we have all our files, we want to calculate greenness for each
of them. To avoid having to type everything we did before over and over
again, will create function to read in each file (two bands), clip them,
and calculate value.

``` r
get_greenness <- function(file_name, clip_coords){
  band_red <- raster(file_name, band = 1)
  crop_red <- crop(band_red, clip_coords)
  band_green <- raster(file_name, band = 2)
  crop_green <- crop(band_green, clip_coords)
  add <- crop_red + crop_green
  numerator <- cellStats(add, stat = "sum")
  subtract <- crop_red - crop_green
  denominator <- cellStats(subtract, stat = "sum")
  greenness <- numerator / denominator
  return(greenness)
}
```

We want to put in, as `file_name`, a list of our files. Use `list.files`
to do that, and a wildcard to specify we want all files in current
directory that are geotiffs.

``` r
image_file_names <- list.files(".", pattern = "*.tif")
```

Then run greenness function across all files in that list, using
previous plot vector to clip. Last argument is to just not include the
names of the files in results. Get four greenness values as
expected.

``` r
greennesses <- sapply(image_file_names, get_greenness, site_clip, USE.NAMES = FALSE)
```

We want to put these values into a dataframe with another column, dates,
so we can later combine this with other data based on day. Just writing
out each date by hand, but there’s programmatic ways using regex to pull
date values out of file names.

Need to turn the date values into date objects like we’ve done before so
they can be combined and plotted more easily. Create new column with
dplyr.

``` r
greenness_df <- data.frame(date = c('2018-05-01', '2018-05-02', '2018-05-18', '2018-05-28'), greenness = greennesses)

library(dplyr)
greenness_df <- greenness_df %>% 
  mutate(day = as.Date(date))
```

## Video 6: Compare Greenness to Trait Value

What we want to do is compare a trait value, canopy cover, to this
greenness metric. We can pull in canopy cover values with `traits`
package like we did the first webinar. The options have already been
set. Also need to turn date into date object.

``` r
cover <- betydb_query(trait = "canopy_cover", 
                      date = "~2018 May", 
                      limit = "none")

cover_day <- cover %>% 
  mutate(day = as.Date(raw_date))
```

Because there are multiple canopy cover values across the entire field,
we’re going to get the mean and average for each day. Using `dplyr`,
group by day and then summarize across those.

``` r
cover_daily <- cover_day %>% 
  group_by(day) %>% 
  summarize(mean_cover = mean(mean))
```

Then combine these with the greenness values by day. Doing left join
because we only want to keep the dates in the greenness dataframe, there
are more in the canopy cover one.

``` r
combined_values <- left_join(greenness_df, cover_daily, by = "day") 
```

Plot to see if there’s any relationship between the two.

``` r
library(ggplot2)
ggplot(combined_values, aes(x = mean_cover, y = greenness)) +
  geom_point()
```

Not much of a relationship. What could be done better here?

  - Do for more dates
  - Use canopy cover from specific plot only
  - Do for more plots
