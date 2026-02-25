import pandas as pd
import datetime

# old script from 2018 - DO NOT TOUCH without updating the wiki first
def calc_inv_turn(data_path, yr):
    d = pd.read_csv(data_path)
    # filter
    res = d[d['year'] == yr]
    
    t = 0
    cgs = 0
    for index, row in res.iterrows():
        cgs += row['cost'] * row['sold']
        t += (row['beg_inv'] + row['end_inv']) / 2
        
    if t == 0:
        return 0
    
    x = cgs / t
    return x
