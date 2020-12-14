import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import pickle
import datetime as dt
import finance_functions

from sklearn.base import TransformerMixin, BaseEstimator
from sklearn.preprocessing import OneHotEncoder, LabelEncoder, Normalizer, MinMaxScaler
from sklearn.compose import ColumnTransformer

import pandas_datareader as pdr

SUBSECTORS: list=['AUTO', 'CARD']
CFs: list=['Y', 'PD']
TYPES: list=['FLT', 'SUB', 'SEQ', 'SB']
PATH="D:/OneDrive/College Notebook/Boston University/Fall Senior Year/CS 506/Project/CS506-Fall2020-Projects/consumer_abs/data"
# PATH="C:/Users/bishj/OneDrive/College Notebook/Boston University/Fall Senior Year/CS 506/Project/CS506-Fall2020-Projects/consumer_abs/data"

class ScreenLoader(object):
    def __init__(self, path=PATH, sectors=SUBSECTORS, types=TYPES, paid=CFs):
        self.path=path
        self.sectors=sectors
        self.types=types
        self.paid=paid

    def load(self, how="dict"):
        if how=="dict":
            return self._loadAsDict()
        elif how=="df":
            return self._loadAsDataFrame()

    def _loadAsDataFrame(self):
        if os.path.exists(self.path):
            df=pd.DataFrame()

            for sector in self.sectors:
                for type in self.types:
                    for cf in self.paid:
                        try:
                            df=pd.concat([df, pd.read_excel(self.path+f"/{sector}_ABS_{cf}_{type}.xlsx")], ignore_index=True)
                        except:
                            print(f"No data for {sector}_ABS_{cf}_{type}.xlsx")
            df=df[df.Ticker!='#N/A Review']
            df['Issued'] = pd.to_datetime(df['Issued'])   
            return df

    def _loadAsDict(self):
        if os.path.exists(self.path):
            screens: dict = {}

            for sector in self.sectors:
                for type in self.types:
                    for cf in self.paid:
                        try:
                            df=pd.read_excel(self.path+f"/{sector}_ABS_{cf}_{type}.xlsx")
                            df['Issued'] = pd.to_datetime(df['Issued']) 
                            df=df[df.Ticker!='#N/A Review']  
                            screens[f"/{sector}_ABS_{cf}_{type}"]=df

                        except:
                            print(f"No data for {sector}_ABS_{cf}_{type}.xlsx")


            return screens

class IssuanceLoader(object):
    def __init__(self, path=PATH, sectors=SUBSECTORS):
        self.path=path
        self.sectors=sectors

    def load(self, how="dict"):
        if how=="dict":
            return self._loadAsDict()
        elif how=="df":
            return self._loadAsDataFrame()

    def _loadAsDataFrame(self):
            if os.path.exists(self.path):
                df=pd.DataFrame()

                for sector in self.sectors:
                    df=pd.concat([df, pd.read_excel(self.path+f"/{sector}_ABS_ISSUANCE.xlsx")], ignore_index=True)

                df['Issue Date'] = pd.to_datetime(df['Issue Date'])    
                return df

    def _loadAsDict(self):
        if os.path.exists(self.path):
                issuances: dict = {}

                for sector in self.sectors:
                   df=pd.read_excel(self.path+f"/{sector}_ABS_ISSUANCE.xlsx")
                   df['Issue Date'] = pd.to_datetime(df['Issue Date'])    
                   issuances[sector]=df
                
                return issuances

