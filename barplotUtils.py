import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

supportedListTypes = (list,tuple, np.ndarray, pd.core.series.Series, pd.core.indexes.base.Index)

def stackbar(axis, x, ys, kwargBroadcast={}, *args, **kwargs):
    '''
    Creates a stacked bar plot on the provided axis, x is the grouping,
    ys must be of the same type and castable to a pandas dataframe (e.g a 2d array) or a pandas
    dataframe. args are strictly passed as is to the plot method while
    kwargs are broadcast by default, this can be toggled for individual kwargs by including
    them in the kwargBroadcast set. If a integer zorder is given then all zorders for the
    elements will be atleast the given value + 1 and atmost said value plus the number of stacked
    plots. Otherwise if zorder is a list of length ys.columns then the zorder defines the stack
    order of the ys, the default value for zorder is 0.
    '''
    
    # cast to dataframe
    if not isinstance(ys,pd.DataFrame):
        ys = pd.DataFrame(ys)
    
    # interpret given zorder (or define default)
    # must always plot lowest zorder first
    # order ensures this, in the first 2 cases a simple default
    # is used, with a custom order the order needs to be sorted
    # but the index pairings must remain the same.
    if 'zorder' not in kwargs.keys():
        kwargs['zorder'] = 0
    if isinstance(kwargs['zorder'],int):
        kwargs['zorder'] = np.arange(len(ys.columns),0,-1)+kwargs['zorder']
        order = (kwargs['zorder']-min(kwargs['zorder']))[::-1]
    else: # custom z-order
        order = np.array(kwargs['zorder'],dtype=int)-min(kwargs['zorder'])
        order = [(i,order[i]) for i in range(len(order))]
        order.sort(key = lambda x: x[1])
        order = [o[0] for o in order[::-1]]
    
    # begin plotting
    yi = np.zeros(len(ys))
    for i in order:
        yi+=ys[ys.columns[i]] # stack subsequent readings
        
        # find the kwargs for this plot
        thisKwargs = {}
        for key in kwargs.keys():
            if key in kwargBroadcast:
                thisKwargs[key] = kwargs[key]
            elif isinstance(kwargs[key],supportedListTypes):
                thisKwargs[key] = kwargs[key][i]
            else:
                thisKwargs[key] = kwargs[key]
        # end for
        axis.bar(x, yi, *args, **thisKwargs)
    # end for
# end method

def multibar(axis, x, ys, iwidth=1, kwargBroadcast = {}, *args, **kwargs):
    '''
    Creates a multiple bar plot on the provided axis, x is the grouping, ys must be of the same type and
    castable to a pandas dataframe (e.g a 2d array) or a pandas dataframe.
    args are strictly passed, as is, to the plot method while kwargs are broadcast by default, this
    can be toggled for individual kwargs by including them in the kwargBroadcast
    set. iwidth creates a 'gap' between sets of data multiplicitively, iwidth should be a value >0 but <=1.
    '''
    
    # cast to dataframe
    if not isinstance(ys,pd.DataFrame):
        ys = pd.DataFrame(ys)
    
    # initialise the width
    width = iwidth/len(ys.columns)
    
    # for labelling xticks
    xlabel = x[::]
    x = np.arange(0,len(x))
    
    # begin plotting
    for i in range(len(ys.columns)):
        # find the kwargs for this plot
        thisKwargs = {}
        for key in kwargs.keys():
            if key in kwargBroadcast:
                thisKwargs[key] = kwargs[key]
            elif isinstance(kwargs[key],supportedListTypes):
                thisKwargs[key] = kwargs[key][i]
            else:
                thisKwargs[key] = kwargs[key]
        # end for
        axis.bar(x+i*width, ys[ys.columns[i]], width=width, *args, **thisKwargs)
    # end for
    axis.set_xticks(x+(i*width)/2)
    axis.set_xticklabels(xlabel)
# end method
