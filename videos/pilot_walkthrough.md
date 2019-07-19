Pilot Walkthrough
================
Kristina Riemer

### Intro

Using data from TERRA REF project. Get and plot trait data, and then
same for weather data.

Will be live coding, so if you want can follow along doing what I do on
your own machine.

Will be using R + RStudio, and following R packages: traits to get data,
dplyr and lubridate for data cleaning, ggplot for plotting trait data.

Full tutorials for these at: terraref.github.io/tutorials/. I can also
send the code used here specifically if people want it.

### Traits download

Set some global options for the function used to get data Using subset
of data that’s publicly available so don’t need API key. Will need to
find and use API key to access other data.

``` r
options(betydb_url = "https://terraref.ncsa.illinois.edu/bety/", 
        betydb_api_version = 'beta', 
        betydb_key = '9999999999999999999999999999999999999999')
```

Using traits R package. Function is betydb\_query, works for several
datasets including Terra Ref.

Pulling data from Season 4, only a subset using limit because there’s a
lot of it.

``` r
library(traits)
```

    ## Registered S3 method overwritten by 'httr':
    ##   method                 from
    ##   as.character.form_file crul

    ## Registered S3 method overwritten by 'hoardr':
    ##   method           from
    ##   print.cache_info httr

``` r
season_4 <- betydb_query(sitename = "~Season 4", limit = 1000)
```

Look at dataframe.

Look at just traits available, canopy\_height is one. Using data
cleaning R package.

``` r
library(dplyr)
```

    ## 
    ## Attaching package: 'dplyr'

    ## The following objects are masked from 'package:stats':
    ## 
    ##     filter, lag

    ## The following objects are masked from 'package:base':
    ## 
    ##     intersect, setdiff, setequal, union

``` r
season_4 %>% 
  distinct(trait) %>% 
  print(n = Inf)
```

    ## # A tibble: 40 x 1
    ##    trait                        
    ##    <chr>                        
    ##  1 canopy_height                
    ##  2 relative_chlorophyll         
    ##  3 absorbance_730               
    ##  4 leaf_temperature             
    ##  5 vH+                          
    ##  6 light_intensity_PAR          
    ##  7 SPAD_880                     
    ##  8 SPAD_850                     
    ##  9 SPAD_650                     
    ## 10 leaf_angle_clamp_position    
    ## 11 ambient_humidity             
    ## 12 leaf_thickness               
    ## 13 SPAD_730                     
    ## 14 SPAD_605                     
    ## 15 SPAD_530                     
    ## 16 RFd                          
    ## 17 qP                           
    ## 18 qL                           
    ## 19 NPQt                         
    ## 20 Fs                           
    ## 21 absorbance_940               
    ## 22 absorbance_880               
    ## 23 absorbance_605               
    ## 24 absorbance_530               
    ## 25 PhiNPQ                       
    ## 26 PhiNO                        
    ## 27 roll                         
    ## 28 absorbance_850               
    ## 29 SPAD_420                     
    ## 30 LEF                          
    ## 31 FoPrime                      
    ## 32 FmPrime                      
    ## 33 Phi2                         
    ## 34 leaf_temperature_differential
    ## 35 ECSt                         
    ## 36 gH+                          
    ## 37 FvP/FmP                      
    ## 38 proximal_air_temperature     
    ## 39 pitch                        
    ## 40 absorbance_650

Want to look at just the trait values for this trait during a more
recent season, season 6. Use same function but with another argument,
trait.

``` r
canopy_height <- betydb_query(trait     = "canopy_height", 
                              sitename  = "~Season 6",
                              limit     =  250)
```

Want to plot canopy height across time, first have to get date into
correct format for plotting. Use function from another R package to
create new date column with correct formatted date.

``` r
library(lubridate)
```

    ## 
    ## Attaching package: 'lubridate'

    ## The following object is masked from 'package:base':
    ## 
    ##     date

``` r
canopy_height <- canopy_height %>% 
  mutate(formatted_date = ymd_hms(raw_date))
```

Plot canopy data. Using ggplot package.

Plot newly formatted date column on x-axis and canopy height value, in
mean column on y.

``` r
library(ggplot2)
ggplot(data = canopy_height, aes(x = formatted_date, y = mean)) +
  geom_point()
```

![](pilot_walkthrough_files/figure-gfm/unnamed-chunk-6-1.png)<!-- -->

Add axis labels, finding units from dataframe.

``` r
ggplot(data = canopy_height, aes(x = formatted_date, y = mean)) +
  geom_point() +
  labs(x = "Date", y = "Plant height (cm)")
```

![](pilot_walkthrough_files/figure-gfm/unnamed-chunk-7-1.png)<!-- -->

How to get API key:

1.  Log into betydb.org
2.  Go to data/users
3.  See your account there with API key listed

### Weather download

No special R package for getting weather data. Pull directly from
Clowder.

Data is in JSON format, so use this R package to pull down data and turn
into R data frame structure.

Create URL based on what part of data we want. Stream ID specifies
weather station, and then since and until for date range. Getting all
weather data for 2017.

``` r
library(jsonlite)
weather <- fromJSON('https://terraref.ncsa.illinois.edu/clowder/api/geostreams/datapoints?stream_id=46431&since=2017-01-02&until=2017-01-31', flatten = FALSE)
```

Pulling out subset of data called properties. Handful of weather data.

Then same reformatting of date as before. Using end\_time column from
weather dataset.

``` r
weather <- weather$properties %>% 
  mutate(formatted_date = ymd_hms(weather$end_time))
```

Plot single variable, air temperature, across time. Turns out data is
only for month of January.

``` r
ggplot(data = weather, aes(x = formatted_date, y = air_temperature)) +
  geom_point() +
  labs(x = "Date", y = "Temperature (K)")
```

![](pilot_walkthrough_files/figure-gfm/unnamed-chunk-10-1.png)<!-- -->

If we want to easily plot all 8 of the weather variables, need to
rearrange data. It’s in wide format, need it in long.

Remove a couple of unneeded columns. Then turn variable headers into a
column and put their values in weather\_value column.

``` r
library(tidyr)
weather_long <- weather %>% 
  select(-source, -source_file) %>% 
  gather(weather_variable, weather_value, -formatted_date)
```

Can now easily plot all of them using
ggplot.

``` r
ggplot(data = weather_long, aes(x = formatted_date, y = weather_value)) +
  geom_point() +
  facet_wrap(~weather_variable, scales = "free_y") +
  labs(x = "Date", y = "Weather variable")
```

![](pilot_walkthrough_files/figure-gfm/unnamed-chunk-12-1.png)<!-- -->
