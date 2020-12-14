from sklearn.utils import shuffle
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

from sklearn.model_selection import train_test_split, RandomizedSearchCV

from sklearn.metrics import classification_report
from sklearn import metrics
import statsmodels.api as sm
from statsmodels.regression.linear_model import RegressionResults
from scipy.linalg import toeplitz

import os 
import sys
pd.plotting.register_matplotlib_converters()

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

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=20)

    logistic_base = LogisticRegression()
    log_params = {'penalty': ['l2', 'l1', 'elasticnet', 'none'], 'C' : [0.1, 1, 10, 100, 1000]}
    log_search = RandomizedSearchCV(logistic_base, log_params, n_iter=200, cv=3, verbose=2, n_jobs=-1)

    svm_base = SVC()
    svm_params = {'C': [0.1, 1, 10, 100, 1000], 'kernel' : ['rbf', 'linear', 'sigmoid']}
    svm_search = RandomizedSearchCV(svm_base, svm_params, n_iter=200, cv=3, verbose=2, n_jobs=-1)

    kNN_base = KNeighborsClassifier()
    kNN_params = {'n_neighbors' : [i for i in range(2, 50, 5)], 
                'leaf_size' : [i for i in range(30, 60, 5)]}
    kNN_search = RandomizedSearchCV(kNN_base, kNN_params, n_iter=200, cv=3, verbose=2, n_jobs=-1)

    decision_tree_base = DecisionTreeClassifier()
    decision_tree_params = {'criterion' : ['gini', 'entropy'], 'max_depth' : [i for i in range(5, 50, 5)]}
    decision_tree_search = RandomizedSearchCV(decision_tree_base, decision_tree_params, n_iter=200, cv=3, verbose=2, n_jobs=-1)

    log_search.fit(X_train, y_train.ravel())
    svm_search.fit(X_train, y_train.ravel())
    kNN_search.fit(X_train, y_train.ravel())
    decision_tree_search.fit(X_train, y_train.ravel())

    sys.stdout = open("Classification Results.txt", "w")    

    
    for j, i in [(logistic_base, log_search), (svm_base, svm_search), (kNN_base, kNN_search), (decision_tree_base, decision_tree_search)]:
        j.set_params(**i.best_params_)
        j.fit(X_train, y_train.ravel())
        evaluation(j, X_train, y_train, X_test, y_test)
        
    sys.stdout.close()
    
    

def main2():
    """
    Uses OLS and GLS to calculate factor model for monthly change in ABS price. Also computes n principal components of monthly return. 
    """
   # sys.stdout = open("Returns Results.txt", "w")
    loader = TRACEEligibleLoader()
    securityDescriptive = loader.load(pickle_name="fromABSTRACEISSUANCES.p")

    loader = SecurityLoader()
    securities = loader.load()

    cardDFs = {}
    autoDFs = {}
    consumerDFs = {}

    
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

    
    def linearRegression(X, y, name, plotResiduals=False, plotFitted=False):
        if np.shape(X)[1] < np.shape(y)[0]:
    

            residuals = sm.OLS(y, X).fit().resid
    
            ols_residuals = sm.OLS(residuals.values[1:], sm.add_constant(residuals.values[:-1])).fit()
            rho = ols_residuals.params[1]

            sigma = rho ** toeplitz(np.arange(len(y)))

            model = sm.GLS(y, X, sigma=sigma)
            results = model.fit()
            y_pred = results.predict(X)

   
            
            print(results.summary())
        
            if plotResiduals:
                residuals = y - y_pred
                fig, ax = plt.subplots()
                ax.scatter(y_pred, residuals)
                ax.set_xlabel("Fitted Value")
                ax.set_ylabel("Residual Value")
                fig.suptitle("Residual Plot")
                plt.show()

            if plotFitted:
                fig, ax = plt.subplots()
                y.plot(ax=ax)
                ax.plot(y_pred)
                ax.set_xlabel("Date")
                ax.set_ylabel("Returns")
                fig.suptitle("Predicted Values")
                plt.savefig(PATH+f"/Plots/{name}_prediction.png")
                plt.show()

        elif np.shape(y)[0] == 0:
            print("No samples")
        else:

            print(f"N_Features ({np.shape(X)[1]}) > N_Samples ({np.shape(y)[0]})")


    for i in autoDFs:
        X, y = modifyDF(autoDFs[i])
        print(y)
        print(f"Results for {i}")
        linearRegression(X, y, i, plotFitted=True)
        # doPCA(X, n_components=min(X.shape[0], X.shape[1]), plot=False)
        print("")
    
   
    for i in consumerDFs:
        X, y = modifyDF(consumerDFs[i])
        print(f"Results for {i}")
        linearRegression(X, y, i, plotFitted=True)
        # doPCA(X, n_components=min(X.shape[0], X.shape[1]), plot=False)
        print("")

    # sys.stdout.close()

def main3():
    loader = TRACEEligibleLoader()
    securityDescriptive = loader.load(pickle_name="fromABSTRACEISSUANCES.p")

    loader = SecurityLoader()
    securities = loader.load()

    cardDFs = {}
    autoDFs = {}
    consumerDFs = {}

    
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
        df.dropna(inplace=True)
        X = df.drop(["Price"], axis=1)
        X = pd.merge(X, yieldCurve, left_index=True, right_index=True)
        # print(X)

        y = df["Price"]

        return X, y

    
    from statsmodels.tsa.arima.model import ARIMA
    from statsmodels.tsa.arima_model import ARIMAResults

    def timeSeriesModel(X, y, plot=False):
        if np.shape(X)[1] < np.shape(y)[0]:

            model = ARIMA(y, exog=X, order=(4, 3, 1))
            model_fit = model.fit()

            print(model_fit.summary())
            

    X, y = modifyDF(consumerDFs['AMXCA 2018-3 A'])

    timeSeriesModel(X, y.values.reshape(-1,1))

    


if __name__=="__main__":
    PATH="D:/OneDrive/College Notebook/Boston University/Fall Senior Year/CS 506/Project/CS506-Fall2020-Projects/consumer_abs/"
    

    # main1()
    main2()
    # main3()
    
   


   

