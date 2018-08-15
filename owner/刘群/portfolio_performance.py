# <codecell>

# output performance table
import logging
from pgportfolio.tools.configprocess import load_config
from pgportfolio.resultprocess import plot

def portfolio_performance(algos, format):
    logging.basicConfig(level=logging.INFO)
    algos = algos.split(",")
    labels = algos
    return plot.table_backtest(load_config(), algos, labels, format = format)


# <codecell>

