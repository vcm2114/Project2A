# -*- coding: utf-8 -*-

#-----------#
# Libraries #
#-----------#

# pandas
import pandas as pd


# scaling function

def scaling(df):
    
    """
       Input: - df: dataframe
       Output: - scaled dataframe
    """       
    
    df1 = df[df >= 0]
    df1 = df1[df1 < 2]
    df2 = df[df > 1]
    df2 = df2[df2 < 4]
    df3 = df[df > 3]
    
    names = df1.columns.tolist()
    names2 = []
    for e in names:
        names2.append('-' + e)
    df1.columns = names2
    
    names = df2.columns.tolist()
    names2 = []
    for e in names:
        names2.append('0' + e)
    df2.columns = names2
    
    names = df3.columns.tolist()
    names2 = []
    for e in names:
        names2.append('+' + e)
    df3.columns = names2    
    
    res = pd.concat([df1, df2, df3], axis=1)
    
    res = res.replace([0,1,2,3,4,5], [1,1,1,1,1,1])
    res = res.fillna(0)
    
    return res