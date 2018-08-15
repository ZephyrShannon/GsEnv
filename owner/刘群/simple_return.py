# <codecell>

def simple_return(price):
    stock_price = price.asMatrix()
    stock_rtn = stock_price.pct_change()
    
    #dropna
    stock_rtn.dropna(axis=1, how='all', inplace = True)
    #stock_rtn.dropna(how='all',inplace = True)

    return stock_rtn


# <codecell>

