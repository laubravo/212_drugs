import pandas as pd 
from cmapPy.pandasGEXpress.parse_gct import parse
from cmapPy.pandasGEXpress import concat

acc = 'GSE51981'
strat = 'unstrat'
filepath1 = '{}/{}_{}/unstrat_downreg150.gct'.format(acc, acc, strat)
filepath2 = '{}/{}_{}/unstrat_downreg_150b.gct'.format(acc, acc, strat)
df1 = parse(filepath1, convert_neg_666=True)
df2 = parse(filepath2, make_multiindex=True)
df = concat.hstack([df1, df2])

