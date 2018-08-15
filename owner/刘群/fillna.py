# <codecell>

# methods: 'median', 'mean', 'ffill', 'bfill', filled by other data or value
# lookback = -1 meaning None (ffill max is the whole axis)

def fillna(data, method, fillna_value=None, lookback=None):
    stocks = data.asMatrix()
        
    if method == 'ffill' and 'bfill':
        if lookback <0:
            lookback = None
        elif lookback == 0:
            raise Exception('Fillna method of %s limit cannot be 0.' % method)
        stocks.fillna(method = method, limit=lookback, inplace=True)
    
    elif method == 'median':
        stocks.fillna(value = stocks.median(), inplace=True)
        
    elif method == 'mean':
        stocks.fillna(value = stocks.mean(), inplace=True)
    
    else:
        stocks.fillna(value = fillna_value, inplace=True)
    
    return stocks
    
 

# <codecell>

