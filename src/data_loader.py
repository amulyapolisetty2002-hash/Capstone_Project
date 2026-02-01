import pandas as pd

def load_listings(path):
    return pd.read_csv(path)

def load_demographics(path):
    return pd.read_csv(path)