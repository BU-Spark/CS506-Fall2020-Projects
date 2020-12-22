import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style("dark")

SUBSECTORS: list=['AUTO', 'CARD']
CFs: list=['Y', 'PD']
TYPES: list=['FLT', 'SUB', 'SEQ', 'SB']
PATH="D:/OneDrive/College Notebook/Boston University/Fall Senior Year/CS 506/Project/CS506-Fall2020-Projects/consumer_abs/Plots"

from preprocessing import ConstructYieldCurve, ScreenLoader, IssuanceLoader, TRACEEligibleLoader

def plotMeanIssuanceByYear(path=PATH, saveAs=None):
    loader=IssuanceLoader(path)
    issuanceDataFrames=loader.load()

    fig = plt.figure(figsize=(15,10))

    for i in issuanceDataFrames:
        mean_issuance_by_year=issuanceDataFrames[i].groupby(issuanceDataFrames[i]['Issue Date'].map(lambda x: x.year)).mean()
        amount_in_millions=mean_issuance_by_year['Mortgage Original Amount']/1e6
        
        plt.plot(mean_issuance_by_year.index, amount_in_millions, label = i)
        
    plt.legend()
    plt.title('Mean ABS Issuance by Year')
    plt.ylabel('Mean Issuance Amount ($M USD)')
    plt.xlabel("Year")
    plt.tight_layout()
    fig.subplots_adjust(top=0.88)
    
    if saveAs is not None:
            plt.savefig(path+f"/{saveAs}.png")

    _=plt.show()

def plotDistributionOfIssuancesByYear(sectors=SUBSECTORS, types=TYPES, path=PATH, saveAs=None):
    fig, axes = plt.subplots(nrows=len(sectors), ncols=len(types), figsize=(20,10))

    loader=ScreenLoader(path)
    SECF_DF= loader.load(how="df")

    
    for j, i in enumerate(sectors):
        for l, k in enumerate(types):
            df=SECF_DF[(SECF_DF['Sub Sector'].str.contains(i)) & (SECF_DF['Type'].str.contains(k))]['Issued'].dt.year
            axes[j,l].hist(df, bins=np.unique(df), density=False, )
            axes[j,l].margins(x=0)
            
    pad=5
    for ax, col in zip(axes[0], types):
        ax.annotate(col, xy=(0.5, 1), xytext=(0, pad),
                    xycoords='axes fraction', textcoords='offset points',
                    size='large', ha='center', va='baseline')

    for ax, row in zip(axes[:,0], sectors):
        ax.annotate(row, xy=(0, 0.5), xytext=(-ax.yaxis.labelpad - pad, 0),
                    xycoords=ax.yaxis.label, textcoords='offset points',
                    size='large', ha='right', va='center')
        
    fig.suptitle('Distribution of Issuances by Year')
    fig.tight_layout()  
    fig.subplots_adjust(top=0.88)

    if saveAs is not None:
            plt.savefig(path+f"/{saveAs}.png")
    _=plt.show()
        
def plotTopNIssuancesByCouponType(path=PATH, sectors=SUBSECTORS, N=10, saveAs=None):
    fig, axes = plt.subplots(ncols=len(SUBSECTORS), figsize=(20,10))
    loader=ScreenLoader(path)
    SECF_DF= loader.load(how="df")

    for j,i in enumerate(sectors):
        axes[j].bar(SECF_DF[SECF_DF['Sub Sector'].str.contains(i, na=False)].Type.value_counts().index[:10], SECF_DF[SECF_DF['Sub Sector'].str.contains(i, na=False)].Type.value_counts()[:N])
        axes[j].set_xlabel('Coupon Type')
        axes[j].set_ylabel('Number of Issuances')
        
        axes[j].set_title(i)
        
    fig.suptitle('Top 10 Card & Auto ABS Issuances by Coupon Type')

    fig.subplots_adjust(top=0.88)
    plt.tight_layout()
    if saveAs is not None:
            plt.savefig(path+f"/{saveAs}.png")
    _=plt.show()

