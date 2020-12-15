import matplotlib.pyplot as plt
from datetime import datetime
from statistics import mean
import geopandas as gpd
import pandas as pd
import numpy as np
import requests
import time
import json

"""filters by land use codes affiliated with MA state agencies"""
def filter_luc(df, codes):
    if codes == "all":
        accepted_codes = ['910','911','912','913','914','915','916','917','918','919','920','921','922',
         '923','924','925','926','927','928','929','970','971','972','973','974','975']
    elif codes == 'transportation':
        accepted_codes = ['972','975']
    elif codes == 'housing':
        accepted_codes = ['970', '973']
    elif codes == 'other':
        accepted_codes = ['910','911','912','913','914','915','916','917','918','919','920','921','922',
         '923','924','925','926','927','928','929','971','974']
    elif codes == "vacant-all":
        accepted_codes = ['973','974','975']
    elif codes == "vacant-transportation":
        accepted_codes = ['975']
    elif codes == "vacant-housing":
        accepted_codes = ['973']
    elif codes == "vacant-other":
        accepted_codes = ['974']
    return df[(df['luc_1'].isin(accepted_codes))|(df['luc_2'].isin(accepted_codes))|(df['luc_adj_1'].isin(accepted_codes))|(df['luc_adj_2'].isin(accepted_codes))]


def filter_transit_friendly(df):
    return df.query('numTransitStops > 10')

def filter_land_sqft(df):
    return df.query('available_land_sqft > 200000')