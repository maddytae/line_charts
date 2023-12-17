
import os
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from matplotlib.ticker import MaxNLocator
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from collections import OrderedDict

def data_standardize(df,row,col,line,period,value,axis_col=None):
    #standardize data
    df=df.rename(columns={row:'row',
                     col:'col',
                     line:'line',
                     value:'value',
                     period:'period'})

    if axis_col in df.columns and axis_col:
        
            df=df.rename(columns={axis_col:'axis_col'})
            df=df[['row','col','line','period','value','axis_col']]
    else:
        
        df=df[['row','col','line','period','value']]
        
    # per_dict={'PQ0':'Y0','PQ4':'Y1','PQ8':'Y2','PQ12':'Y3'}
    # df['Period']=df['Period'].map(per_dict).fillna(df['Period'])
    return df


def get_lower_upper(data,padding=0.1):
    
    min_value = data['value'].min()
    max_value = data['value'].max()
    
    return min_value * (1-padding),max_value * (1+padding)