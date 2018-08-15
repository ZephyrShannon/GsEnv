# <codecell>



# <codecell>

from lib.gftTools import gsUtils

def precheck_for_empty_row(*dataframes):
    for df in dataframes:
        if df.index.size <= 0:
            return gsUtils.ItContinue("Dataframe is empty")
    return dataframes


# <codecell>

