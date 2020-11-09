import numpy as np
import seaborn as sns
import pdb

def ols(Y, X):
    q, r = np.linalg.qr(X)
    pdb.set_trace()
    # np.linalg.inv( r ) @ q.T @ Y
    return(np.linalg.inv( r ).dot( q.T ).dot( Y ))

iris = sns.load_dataset("iris")
iris_mat = iris[["sepal_width", "petal_length", "petal_width"]].values

print(ols(iris['sepal_length'].values, iris_mat))
