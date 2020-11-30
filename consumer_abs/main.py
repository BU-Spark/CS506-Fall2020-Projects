from functions import *
from preprocessing import *
from sklearn.pipeline import Pipeline, make_pipeline

from sklearn.naive_bayes import MultinomialNB
from sklearn.preprocessing import Binarizer
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis

from sklearn.model_selection import train_test_split

from sklearn.metrics import classification_report
from sklearn import metrics
import statsmodels.api as sm
from statsmodels.regression.linear_model import RegressionResults
from scipy.linalg import toeplitz

import os 
import sys

def evaluation(model, X_train, y_train, X_test, y_test):
    # y_pred = model.predict(X_train)
    # score  = metrics.mean_squared_error(y_train,y_pred, squared=False)

    # print("Train: RMSE of {} is {:0.3f}".format(model, (score)))
    # print(classification_report(y_train, y_pred))

    y_pred = model.predict(X_test)
    score  = metrics.mean_squared_error(y_test,y_pred, squared=False)

    print("Test: RMSE of {} is {:0.3f}".format(model, (score)))
    print(classification_report(y_test, y_pred))

    return score

def main1():    
    """
    Uses Logistic Regression and kNN to predict prepayment/default of ABS. 
    """
    loader = TRACEEligibleLoader()
    securities = loader.load(pickle_name="fromTRACEELIGIBLE.p")
    print(securities.columns)

    # We need to exclude Next Call Date, WAC, and Current WAL since they give prepayment information
    X = securities.drop(['Is Mortgage Paid Off', "Next Call Date", "WAC", "Current WAL", "Amt Out"], axis=1)
    
    y = securities['Is Mortgage Paid Off'].values.reshape(-1,1)


    transformer=TRACETransformer(categoricalColumns=["BBG Composite", "Day Count", "Category", "isCallable"], dateColumns=["Issue Date", "Maturity"], 
                        labelColumns=["CUSIP", "Security Name", "Ticker"])
    X=transformer.fit_transform(X)


    # Here, we see that KNN performs better than Logistic Regression in classifying defaults/payoffs
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=20)

    # sys.stdout = open("Classification Results.txt", "w")    

    # pipeline=make_pipeline(LogisticRegression())
    # pipeline.fit(X_train, y_train)
    # evaluation(pipeline, X_train, y_train, X_test, y_test)
    
    # classifiers = [
    #     KNeighborsClassifier(3),
    #     SVC(kernel="linear", C=0.025),
    #     SVC(gamma=2, C=1),
    #     GaussianProcessClassifier(1.0 * RBF(1.0)),
    #     DecisionTreeClassifier(max_depth=5),
    #     RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1),
    #     MLPClassifier(alpha=1, max_iter=1000),
    #     AdaBoostClassifier(),
    #     GaussianNB(),
    #     QuadraticDiscriminantAnalysis()]




    # for classifier in classifiers:

    #     pipeline=make_pipeline(classifier)
    #     pipeline.fit(X_train, y_train)
    #     evaluation(pipeline, X_train, y_train, X_test, y_test)


    
    # sys.stdout.close()

    classifiers = [
        KNeighborsClassifier(3),
        GaussianProcessClassifier(1.0 * RBF(1.0)),
        DecisionTreeClassifier(max_depth=5),
        AdaBoostClassifier(),
        GaussianNB(),
    ]

    for i in range(2, 25, 3):
        pipeline=make_pipeline(KNeighborsClassifier(i))
        pipeline.fit(X_train, y_train)
        evaluation(pipeline, X_train, y_train, X_test, y_test)

    for i in range(2, 25, 3):
        pipeline=make_pipeline(DecisionTreeClassifier(max_depth=i))
        pipeline.fit(X_train, y_train)
        evaluation(pipeline, X_train, y_train, X_test, y_test)

    
    

