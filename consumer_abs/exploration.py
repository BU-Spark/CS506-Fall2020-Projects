
import matplotlib.dates as mdates
import datetime as dt
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from preprocessing import*

import statsmodels.api as sm
import statsmodels.formula.api as smf
from sklearn.compose import ColumnTransformer

import seaborn as sns
sns.set_style("dark")

SUBSECTORS: list = ['AUTO', 'CARD']
CFs: list = ['Y', 'PD']
TYPES: list = ['FLT', 'SUB', 'SEQ', 'SB']
PATH="D:/OneDrive/College Notebook/Boston University/Fall Senior Year/CS 506/Project/CS506-Fall2020-Projects/consumer_abs/data"
# PATH = "C:/Users/bishj/OneDrive/College Notebook/Boston University/Fall Senior Year/CS 506/Project/CS506-Fall2020-Projects/consumer_abs/data"


def linreg(traceIssuances):

    X = pd.get_dummies(traceIssuances[['Delinquency Rate 60+ Days',
                                       'Delinquency Rate 90+ Days', 'isCallable']])
    y = traceIssuances['Cpn']

    # X = pd.get_dummies(traceIssuances[['BBG Composite', 'isCallable']])
    results = sm.OLS(y, X).fit()

    print(results.summary())


def kmeans(traceIssuances):
    from sklearn.cluster import KMeans
    from sklearn.preprocessing import MinMaxScaler
    from sklearn.decomposition import PCA
    from sklearn.preprocessing import OneHotEncoder, LabelEncoder

    X_Cols = ['Cpn', 'Amt Out', 'BBG Composite', 'Current WAL', 'Day Count',
            'Delinquency Rate 60+ Days', 'Delinquency Rate 90+ Days', 'Issue Date', 'Maturity', 'Mid Price', 'Mortgage Original Amount',
            'Next Call Date', 'Next Coupon Date',
            'Price at Issue', 'Category',
            'isCallable']

    X = traceIssuances.copy()[X_Cols]
    X.dropna(inplace=True)

    encoder = OneHotEncoder()
    categoricalColumns=["BBG Composite", "Day Count", "Category", "isCallable"]

    categoricalTransforms: dict = {}

    for i in categoricalColumns:

        categoricalTransforms[i]=ColumnTransformer([(i, OneHotEncoder(), [X.columns.get_loc(i)])], sparse_threshold=0)



    dateColumns=["Next Call Date", "Next Coupon Date", "Issue Date", "Maturity"]
    dateTransforms: dict = {}

    for i in dateColumns:
        X[i]=X[i].map(dt.datetime.toordinal)
        dateTransforms[i]=ColumnTransformer([(i, LabelEncoder(), [X.columns.get_loc(i)])])

    scaler = MinMaxScaler()
    X_transformed=X.drop(categoricalColumns+dateColumns, axis=1)
    X_cols=X_transformed.columns
    X_transformed = scaler.fit_transform(X_transformed)
    X_transformed=pd.DataFrame(X_transformed, columns=X_cols)
    

    for i in categoricalTransforms:
        df=pd.DataFrame(categoricalTransforms[i].fit_transform(X))
        df.columns=categoricalTransforms[i].get_feature_names()
        X_transformed=pd.merge(X_transformed, df, left_index=True, right_index=True)


    kmodel = KMeans(n_clusters=5)
    y_pred = kmodel.fit_predict(X_transformed)

    vals, counts = np.unique(y_pred, return_counts=True)
    X_Cols.append('CUSIP')


    sampleSelection = traceIssuances[X_Cols].copy()
    sampleSelection.dropna(inplace=True)
    sampleSelection.reset_index(inplace=True)
    sampleSelection.drop('index', inplace=True, axis=1)
    sampleSelection['cluster'] = y_pred


    cols = ['Cpn',  'Mortgage Original Amount',  'BBG Composite',
            'Delinquency Rate 60+ Days', 'Delinquency Rate 90+ Days', 'Category']


    rows = vals
    myFmt = mdates.DateFormatter('%Y')


    fig, axes = plt.subplots(ncols=len(vals), nrows=len(cols), figsize=(20, 15))

    for j, i in enumerate(cols):
        for l, k in enumerate(vals):
            sample = sampleSelection[sampleSelection['cluster'] == k][i].iloc[0]

            if type(sample) == str or type(sample) == np.bool_:
                axes[j, l].barh(sampleSelection[sampleSelection['cluster'] == k][i].unique(), sampleSelection[sampleSelection['cluster'] == k]
                                [i].value_counts()/np.sum(sampleSelection[sampleSelection['cluster'] == k][i].value_counts()), linewidth=0)
            elif type(sample) == pd.Timestamp:
                axes[j, l].hist(sampleSelection[sampleSelection['cluster']
                                                == k][i], density=True, orientation='horizontal')
                axes[j, l].yaxis.set_major_formatter(myFmt)
            else:
                axes[j, l].hist(sampleSelection[sampleSelection['cluster']
                                                == k][i], density=True, orientation='horizontal')

            axes[j, l].tick_params(axis='x', labelrotation=90)
            axes[j, l].autoscale()


    pad = 5
    for ax, col in zip(axes[0], vals):
        ax.annotate("Cluster " + str(col+1), xy=(0.5, 1), xytext=(0, pad),
                    xycoords='axes fraction', textcoords='offset points',
                    size='large', ha='center', va='baseline')

    for ax, row in zip(axes[:, 0], cols):
        ax.annotate(row, xy=(0, 0.5), xytext=(-ax.yaxis.labelpad - pad, 0),
                    xycoords=ax.yaxis.label, textcoords='offset points',
                    size='large', ha='right', va='center')

    fig.autofmt_xdate()
    fig.tight_layout()
    plt.savefig(PATH+f"/clusterAttributes.png")
    plt.show()



if __name__=="__main__":
    loader = TRACEEligibleLoader()
    traceIssuances = loader.load()
    X=TRACETransformer().fit_transform(traceIssuances)

    kmeans(traceIssuances)
    