def plotHeatMapIssuancesByCouponType(path=PATH, sectors=SUBSECTORS, types=TYPES, saveAs=None):
    loader=ScreenLoader(path)
    SECF_DF= loader.load(how="df")

    fig, ax = plt.subplots(ncols=2, figsize=(20,15))

    cmap=plt.get_cmap('Blues')

    for num, subsector in enumerate(sectors):
        heatmapData: list = []

        for i in types:
            heatmapData.append([len(SECF_DF[(SECF_DF['Type'].str.contains(i, na=False)) & (SECF_DF['Type'].str.contains(j, na=False)) & (SECF_DF['Sub Sector'].str.contains(subsector, na=False))]) for j in types])

        heatmapData=np.array(heatmapData)
        
        im = ax[num].imshow(heatmapData, cmap=cmap)
        ax[num].set_xticks(np.arange(len(types)))
        ax[num].set_yticks(np.arange(len(types)))

        ax[num].set_xticklabels(types)
        ax[num].set_yticklabels(types)

        plt.setp(ax[num].get_xticklabels(), rotation=45, ha="right",
                rotation_mode="anchor")
        
        ax[num].set_title(f"{subsector} Number of Issuances by Coupon Type")

        for i in range(len(types)):
            for j in range(len(types)):
                if heatmapData[i,j]==0:
                    text = ax[num].text(j, i, heatmapData[i, j],
                                ha="center", va="center", color="w")

                else:
                    text = ax[num].text(j, i, heatmapData[i, j],
                                ha="center", va="center", color="black")

    fig.subplots_adjust(top=0.88)
    fig.tight_layout()
    if saveAs is not None:
            plt.savefig(path+f"/{saveAs}.png")
    _=plt.show()

def plotAverageDollarAmtIssuedByCouponType(path=PATH, sectors=SUBSECTORS, types=TYPES, saveAs=None):
    loader=ScreenLoader(path)
    SECF_DF= loader.load(how="df")

    fig, ax = plt.subplots(ncols=2, figsize=(20,15))

    cmap=plt.get_cmap('Blues')

    for num, subsector in enumerate(sectors):
        heatmapData: list = []

        for i in types:
            heatmapData.append([(SECF_DF[(SECF_DF['Type'].str.contains(i, na=False)) & (SECF_DF['Type'].str.contains(j, na=False)) & (SECF_DF['Sub Sector'].str.contains(subsector, na=False))]['Original Amount']).mean() for j in types])

        heatmapData=np.array(heatmapData)
        heatmapData=np.nan_to_num(heatmapData)
        heatmapData=np.round(heatmapData/1e9, 1)
        
        im = ax[num].imshow(heatmapData, cmap=cmap)
        ax[num].set_xticks(np.arange(len(types)))
        ax[num].set_yticks(np.arange(len(types)))

        ax[num].set_xticklabels(types)
        ax[num].set_yticklabels(types)

        plt.setp(ax[num].get_xticklabels(), rotation=45, ha="right",
                rotation_mode="anchor")
        
        ax[num].set_title(f"{subsector} Average Dollar Amount Issued by Coupon Type (USD Billions)")

        for i in range(len(types)):
            for j in range(len(types)):
                if heatmapData[i,j]==0:
                    text = ax[num].text(j, i, heatmapData[i, j],
                                ha="center", va="center", color="w")

                else:
                    text = ax[num].text(j, i, heatmapData[i, j],
                                ha="center", va="center", color="black")

    fig.subplots_adjust(top=0.88)
    fig.tight_layout()
    if saveAs is not None:
            plt.savefig(path+f"/{saveAs}.png")

    plt.show()

def plotTRACEDistributions(path=PATH, saveAs=None):
    df=TRACEEligibleLoader(path=path).load()
    fig, axes=plt.subplots(ncols=4, figsize=(30,10))

    axes[0].hist(df['Maturity'])
    axes[0].set_title('Distribution of Maturity Dates')


    axes[1].hist(df['Cpn'])
    axes[1].set_title('Distribution of Coupon Amounts')


    axes[2].hist(df['Issue Date'])
    axes[2].set_title('Distribution of Issue Dates')

    axes[3].bar(df['Category'].unique()[:5], df['Category'].value_counts()[:5])
    axes[3].set_title('Distribution of Top 5 Coupon Types')

    fig.suptitle('Various Distributions for Final Set of Securities')
    fig.subplots_adjust(top=0.88)
    plt.tight_layout()
    if saveAs is not None:
            plt.savefig(path+f"/{saveAs}.png")
    
    plt.show()