class TRACEEligibleLoader(object):
    def __init__(self, path=PATH, sectors=SUBSECTORS, types=TYPES, paid=CFs):
        self.path=path
        self.sectors=sectors
        self.types= types
        self.paid=paid

    def load(self, pickle_name="traceIssuances.p"):
        if os.path.exists(self.path+f"/pickles/{pickle_name}"):
            print("Pickle found: Returning.")
            return pickle.load(open(self.path+f"/pickles/{pickle_name}", "rb"))
        else:
            #traceCategories=['CARD', 'AUTO', 'CONSUMER', "STUDENT"]
            traceCategories=['CARD', 'AUTO', 'CONSUMER']

            traceIssuanceDFs: dict = {}
                
            for i in traceCategories:
                df: pd.DataFrame = pd.read_excel(self.path + f"/ABS TRACE ISSUANCE {i}.xlsx")
                # df: pd.DataFrame = pd.read_excel(self.path + f"/TRACE Eligible {i} Loans.xlsx")
                df['Category']=i
                traceIssuanceDFs[f"{i}"] = df

            traceIssuances: pd.DataFrame=pd.concat([traceIssuanceDFs[i] for i in traceIssuanceDFs])
            traceIssuances.reset_index(inplace=True)
            traceIssuances.drop('index', inplace=True, axis=1)
        
            # traceIssuances['Is Mortgage Paid Off'].replace("Y", 1,inplace=True)
            # traceIssuances['Is Mortgage Paid Off'].replace("N", 0,inplace=True)

            traceIssuances['Delinquency Rate 60+ Days'].replace(float("nan"), 0,inplace=True)
            traceIssuances['Delinquency Rate 90+ Days'].replace(float("nan"), 0,inplace=True)
            # traceIssuances['WAC'].replace("#N/A Field Not Applicable", 0,inplace=True)
            # traceIssuances['Benchmark Spread at Issue'].replace("#N/A Field Not Applicable", 0,inplace=True)
            # traceIssuances['WAC'].replace(float("nan"), 0,inplace=True)
     
            # traceIssuances['PSA Since Issuance'].replace(float("nan"), 0,inplace=True)

            # traceIssuances=traceIssuances[(traceIssuances['Issue Date']!="#N/A Field Not Applicable") & (traceIssuances['Issue Date'] !=  "#N/A Review")] 
            traceIssuances=traceIssuances[(traceIssuances['Maturity']!="#N/A Field Not Applicable") & (traceIssuances['Maturity'] !=  "#N/A Review")]

            # Create isCallable column which says if the bond is callable or not: If we have a NaN field for the call date, the bond is not callable 
            traceIssuances['isCallable']=traceIssuances["Next Call Date"].isna()
            traceIssuances['isCallable'].replace(False, 1, inplace=True)
            traceIssuances['isCallable'].replace(True, 0, inplace=True)

            # Replace the non-callable bonds' call dates with their maturities 
            traceIssuances["Next Call Date"] = np.where(traceIssuances["Next Call Date"]=="#N/A Field Not Applicable", traceIssuances["Maturity"], traceIssuances["Next Call Date"] )
            
            traceIssuances=traceIssuances[(traceIssuances['Price at Issue']!="#N/A Field Not Applicable") & (traceIssuances['Price at Issue'] !=  "#N/A Review")]

            # Fill in missing coupons 
            traceIssuances["Cpn"] = traceIssuances["Cpn"].fillna(traceIssuances.groupby("BBG Composite")["Cpn"].transform("mean"))

            # Fill in WAL: if the pool is paid off, WAL is 0
            # traceIssuances["Current WAL"] = np.where(traceIssuances["Current WAL"].isna(), 0, traceIssuances["Current WAL"])
            traceIssuances["Original WAL"] = traceIssuances.apply(lambda x: finance_functions.calculate_WAL(x["Mortgage Original Amount"], x["Cpn"]/100, x["Issue Date"], x["Maturity"]), axis=1)

            traceIssuances.dropna(subset=['Mid Price'], inplace=True)
            # traceIssuances.drop("Is Pool Collapsed", axis=1, inplace=True)
            traceIssuances['Issue Date'] = pd.to_datetime(
                traceIssuances['Issue Date'], infer_datetime_format=True)
            traceIssuances['Maturity'] = pd.to_datetime(
                traceIssuances['Maturity'], infer_datetime_format=True)
            traceIssuances['Next Call Date']=pd.to_datetime(traceIssuances['Next Call Date'])
            traceIssuances['Next Call Date'].fillna(traceIssuances['Maturity'], inplace=True)

            traceIssuances['Next Coupon Date'] = pd.to_datetime(
               traceIssuances['Next Coupon Date'], infer_datetime_format=True)
            
            traceIssuances = traceIssuances.replace(["#N/A Field Not Applicable"], float("nan"))
            traceIssuances.dropna(inplace=True)
            
            
            traceIssuances.reset_index(inplace=True, drop=True)

            pickle.dump(traceIssuances, open(self.path+f"/pickles/{pickle_name}", "wb"))

            return traceIssuances

