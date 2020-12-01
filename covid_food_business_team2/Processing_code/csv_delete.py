
import pandas as pd
def csv_filter(filename):
    f=pd.read_csv(filename)
    keep_col = ["location_name","street_address","city","region","postal_code","popularity_by_day"]
    new_f = f[keep_col]
    new_f.to_csv("newFile.csv", index=False)
    return "newFile.csv"
