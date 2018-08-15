# <codecell>

from lib.gftTools import gsUtils

# <codecell>


def precheck_4_none(*datas):
    for data in datas:
        if isinstance(data, gsUtils.ItContinue):
            return data
    return datas


# <codecell>