class IndexLoader(object):
    def __init__(self, indices=["LACCTRUU", "LAATTRUU"], path=PATH):
        self.indices= indices
        self.path= path

    def load(self, how="df"):
        if how=="df":
            return self._loadAsDataFrame()
        else:
            return self._loadAsDictionary()

    def _loadAsDictionary(self):
        if os.path.exists(self.path):
                issuances: dict = {}

                for index in self.indices:
                   df=pd.read_excel(self.path+f"/{index}.xlsx")
                   df['Date'] = pd.to_datetime(df['Date'])    
                   issuances[index]=df
                
                return issuances

    def _loadAsDataFrame(self):
        if os.path.exists(self.path):
            df = pd.read_excel(self.path+f"/{self.indices[0]}.xlsx")
            df.rename(columns={"Last Price":self.indices[0]}, inplace=True)

            for index in self.indices[1:]:
                df2=pd.read_excel(self.path+f"/{index}.xlsx")
                df2.rename(columns={"Last Price":index}, inplace=True)
                df=pd.merge(df, df2, on="Date")

            df.set_index("Date", inplace=True)
            return df

class PriceLoader(object):
    def __init__(self, path=PATH, pricesFileName="individual_bond_prices.xlsx"):
        self.path=path+"/"+pricesFileName
    

    def load(self, how="df", bonds=['DCENT 2019-A1 A1', 'AMXCA 2018-3 A', 'SYNCT 2017-2 B',
       'CARMX 2018-1 A4', 'GMCAR 2020-2 A3', 'CARMX 2019-2 B', 'FCAT 2019-1 D',
       'FORDO 2019-C A2B', 'PPWR 2018-A C', 'LLEND 2019-1A B',
       'CCCIT 2014-A5 A5', 'CCCIT 2007-A3 A3', 'COMET 2005-B3 B3',
       'NAROT 2018-A A4', 'PART 2016-2A D', 'GMCAR 2019-4 A4',
       'TCFAT 2016-1A C', 'TCFAT 2016-1A D', 'OMFIT 2016-3A A',
       'UPST 2017-2 C']):
        if how=="df":
           return self._loadAsDataFrame(bonds=bonds)
        elif how=="dict":
            return self._loadAsDictionary(bonds=bonds)

    def _loadAsDictionary(self, bonds):
        df=pd.read_excel(self.path)
        df.set_index("Date", inplace=True)
        
        bondDict: list = {}
        for bond in bonds:
            bondDict[bond]=df[bond]

        return bondDict

    def _loadAsDataFrame(self, bonds):
        df=pd.read_excel(self.path)
        df.set_index("Date", inplace=True)

        return df[bonds]

class CollateralLoader(object):
    def __init__(self, path=PATH):
        self.path=path

    def load(self, how="dict", bonds=['DCENT 2019-A1 A1', 'AMXCA 2018-3 A', 'SYNCT 2017-2 B',
       'CARMX 2018-1 A4', 'GMCAR 2020-2 A3', 'CARMX 2019-2 B', 'FCAT 2019-1 D',
       'FORDO 2019-C A2B', 'PPWR 2018-A C', 'LLEND 2019-1A B',
       'CCCIT 2014-A5 A5', 'CCCIT 2007-A3 A3', 'COMET 2005-B3 B3',
       'NAROT 2018-A A4', 'PART 2016-2A D', 'GMCAR 2019-4 A4',
       'TCFAT 2016-1A C', 'TCFAT 2016-1A D', 'OMFIT 2016-3A A',
       'UPST 2017-2 C']):
        if how=="dict":
           return self._loadAsDict(bonds)
        else:
            return self._loadAsDataFrame(bonds)

    def _loadAsDict(self, bonds):
        crossRef=pd.read_excel(PATH+"/traceissuances.xlsx")
  

        collateralDict: dict = {}
        for bond in bonds:
            cusip=crossRef[crossRef["Security Name"]==bond].CUSIP.values[0]
            df=pd.read_excel(self.path+f"/{cusip}_PDI_Collateral.xlsx", skiprows=2)
            df["Date"]=pd.to_datetime(df["Date"]).dt.to_period("M")
            df.set_index("Date", inplace=True)

            if crossRef[crossRef["Security Name"]==bond].Category.values[0]=="CARD":
                df.rename(columns={"3M":"ExcessSpread3M", "1M":"ExcessSpread1M", "30":"del30", "60":"del30", "90+":"del90Plus"}, inplace=True)
                df.drop("Seller Int", axis=1, inplace=True)
            elif crossRef[crossRef["Security Name"]==bond].Category.values[0]=="AUTO":
                df.drop("Net Interest", axis=1, inplace=True)
            else:
                df.drop("Principal", axis=1, inplace=True)
            
            df.dropna(inplace=True)

            collateralDict[bond]=df

        return collateralDict

    def _loadAsDataFrame(self, bonds):
        pass


