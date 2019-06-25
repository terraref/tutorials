# PARTIAL TRAITS LIST
# -------------------
# canopy_height
# canopy_cover
# leaf_length 
# leaf_width
# stalk_diameter_fixed_height
# surface_temperature
# leaf_angle_alpha_src, leaf_angle_beta_src, leaf_angle_alpha_fit, leaf_angle_beta_fit, leaf_chi_src, leaf_chi_fit
# -------------------
trait <- "canopy_cover"

# install.packages('traits')
library(traits)
# get your api key at https://terraref.org/bety/users or ask David
options(betydb_key = readLines('~/.betykey', warn = FALSE),
        betydb_url = "https://terraref.ncsa.illinois.edu/bety/",
        betydb_api_version = 'beta')
trait_data <- betydb_search(trait     = trait,
                            sitename  = "~Season 6",
                            limit     = "none")
readr::write_csv(x = trait_data, path = paste(c('~/season6_', trait, '.csv'), sep=""))