def main2():
    """
    Uses OLS and GLS to calculate factor model for monthly change in ABS price. Also computes n principal components of monthly return. 
    """
    sys.stdout = open("Returns Results.txt", "w")
    loader = TRACEEligibleLoader()
    securityDescriptive = loader.load(pickle_name="fromABSTRACEISSUANCES.p")

    loader = SecurityLoader()
    securities = loader.load()

    cardDFs = {}
    autoDFs = {}
    consumerDFs = {}

    print(securityDescriptive)
    
    for j in securities:
        if securityDescriptive[securityDescriptive["Security Name"]==j]['Category'].values == "CARD":
            cardDFs[j] = securities[j]
        elif securityDescriptive[securityDescriptive["Security Name"]==j]['Category'].values == "AUTO":
            autoDFs[j] = securities[j]

        else:
            consumerDFs[j] = securities[j]

    yieldConstructor = ConstructYieldCurve()
    yieldCurve = yieldConstructor.load()


    def modifyDF(df):
        # Percent change month/month
        df["Price"] = df["Price"].pct_change(-1)

        # Lag to see if previous month's features are indicative of present month's return
        df["Price"] = df["Price"].shift(1)
        df.dropna(inplace=True)
        X = df.drop(["Price"], axis=1)
        X = pd.merge(X, yieldCurve, left_index=True, right_index=True)
        # print(X)

        y = df["Price"]

        return X, y

    def SVD(X, threshold=0.1):
        u, s, vt = np.linalg.svd(X)

        X_norm = np.linalg.norm(X)
        err = np.cumsum(s[::-1]**2)
        err = np.sqrt(err[::-1])
        # plt.plot(range(1,len(s)+1),err[:len(s)]/X_norm)
        # plt.show()
        
        for k in range(len(err)):
            if err[k] < threshold:
                return  u[:,:k-1] @ np.diag(s[:k-1])

       

    def linearRegression(X, y, plot=False):
        if np.shape(X)[1] < np.shape(y)[0]:
            residuals = sm.OLS(y, X).fit().resid
    
            ols_residuals = sm.OLS(residuals.values[1:], sm.add_constant(residuals.values[:-1])).fit()
            rho = ols_residuals.params[1]

            sigma = rho ** toeplitz(np.arange(len(y)))

            model = sm.GLS(y, X, sigma=sigma)
            results = model.fit()
            y_pred = results.predict(X)

            
            print(results.summary())
        
            if plot:
                residuals = y - y_pred
                fig, ax = plt.subplots()
                ax.scatter(y_pred, residuals)
                ax.set_xlabel("Fitted Value")
                ax.set_ylabel("Residual Value")
                fig.suptitle("Residual Plot")

                plt.show()
        elif np.shape(y)[0] == 0:
            print("No samples")
        else:

            print(f"N_Features ({np.shape(X)[1]}) > N_Samples ({np.shape(y)[0]})")



    for i in cardDFs:
        X, y = modifyDF(cardDFs[i])
        print(f"Results for {i}")
        linearRegression(X, y)
        doPCA(X, n_components=min(X.shape[0], X.shape[1]), security=i, plot=False)
        print("")


    for i in autoDFs:
        X, y = modifyDF(autoDFs[i])
        print(f"Results for {i}")
        linearRegression(X, y)
        doPCA(X, n_components=min(X.shape[0], X.shape[1]), plot=False)
        print("")
    
   
    for i in consumerDFs:
        X, y = modifyDF(consumerDFs[i])
        print(f"Results for {i}")
        linearRegression(X, y)
        doPCA(X, n_components=min(X.shape[0], X.shape[1]), plot=False)
        print("")

    sys.stdout.close()



if __name__=="__main__":
    PATH="D:/OneDrive/College Notebook/Boston University/Fall Senior Year/CS 506/Project/CS506-Fall2020-Projects/consumer_abs/"
    # PATH="C:/Users/bishj/OneDrive/College Notebook/Boston University/Fall Senior Year/CS 506/Project/CS506-Fall2020-Projects/consumer_abs/data"

    # loader = IssuanceLoader()
    # securities = loader.load(how="df")
    # print(securities)

    # loader = TRACEEligibleLoader()
    # securities = loader.load(pickle_name="fromABSTRACEISSUANCES.p")
    # securities = pd.read_excel(PATH+"/traceIssuances.xlsx")

    # X_Cols=['Cpn', 'Amt Out', 'BBG Composite', 'Current WAL', 'Day Count',
    #    'Delinquency Rate 60+ Days', 'Delinquency Rate 90+ Days', 'Issue Date', 'Maturity', 'Mid Price', 'Mortgage Original Amount',
    #    'Next Call Date', 'Next Coupon Date',
    #    'Price at Issue', 'Category',
    #    'isCallable']

    # # We need to exclude Next Call Date, WAC, and Current WAL since they give prepayment information
    # X = securities.drop(['Is Mortgage Paid Off', "Next Call Date", "WAC", "Current WAL", "Amt Out"], axis=1)
    
    # y = securities['Is Mortgage Paid Off'].values.reshape(-1,1)


    # transformer=TRACETransformer(categoricalColumns=["BBG Composite", "Day Count", "Category", "isCallable"], dateColumns=["Issue Date", "Maturity"], 
    #                     labelColumns=["CUSIP", "Security Name", "Ticker"])
    # X=transformer.fit_transform(X)

    # kmodel=KMeans(n_clusters=10)

    # y_pred=kmodel.fit_predict(X)
    # X_Cols.append('CUSIP')

    # sampleSelection=securities[X_Cols].copy()
    # sampleSelection.dropna(inplace=True)
    # sampleSelection.reset_index(inplace=True)
    # sampleSelection.drop('index', inplace=True, axis=1)
    # sampleSelection['cluster']=y_pred


    # fig, ax = plt.figure()
    main1()
    # main2()
    
   


   

