# <codecell>

import numpy as np
import pandas as pd
from sklearn import datasets, linear_model
from sklearn.metrics import r2_score
import statsmodels.api as sm
import statsmodels.stats.api as sms
from statsmodels.compat import lzip
import statsmodels.stats.outliers_influence as smo

def OLS Precheck(context, X,y):
    precheck={'OLS Summary':ols_summary(X,y),'Coefficient Changes': ols_coeff_changes(X,y),'VIF':VIF(X),\
              'Conditional Number':Cond_No(X),'Breush Pagan test':Breush_Pagan(X,y),\
              'Goldfeld Quant test': Goldfeld_Quant(X,y),'ARCH test':ARCH_test(X,y), 'Breusch Goldfrey test': Breusch_Goldfrey(X,y),\
             'Durbin Watson test': Durbin_Watson(X,y),'OLS Influence': OLSinfluence(X,y),'Elliptic Envelop': EllipticEnvelop(X)}
    return precheck

# <codecell>



# <codecell>

#OLS fit
def ols(X,y):
    ols_model=sm.OLS(y,X)
    return ols_results = ols_model.fit()

#OLS summary
def ols_summary(X,y):
    ols_results = ols(X,y)
    return ols_results.summary()

# <codecell>

##Check Multicollinearity
#1. Check if there is large changes in the coefficients when one variable is deleted (dataframe)
def ols_coeff_changes(X,y):
    ols_results2 = sm.OLS(y.ix_[:999],X.ix_[:999]).fit()
    return print("Percentage change %4.2f%%\n"*7 % \
      tuple([i for i in (ols_results2.params - ols(X,y).params)/ols(X,y).params*100]))

'''
2. Adding random noise and perturb the data and check changes in the coefficients
sig=2
e = sig*np.random.normal(size=n_samples)
y = y_true + e
stats_model=sm.OLS(y,X)
results = stats_model.fit()
print('After purterbation, the coefficients become: ', results.params)
'''


#3. VIF: there is highly collinearity if it is above 5
def VIF(X):
    vif=pd.DataFrame()
    vif["VIF Factor"]=[smo.variance_inflation_factor(X, i) for i in range(X.shape[1])]
    return vif

#4. Condition Number Test: there is highly collinearity if it is above 30
def Cond_No(X):
    cond=np.linalg.cond(np.dot(X.T,X))
    return cond

# <codecell>

## Check Heteroskedasticity

# 1. Breush-Pagan test: ep**2 = del_0 + del_1 x_1 + del2 x_2 +...+ e
# hypothesis-esidual variance does not depend on the variables in x. 
# reject if p-value is too small and f-value is too large(or compare to the statistic tables)
# http://www.statsmodels.org/dev/generated/statsmodels.stats.diagnostic.het_breuschpagan.html#statsmodels.stats.diagnostic.het_breuschpagan
def Breush_Pagan(X,y):
    ols_retults=ols(X,y)
    name = ['LM statistic', 'p-value of LM test', 
            'f-statistic of the hypothesis', 'f p-value']
    test = sms.het_breushpagan(ols_retults.resid, ols_retults.model.exog)
    return lzip(name, test)


# 2. Goldfeld-Quandt test: split X into two subsamples
# null: two subsamples' variance are the same
# alternative: increasing, decreasing or two-sided
# http://www.statsmodels.org/dev/generated/statsmodels.stats.diagnostic.HetGoldfeldQuandt.html#statsmodels.stats.diagnostic.HetGoldfeldQuandt
def Goldfeld_Quant(X,y):
    ols_retults=ols(X,y)
    name = ['F statistic', 'p-value']
    test = sms.HetGoldfeldQuandt().run(ols_results.model.endog, ols_results.model.exog, idx=None, \
                                 split=0.25, drop =0.5, alternative ='two-sided', attach=True )
    return lzip(name, test)



# 3. Engle’s Test for Autoregressive Conditional Heteroscedasticity (ARCH): 
# (AR(p)): ep_t**2 = a_0 + a_1 ep_t-1**2 + ..+ a_p ep_t-p **2 +  e_t
# check time series error variance depends on previous time periods' error terms 
# null: variance do not depend on previous errors
def ARCH_test(X,y):
    ols_retults=ols(X,y)
    name = ['LM statistic', 'p-value of LM test', 
            'f-statistic of the hypothesis', 'f p-value']
    test = sms.het_arch(ols_results.resid)
    return lzip(name,test)

# <codecell>

## Check Autocorrelation
# 1. Breusch-Godfrey LM test (AR(p)) : 
# ep_t = del_0 + del_1 x_t,1 + del2 x_t,2+...a_1 ep_t-1 +...+ a_p ep_t-p +e_t
# check redisuals in regression
# null: errors do not depends on previous errors of order up to p
def Breusch_Goldfrey(X,y):
    ols_retults=ols(X,y)
    name = ['LM statistic', 'p-value of LM test', 
            'f-statistic of the hypothesis', 'f p-value']
    test = sms.acorr_breusch_godfrey(ols_results)
    return lzip(name,test)

#2. Durbin-Watson test
# d= sum(e_t -e_t-1)**2 / sum(e_t)**2
#null: no correlation. See if the result is close to 2
def Durbin_Watson(X,y):
    ols_retults=ols(X,y)
    test = sms.stattools.durbin_watson(ols_results.resid,axis=0)
    return test

## Autocorrelation fix
# Using Newey-West estimator to estimate covariance matrix (lag=1)
# Also shows Durbin-Watson test
# small sample correction??
def Newey_West(X,y):
    ols_retults=ols(X,y)
    FGLS = ols_results.get_robustcov_results(cov_type='HAC',maxlags=999)
    return FGLS.summary

# <codecell>

# 1. OLSInfluence: Influence after remove each observation. Used in moderate data size
# possible outliers: (a) large change in dfbetas; (b) big cooks distance
# (c) big Dffits (d) big diff btw Dffits and internal dffits
# (e) big hat diag (f))big diff btw std res and studentized resid
def OLSinfluence(X,y):
    ols_retults=ols(X,y)
    test_class = smo.OLSInfluence(ols_results)
    test =test_class.summary_frame()
    return test.head()

# 2. Robust covariance estimation
# (a) Elliptic Envelope 
# X[,y]??
def EllipticEnvelop(X):
    Outlier_fraction = 0.0001
    from sklearn.covariance import EllipticEnvelope
    # (n+k+1)/2 points whose empirical covariance has the smallest determinant
    ell = EllipticEnvelope(contamination=Outlier_fraction).fit(X)
    Outlier_pred = ell.predict(X)
    return Outlier_pred