class TRACETransformer(BaseEstimator, TransformerMixin):
    def __init__(self, categoricalColumns=["BBG Composite", "Day Count", "Category", "isCallable"], dateColumns=["Next Call Date", "Issue Date", "Maturity"], 
                        labelColumns=["CUSIP", "Security Name", "Ticker"], dropCols = [],
                        transformDates=True, keepLabels=True, normalize="MinMax"):
        self.categoricalColumns=categoricalColumns
        self.transformDates=transformDates
        self.dateColumns = dateColumns
        self.labelColumns= labelColumns
        self.dropCols = dropCols
        self.keepLabels=keepLabels
        self.normalize=normalize

    def fit_transform(self, X, y=None):
        # X.drop(self.dropCols, axis=1, inplace=True)
        X.dropna(inplace=True)
        X.reset_index(drop=True)
        
        X_transformed=X.drop(self.categoricalColumns+self.dateColumns+self.labelColumns, axis=1)
        X_cols=X_transformed.columns
        if self.normalize=="MinMax":
            scaler=MinMaxScaler()
            X_transformed = scaler.fit_transform(X_transformed)
        elif self.normalize=="Normalize":
            normal=Normalizer()
            X_transformed=normal.fit_transform(X_transformed)

        X_transformed=pd.DataFrame(X_transformed, columns=X_cols)
        X_transformed=pd.merge(X_transformed, self._categoricalTransform(X[self.categoricalColumns]), left_index=True, right_index=True)
        X_transformed=pd.merge(X_transformed, self._dateTransform(X[self.dateColumns]), left_index=True, right_index=True)
        X_transformed=pd.merge(X_transformed, self._labelTransform(X[self.labelColumns]), left_index=True, right_index=True) 
       
        return X_transformed
           
    def _categoricalTransform(self, X):
        categoricalTransforms: dict = {}

        for i in self.categoricalColumns:
            categoricalTransforms[i]=ColumnTransformer([(i, OneHotEncoder(), [X.columns.get_loc(i)])], sparse_threshold=0)

        X_transformed=pd.DataFrame(index=[i for i in range(len(X))])

        for i in categoricalTransforms:
            df=pd.DataFrame(categoricalTransforms[i].fit_transform(X))
            df.columns=categoricalTransforms[i].get_feature_names()
            X_transformed=pd.merge(X_transformed, df, left_index=True, right_index=True)

        print(X_transformed)
        return X_transformed.reset_index(drop=True)

    def _labelTransform(self, X):
        if self.keepLabels:
            for i in self.labelColumns:
                X[i]=LabelEncoder().fit_transform(X[i])

        return X.reset_index(drop=True)

    def _dateTransform(self, X):
        if self.transformDates:
            for i in self.dateColumns:
                X[i]=X[i].map(dt.datetime.toordinal)

     
        return X.reset_index(drop=True)