def plotCorrleationMatrixOfTRACE(path=PATH, saveAs=None):
    traceIssuances=TRACEEligibleLoader(path=path).load()

    cols=['Cpn', 'Maturity', 'Mortgage Original Amount', 'Issue Date', 'BBG Composite', 'Original WAL','Delinquency Rate 60+ Days', 'Delinquency Rate 90+ Days']

    fig, axes = plt.subplots(ncols=len(cols), nrows=len(cols), figsize=(25,25))

    for j,i in enumerate(cols):
        for l, k in enumerate(cols):
            if j==l:
                if type(traceIssuances[i][0])==str or type(traceIssuances[i][0])==np.bool_:
                    axes[j,l].barh(traceIssuances[i].unique(), traceIssuances[i].value_counts()/np.sum(traceIssuances[i].value_counts()), linewidth=0)
                elif type(traceIssuances[i][0])==pd.Timestamp:
                    axes[j,l].hist(traceIssuances[i].dt.year, orientation='horizontal', density=True)
                else:
                    axes[j,l].hist(traceIssuances[i], orientation='horizontal', density=True)
                    

            else:
                axes[j,l].scatter(traceIssuances[k], traceIssuances[i])
                    
            
            axes[j,l].tick_params(axis='x', labelrotation=90)
            axes[j,l].autoscale()
                
    pad=5
    for ax, col in zip(axes[0], cols):
        ax.annotate(col, xy=(0.5, 1), xytext=(0, pad),
                    xycoords='axes fraction', textcoords='offset points',
                    size='large', ha='center', va='baseline')

    for ax, row in zip(axes[:,0], cols):
        ax.annotate(row, xy=(0, 0.5), xytext=(-ax.yaxis.labelpad - pad, 0),
                    xycoords=ax.yaxis.label, textcoords='offset points',
                    size='large', ha='right', va='center')
        
        
    # fig.suptitle("Correlation Matrix of TRACE Elligible Bonds")
    fig.subplots_adjust(top=0.88)
    fig.tight_layout()
    if saveAs is not None:
            plt.savefig(path+f"/{saveAs}.png")
    plt.show()

def plotYieldCurveChange(path=PATH, saveAs=None):
    loader = ConstructYieldCurve()
    curves = loader.load(start_date="01-01-2008")

    X_ticks = [1, 2, 3, 5, 7, 10, 20, 30]

    print(curves)
    fig, ax = plt.subplots()

    ax.plot(X_ticks, curves.iloc[-1].values, label=f"Yields as of 1/1/2008")
    ax.plot(X_ticks, curves.loc["2009-01"].values, label=f"Yields as of 1/1/2009")
    ax.plot(X_ticks, curves.loc["2020-01"].values, label=f"Yields as of 1/1/2020")
    ax.plot(X_ticks, curves.iloc[0].values, label=f"Yields as of 10/30/2020")
    
    ax.legend()

    ax.set_xlabel("Maturity (Yrs)")
    ax.set_ylabel("Yield (%)")

    ax.set_xticks(X_ticks)

    fig.suptitle("Change in Yield Curve from 2008 to 2020")
    if saveAs is not None:
            plt.savefig(path+f"/{saveAs}.png")
    plt.show()

    

if __name__=="__main__":
    
    # plotMeanIssuanceByYear(saveAs="meanIssuanceByYear")
    # plotDistributionOfIssuancesByYear(saveAs="distributionOfIssuancesByYear")
    # plotTopNIssuancesByCouponType(saveAs="top10IssuancesByCoupon")
    # plotHeatMapIssuancesByCouponType(saveAs="heatMapIssuances")
    # plotAverageDollarAmtIssuedByCouponType(saveAs="AverageDollarAmtIssuedByCouponType")
    # plotTRACEDistributions(saveAs="TRACEDistributions")
    # plotCorrleationMatrixOfTRACE(saveAs="TRACECorrelationMatrix")
    plotYieldCurveChange(saveAs="YieldCurve")
