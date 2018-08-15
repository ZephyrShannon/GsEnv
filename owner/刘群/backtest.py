# <codecell>

import logging
from pgportfolio.tools.shortcut import execute_backtest


def backtest(algo):
    config = config_by_algo(algo)
    set_logging_by_algo(logging.DEBUG, logging.DEBUG, algo, "backtestlog")
    portfolio_change_arr = execute_backtest(algo, config) # mu * w * y
    dic = {'portfolio_return': portfolio_change_arr}
    return dic


# <codecell>

def set_logging_by_algo(console_level, file_level, algo, name):
    if algo.isdigit():
        logging.basicConfig(filename="./train_package/" + algo + "/" + name,
                            level=file_level)
        console = logging.StreamHandler()
        console.setLevel(console_level)
        logging.getLogger().addHandler(console)
    else:
        logging.basicConfig(level=console_level)

# <codecell>

def config_by_algo(algo):
    """
    :param algo: a string represent index or algo name
    :return : a config dictionary
    """
    if not algo:
        raise ValueError("please input a specific algo")
    elif algo.isdigit():
        config = load_config(algo)
    else:
        config = load_config()
    return config

# <codecell>

