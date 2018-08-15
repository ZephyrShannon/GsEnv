# <codecell>



# <codecell>

gsUtils.

# <codecell>

x0

# <codecell>

def cut2bin(ser_x, totalBinNum, ascending=False):
    # calculate bin size
    totalBinNum = int(totalBinNum)
    xlen = len(ser_x)
    arr_binsize = np.repeat(xlen // totalBinNum, totalBinNum)
    remaining = xlen % totalBinNum
    if remaining > 0:
        arr_binsize[:remaining] += 1
    # map each signal to its binIdx
    arr_binmap = np.repeat(np.arange(totalBinNum) + 1, arr_binsize)
    ser_xrank = ser_x.rank(method='first', ascending=ascending)
    ser_result = pd.Series(
        arr_binmap[np.array(ser_xrank.values - 1, dtype='int')])
    return ser_result

# <codecell>

df_l_factors['binIdx'] = gb_factors.transform(cut2bin,totalBinNum,ascending=False)


# <codecell>


df_l_factors
