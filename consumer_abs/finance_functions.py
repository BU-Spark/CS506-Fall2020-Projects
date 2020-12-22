from functions import *
from preprocessing import *
import datetime
import pandas as pd
import numpy as np
from dateutil.relativedelta import relativedelta

def calculate_WAL(principal, coupon, start_date, end_date):
    if not isinstance(start_date, datetime.datetime):
        start_date = pd.to_datetime(start_date)

    if not isinstance(end_date, datetime.datetime):
        end_date = pd.to_datetime(end_date)

    N = relativedelta(end_date,
     start_date).years
    
    unweighted_payments = [principal * coupon for i in range(N)]
    weighted_payments = np.array([i+1 for i in range(N)])@np.array(unweighted_payments)
    return (weighted_payments)/np.sum(unweighted_payments)



if __name__=="__main__":
    PATH="D:/OneDrive/College Notebook/Boston University/Fall Senior Year/CS 506/Project/CS506-Fall2020-Projects/consumer_abs/data"
    # PATH="C:/Users/bishj/OneDrive/College Notebook/Boston University/Fall Senior Year/CS 506/Project/CS506-Fall2020-Projects/consumer_abs/data"

    loader = TRACEEligibleLoader()
    collat = loader.load()
    print(collat.iloc[1085])

    bond = collat.iloc[1085]

    print(calculate_WAL(bond["Amt Out"], bond["Cpn"]/100, bond["Issue Date"], bond["Maturity"]))
