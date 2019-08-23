Second Walkthrough Notes
================
Kristina Riemer

## Introduction

The purpose of this walkthrough is to review the experimental design of
TERRA REF, and show how to find and access data on the two platforms.
The focus will be on image data, using RGB data from the project as an
example.

## Video 1: Explore Data with Traitvis Web App

Go to [website](https://traitvis.workbench.terraref.org/), which takes a
minute to load. Displays plots of various data across collection time.

As example, we’ll look at data from Season 6, which we looked at last
week, by going to “MAC Season 6” tab.

Can choose different variables and cultivars. Select “Canopy Cover” from
first dropdown and second dropdown to “PI656026” to look at cultivar
from last time. How much ground is covered increases across year with
max at 100. Hover over parts of graph to get specific values.

Change second dropdown to “None” to get all cultivars. Select “Map” tab
to look at data spatially. Shows long field in Maricopa, Arizona.

## Video 2: TERRA REF Experimental Design

*first slide*

Field is passed over by large robot called a gantry. Lot of equipment in
hanging box to collect many types of data.

Gantry goes systematically over entire field once a day. Some sensors
take data every day, like 9,000 images from RGB camera. Others more
intermittently, like hyperspectral images, because of data space limits.

*second slide* + *table*

Sensors include:

  - camera that takes pairs of red-green-blue images (**Stereo RGB**)
  - thermal infrared images (**FLIR**)
  - images at a bunch of wavelengths to get hyperspectral data
    (**VNIR/SWIR**)
  - laser that collects points on plant surfaces to create 3D image
    (**3D Laser**)
  - measures plant fluorescence (**PS II Fluor**)
  - handful of others, including environmental data such as temperature
    and light

*rest of slides*

See example data for some of these.

*traitvis webapp*

Collecting data since 2015, and are up to 8 seasons worth in that time.
Originally for sorghum, but now open to other crop species and
organizations that want to use system.

Field is split up into plots. Referenced using range by column system,
can see by hovering over map.

Can choose data within season with slider bar. Set to July 25, or
2018-07-25. Takes a moment to pull data for that date.

Currently shows canopy cover value for each plot. See for single plot
“Range 20 Column 1”. Zoom in on lower left hand part. Hover over that
and see a canopy cover value of ~18%.

These data are summarized from camera data, can see that by unselecting
“Heat Map” button on left. These are downscaled versions of infrared
data. Main image data are infrared and RGB.

## Video 3: Downloading RGB Files from Globus

We can download these individual files. TERRA REF data are on two
platforms. We pulled data from the first platform Clowder last week.
Other platform is called Globus, let’s work with that first.

All data are on Globus. Go to [website](globus.org) and log in. Need to
set up account and get acccess to Terraref collection. Instructions are
[here](https://docs.terraref.org/user-manual/how-to-access-data/using-globus-sensor-and-genomics-data).

In File Manager section. Click “Start here”, “Shared With You” tab, and
then “Terraref” option. This gives access to a bunch of files for the
project.

Go to “ua-mac” folder, which contains data from Maricopa site. Can look
at plot-level data like in map in web app. Select “Level\_1\_Plots” and
“ir\_geotiff” and “2018-07-15” and “MAC Field Scanner Season 6 Range
20 Column 1” (fourth of way down). Returns all of the infrared files for
that date and plot.

Let’s do same but focus instead on RGB images. Back up three levels,
then “rgb\_geotiff”, “2018-07-25”, “Range 20 Column 1”. Click on single
RGB image of interest within that plot on that date.
"rgb\_geotiff\_L1\_ua-mac\_2018-07-25\_\_13-30-49-010\_left.tif" is near
bottom. They’re labeled by exact time image was taken.

Can get file locally. First have to create an endpoint on local
computer. In Globus, right click on “Endpoints” on right hand side, then
“Create new endpoint” in upper right hand corner and select “Globus
Connect Personal”. This walks through how to name endpoint, get key, and
download Globus Connect Personal program on computer. I already have
one.

Go back to file in File Manager. Click “Transfer or Sync to” button on
right hand side. Click “Select a collection” and double click on my
endpoint “My University of Arizona MacBook”. Select “Desktop” on right
hand side to specify where file should go. Still have file of interest
selected, can hit Start button on lower left to transfer. Look at
Finder, can see it’s downloading. Can open it up and look at it, nice
image of plant.

Globus is good for downloading a bunch of images, from a particular date
and/or plot. These can take a long time, especially with lots of files.
But can’t see ahead of time.

## Video 4: Downloading RGB Files from Clowder

Second platform is Clowder, which is better for browsing through files.
Website is [here](https://terraref.ncsa.illinois.edu/clowder/). You can
follow along, these are publicly accessible files. Clowder is an
interface on top of Globus.

All data are organized in several ways. In spaces, collections, or
datasets. We can find same RGB tif from before. Under “Explore” tab,
select “Collections”. Look at “Season 6 (2018)”, which takes a minute to
load. Then “RGB Camera Data (Season6 Samples)”. Scroll down to third
file, can see it’s the one from the same date and time as before.

Unlike Globus, can see thumbnails and previews of images to better
browse. Can click on this and see preview of image.

Can download like before by clicking Download button. This will take a
minute to download. Move this into Desktop and Clowder\_RGB folder. Can
look at file like before.

Clowder is easier in some ways for browsing, but can be slower because
of the interface and files have to be downloaded one at a time.

Open new tab with Clowder home page. These are all the publicly
accessible files, that are sample data drawn from a couple of seasons.
Can also get an account on Clowder and access more of the data. Click on
“Sign Up” in top right hand and enter email.

Log in to my account. If I navigate to Datasets with Explore tab, can
see at the top some RGB tifs that were collected this year.

## Video 4: Download with Python

In addition to manually downloading data through Clowder or Globus, can
get programmatically using Python. Will walk through this now, can
follow along if you have the Vice app like I used last week.

Go to Cyverse Discovery Environment and open up TERRA REF RStudio app. I
will be running Python in the command line. The benefit of using this
app is that the Python modules we’ll use are already installed. Go to
Terminal tab.

First thing we’ll do is starting running Python. Specifically the newest
version of Python.

``` python
python3
```

Read in requests Python module, which is used to connect to the URL
where we’ll pull data from and makes sure there is data there.

This function needs a url and an additional parameter input. Create
object with url, like we did on Friday. Combine Clowder base URL with
the string of letters and numbers that identify file. Navigate back to
Clowder and copy that from the URL.

Can see if it works by running object, should return a 200 message.

``` python
import requests

file_url = 'https://terraref.ncsa.illinois.edu/clowder/files/5c5488fa4f0c4b0cbe7af98a'
api_key = {'key': ''}
file_request = requests.get(file_url, api_key)
file_request
```

We then want to open up the file and save it locally. Use another Python
module called io. Because the files can be big and the URL request could
time out while waiting, want to pull down file in chunks using a for
loop.

Create object for name of file we want. Copy and paste from Clowder
page.

Use io function `open`, specifying file name and that want want to write
file (`w`) as a binary file (`b`), and we’ll call it object.

The for loop does this in chunks of 1024 bytes. For every chunk that
exists, it writes it to the object.

Should then see file in file system. Can use it within this app or
export to local machine.

``` python
from io import open

file_name = 'rgb_geotiff_L1_ua-mac_2018-07-25__13-30-49-010_left.tif'
with open(file_name, 'wb') as object:
     for chunk in file_request.iter_content(chunk_size=1024):
             if chunk:
                     object.write(chunk)
```

This can be scaled up by using a list of file urls and names to download
a bunch of files.

There is also a Python module called terrautils that is specifically
designed for interacting with TERRA REF data. Documentation is
[here](https://pypi.org/project/terrautils/). Don’t have time to get
into that today.

Working with data across plots and/or across time can be difficult
because these files are large. They take a long time to download and
process.

Most researchers have this workflow. They download a few files, like RGB
images, develop this algorithm or extraction method. They then work with
TERRA REF team to implement their method in a processing pipeline for
larger amounts of data.

We’re trying to make these data more usable to anyone who wants to do
that, so feedback on either of these interfaces or any of the
documentation is very welcome. These data are on a large enough scale
that there are storage and access challenges.

In next week’s webinar, we will follow up on this work by getting some
RGB images, calculating a greenness index, and combining with trait data
like we worked with last week.

I will be sending out an email with the followup survey, if everyone
could take that, and notes from this session. This session was recorded
and I will be posting it as YouTube videos soon.
