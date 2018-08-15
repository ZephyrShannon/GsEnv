# <codecell>


from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

def ols_score(dataset):
    lr = LinearRegression().fit(dataset['X_train'], dataset['y_train'])
    y_pred = lr.predict(dataset['X_test'])
    mse = mean_squared_error(dataset['y_test'],y_pred)
    r2_score = r2_score(dataset['y_test'],y_pred)
    print('MSE is', mse)
    print('Variance score is', r2_score)
    return mse


# <codecell>

