import pandas as pd

# Merge listings & demographics
def merge_listings_demographics(listings, demographics):
    return listings.merge(demographics,on="zip_prefix",how="left")