class SecurityLoader(object):
    def __init__(self, names=['DCENT 2019-A1 A1', 'AMXCA 2018-3 A', 'SYNCT 2017-2 B',
       'CARMX 2018-1 A4', 'GMCAR 2020-2 A3', 'CARMX 2019-2 B', 'FCAT 2019-1 D',
       'FORDO 2019-C A2B', 'PPWR 2018-A C', 'LLEND 2019-1A B',
       'CCCIT 2014-A5 A5', 'CCCIT 2007-A3 A3', 'COMET 2005-B3 B3',
       'NAROT 2018-A A4', 'PART 2016-2A D', 'GMCAR 2019-4 A4',
       'TCFAT 2016-1A C', 'TCFAT 2016-1A D', 'OMFIT 2016-3A A',
       'UPST 2017-2 C']):
        if type(names)=="str":
            self.names = [names]
        else:
            self.names=names

        self.priceLoader=PriceLoader()
        self.collateralLoader= CollateralLoader()

    def load(self):
        collateralDict = self.collateralLoader.load(bonds=self.names)
        priceDict = self.priceLoader.load(how="dict", bonds=self.names)

        securityDict: dict={}
        for i in self.names:
            df=priceDict[i].resample("m").mean()
            df=df.sort_values(0, ascending=False)
            df.index=sorted(df.index.to_period("M"), reverse=True)

            df=pd.merge(df, collateralDict[i], left_index=True, right_on="Date")
            df.rename(columns={i:"Price"}, inplace=True)
            df.dropna(subset=["Price"], inplace=True)
            # df.dropna(inplace=True)
            securityDict[i]=df


        return securityDict

class ConstructYieldCurve(object):
    def __init__(self):
        self.FRED_Codes = ["DGS1", "DGS2", "DGS3", "DGS5", "DGS7", "DGS10", "DGS20", "DGS30"]

    def load(self, start_date='01-01-2000', end_date='2020-10-30', to_months=True):
        yields: dict = {}

        for i in self.FRED_Codes:
            yields[i] = pdr.get_data_fred(i, start_date, end_date)

        df = yields[self.FRED_Codes[0]]


        for i in self.FRED_Codes[1:]:
            df = pd.merge(df, yields[i], left_index=True, right_index=True)

        if to_months:
            df=df.resample("m").mean()
            df=df.sort_values("DATE", ascending=False)
            df.index=sorted(df.index.to_period("M"), reverse=True)

        return df   

class ConstructForwardCurve(object):
    def __init__(self):
        self.FRED_Codes = ['THREEFF1', 'THREEFF2', 'THREEFF3', 'THREEFF4', 'THREEFF5', 'THREEFF6', 'THREEFF7', 'THREEFF8', 'THREEFF9', 'THREEFF10']

    def load(self, start_date='01-01-2000', end_date='2020-10-30', to_months=True):
        rates: dict = {}

        for i in self.FRED_Codes:
            rates[i] = pdr.get_data_fred(i, start_date, end_date)

        df = rates[self.FRED_Codes[0]]
        for i in self.FRED_Codes[1:]:
            df = pd.merge(df, rates[i], left_index=True, right_index=True)

        if to_months:
            df=df.resample("m").mean()
            df=df.sort_values("DATE", ascending=False)
            df.index=sorted(df.index.to_period("M"), reverse=True)

        return df   

class FannieFreddieLoader(object):
    def __init__(self):
        pass






if __name__=="__main__":
    # loader = SecurityLoader()
    # # securityDescriptive = loader.load(pickle_name="fromTRACEELIGIBLE.p")
    # securities = loader.load()
    # print(securities['LLEND 2019-1A B'])

    # loader = TRACEEligibleLoader()
    # securityDescriptive = loader.load(pickle_name="fromABSTRACEISSUANCES.p")
    
    loader = CollateralLoader()
    securities=loader.load()
    
    print(securities)

    loader = SecurityLoader()
    securities=loader.load()
    
    print(len(securities))

    # loader = SecurityLoader()
    # securities = loader.load()

    # cardDFs = {}
    # autoDFs = {}
    # consumerDFs = {}

    
    # for j in securities:
    #     if securityDescriptive[securityDescriptive["Security Name"]==j]['Category'].values == "CARD":
    #         cardDFs[j] = securities[j]
    #         securities[j].to_excel(PATH+f"/individual_securities/card/{j}.xlsx")
    #     elif securityDescriptive[securityDescriptive["Security Name"]==j]['Category'].values == "AUTO":
    #         autoDFs[j] = securities[j]
    #         securities[j].to_excel(PATH+f"/individual_securities/auto/{j}.xlsx")

    #     else:
    #         consumerDFs[j] = securities[j]
    #         securities[j].to_excel(PATH+f"/individual_securities/consumer/{j}.xlsx")





 

