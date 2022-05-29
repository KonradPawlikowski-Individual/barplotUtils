import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

supportedListTypes = (list,tuple, np.ndarray, pd.core.series.Series, pd.core.indexes.base.Index)

def stackbar(axis, x, ys, stackOrder=None, kwargBroadcast={}, **kwargs):
    '''
    Creates a stacked bar plot on the provided axis, x is the grouping,
    ys must be of the same type and castable to a numpy array.
    kwargs are broadcast similar to how the method works in numpy, this can be
    toggled for individual kwargs by including them in the kwargBroadcast set.
    If no stack order is given the given order of elements will be used, if given
    must be a list with the order of the each data stack matched by index.
    '''
    
    # cast all data to numpy array format
    x = np.array(x)
    ys = np.array(ys)
    
    # interpret given stackOrder, must always plot lowest stack first,
    # order ensures this, in the first case a simple default
    # is used, with a custom order the order needs to be sorted appropriately.
    if stackOrder is None:
        order = np.arange(ys.shape[1],0,-1)[::-1]
    else:
        order = np.array(stackOrder,dtype=int)-min(stackOrder)
        order = [(i,order[i]) for i in range(len(order))]
        order.sort(key = lambda x: x[1])
        order = [o[0] for o in order[::-1]]
    
    # group the kwargs
    thinKwargs = {}
    wideKwargs = set()
    for key in kwargs.keys():
        if key in kwargBroadcast:
            thinKwargs[key] = kwargs[key]
        elif isinstance(kwargs[key],supportedListTypes):
            for i in range(len(order)):
                wideKwargs.add(key)
        else:
            thinKwargs[key] = kwargs[key]
    
    # iterpret plot bottom
    if 'bottom' in kwargs.keys():
        yi = np.array(kwargs['bottom'])
    else:
        yi = np.zeros(ys.shape[0])
    
    # begin plotting
    for i in order:
        # find the kwargs for this plot
        thisKwargs = thinKwargs.copy()
        for key in wideKwargs:
            thisKwargs[key] = kwargs[key][i]
        
        axis.bar(x, ys[::,i], bottom=yi, **thisKwargs)
        yi += ys[::,i] # stack subsequent readings for next bottom
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
    
    # cast all data to numpy array format
    x = np.array(x)
    ys = np.array(ys)
    
    # initialise the width
    width = iwidth/ys.shape[1]
    
    # for labelling xticks
    xlabel = x[::]
    x = np.arange(0,len(x))
    
    # begin plotting
    for i in range(ys.shape[1]):
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
        axis.bar(x+i*width, ys[::,i], width=width, *args, **thisKwargs)
    # end for
    axis.set_xticks(x+(i*width)/2)
    axis.set_xticklabels(xlabel)
# end method
