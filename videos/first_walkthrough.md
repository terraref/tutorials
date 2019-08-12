First Walkthrough Notes
================
Kristina Riemer

## Video 1: Objectives + TERRA REF Overview + Getting Started

#### Objectives

These walkthroughs are a hands-on introduction to how to use data
produced by TERRA REF project.

The intended audience is community members and anyone interested in
these data.

These live walkthroughs will be turned into video tutorials that can be
viewed at any time. They will be put on YouTube, and I’ll provide links
once they’re ready.

#### Project overview

TERRA REF is a project funded by ARPA-E to gather phenomic and genomic
data on plant crops. An extensive series of sensors are used to collect
trait and image data on outdoor experimental plots. Weather stations
also collect weather data. And crop genomes are being sequenced, with
these genomic data being provided.

These tutorials are to make these data accessible and useable. I will
provide an overview of how to use computational tools to get these data,
and combine, plot, and analyze them.

We have written online tutorials
[here](https://terraref.github.io/tutorials/). These walkthroughs and
videos complement those materials, which are growing and improving
continually.

#### VICE setup and use

Launching TERRA REF app on VICE:

1.  Google “Cyverse” and click link to website
2.  Select Products tab
3.  Under “Discovery Environment”, select Launch button
4.  Hit “Log in with your CyVerse ID” button
5.  Log in with CyVerse credentials (username and password)
6.  Select “Apps”, type in “terra”, select “TERRA REF Rstudio 3.6.0”,
    and “Use App”
7.  Click “Launch Analysis”, hit Analysis button, and select arrow
    button in Analyses window
8.  Wait patiently
9.  Sign into RStudio using username: rstudio and password: rstudio1

Reopen running TERRA REF instance:

1.  Google “Cyverse” and click link to website
2.  Select Products tab
3.  Under “Discovery Environment”, select Launch button
4.  Hit “Log in with your CyVerse ID” button
5.  Log in with CyVerse credentials (username and password)
6.  Open Analyses window and hit arrow button to open up RStudio

## Video 2: Downloading Trait Data

Use `traits` R package to download TERRA REF trait data. Package
developed by rOpenSci more generally for downloading trait data.
Implemented for several other trait databases in addition to TERRA REF.
Package is on CRAN.

``` r
library(traits)
```

    ## Registered S3 method overwritten by 'httr':
    ##   method                 from
    ##   as.character.form_file crul

    ## Registered S3 method overwritten by 'hoardr':
    ##   method           from
    ##   print.cache_info httr

First set some global options that will apply across all instances of
using this package’s function. Limits redundant typing.

Specify:

  - Where from internet to download from (NCSA is where TERRA REF data
    is)
  - Want to use most recent version of API for data
  - Using public API key to access data, will show later how to access
    your own API key to get to more data

<!-- end list -->

``` r
options(betydb_url = "https://terraref.ncsa.illinois.edu/bety/", 
        betydb_api_version = 'beta', 
        betydb_key = '9999999999999999999999999999999999999999')
```

Function from `traits` is `betydb_query`. Getting first 1000 rows of
data from fourth season. Can get all by not setting `limit` argument,
but it takes a while.

``` r
season_4 <- betydb_query(sitename = "~Season 4", 
                         limit = 1000)
```

Each row is trait observation. Lots of info, including location (`lat`,
`lon`), species, time, type of `trait`, and value (`mean`).

## Video 3: Available Traits

Look at which traits are available. Using popular data cleaning R
package `dplyr`.

Take dataframe with trait observations, return all the unique values
from trait column with `distinct` and print them all out.

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

    ## # A tibble: 20 x 1
    ##    trait                           
    ##    <chr>                           
    ##  1 leaf_desiccation_present        
    ##  2 lodging_present                 
    ##  3 surface_temperature             
    ##  4 leaf_stomatal_conductance       
    ##  5 flag_leaf_emergence_time        
    ##  6 flowering_time                  
    ##  7 grain_stage_time                
    ##  8 aboveground_dry_biomass         
    ##  9 aboveground_biomass_moisture    
    ## 10 aboveground_fresh_biomass       
    ## 11 dry_matter_fraction             
    ## 12 harvest_lodging_rating          
    ## 13 leaf_temperature                
    ## 14 stem_elongated_internodes_number
    ## 15 canopy_height                   
    ## 16 planter_seed_drop               
    ## 17 stand_count                     
    ## 18 panicle_height                  
    ## 19 emergence_count                 
    ## 20 seedling_emergence_rate

Focus on one trait, canopy\_height, from more recent season.

``` r
canopy_height <- betydb_query(trait     = "canopy_height", 
                              sitename  = "~Season 6",
                              limit     =  250)
```

## Video 4: Plot Trait Data

Want to plot canopy height across time using `raw_date`. Column is in
wrong format, so first use a function from `lubridate` package to
transform.

Add this as new column using `mutate` from `dplyr`.

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

Use common R package `ggplot` to plot these data. Specify dataframe,
then what axes should be with `aes` argument. Use scatter plot function.

``` r
library(ggplot2)
ggplot(data = canopy_height, aes(x = formatted_date, y = mean)) +
  geom_point()
```

![](first_walkthrough_files/figure-gfm/unnamed-chunk-7-1.png)<!-- -->

Add better axis labels. Can find canopy\_height units from `units`.

``` r
ggplot(data = canopy_height, aes(x = formatted_date, y = mean)) +
  geom_point() +
  labs(x = "Date", y = "Plant height (cm)")
```

![](first_walkthrough_files/figure-gfm/unnamed-chunk-8-1.png)<!-- -->

Can do same plot across all the traits in the original dataframe from
fourth season. Do same column time transformation.

``` r
season_4 <- season_4 %>%
  mutate(formatted_date = ymd_hms(raw_date))
```

Create plot same as for canopy\_height, but add in `facet_wrap` to
produce one per unique trait type.

Some data only take at one or a few times of year.

``` r
ggplot(data = season_4, aes(x = formatted_date, y = mean)) +
  geom_point() +
  facet_wrap(~trait, scales = "free_y")
```

![](first_walkthrough_files/figure-gfm/unnamed-chunk-10-1.png)<!-- -->

## Video 5: Access API Key

Each beta user will have their own unique key. Do not share these with
anyone.

Find the key:

1.  Log into betydb.org
2.  Go to data/users
3.  See your account there with API key listed
