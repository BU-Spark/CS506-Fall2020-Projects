
import pandas as pd
def csv_filter(filename):
    f=pd.read_csv(filename)
    keep_col = ['businessname','licenseno','licenseno','issdttm','expdttm',
                "licstatus","licensecat","descript","result","violation","violdesc","violdttm","violstatus","address","city","state","zip"]
    new_f = f[keep_col]
    new_f.to_csv("newFile.csv", index=False)
    return "newFile.csv"
