from preprocessing import *
import datetime as dt
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

def doPCA(X, n_components, threshold=0.99, plot=True):
    if np.shape(X)[0] != 0:
        feature_columns=X.columns
        model=PCA(n_components=n_components)
        model.fit(X)

        componentMap=pd.DataFrame(model.components_, columns=feature_columns, index=[f'PC-{i+1}' for i in range(n_components)])
        print(componentMap) 

        if plot:
            fig, ax = plt.subplots()

            ax.plot(model.explained_variance_ratio_)
            ax.axhline(1-threshold)
            plt.show()

        # print(model.explained_variance_ratio_)
        # print(model.singular_values_)
        return componentMap

def doKMeans(X, n_clusters=5):
    err: list = []

    for i in range(1,20): 
        kmeans = KMeans(n_clusters=i, init ='k-means++', max_iter=300,  n_init=10,random_state=0 )

        kmeans.fit(X)

        err.append(kmeans.inertia_)

    plt.plot(range(1,20),err)
    plt.title('Elbow Method Graph')
    plt.xlabel('Number of clusters')
    plt.ylabel('WCSS')
    plt.show()

    model=KMeans(n_clusters=n_clusters)

    y_pred=model.fit_predict(X)

    fig=plt.figure(figsize=(10,5))

    plt.scatter(X['Cpn'], X['Delinquency Rate 60+ Days'], c=y_pred)
    plt.tight_layout()

    plt.title('Classifications showing relationship between Rating and Coupon')
    _=plt.show()