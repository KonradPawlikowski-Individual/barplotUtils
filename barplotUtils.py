import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

supportedListTypes = (list,tuple, np.ndarray, pd.core.series.Series, pd.core.indexes.base.Index)

def stackbar(axis, x, ys, stackOrder=None, kwargBroadcast={}, bottom=0, **kwargs):
    '''
    Creates a stacked bar plot on the provided axis, x is the grouping,
    ys must be of the same type and castable to a NumPy array.
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
 
    yi = np.zeros(ys.shape[0])
    
    # interpret bottom param
    bottom = np.array(bottom)
    if len(bottom.shape)<2:
        yi += bottom
        flag_bottom = False
    else:
        flag_bottom = True
    
    # begin plotting
    for i in order:
        # handle bottom param
        if flag_bottom:
            yi += bottom[i]
        
        # find the kwargs for this plot
        thisKwargs = thinKwargs.copy()
        for key in wideKwargs:
            thisKwargs[key] = kwargs[key][i]
        
        axis.bar(x, ys[::,i], bottom=yi, **thisKwargs)
        yi += ys[::,i] # stack subsequent readings for next bottom
    # end for
# end method

def multibar(axis, x, ys, igap=0, bgap=0, kwargBroadcast={}, **kwargs):
    '''
    Creates a multiple bar plot on the provided axis, x is the grouping, ys must be castable to a NumPy array.
    Kwargs are broadcast by default, this can be toggled for individual kwargs by including them in the kwargBroadcast
    set. igap creates an intermediate gap between multiple bars while bgap creates a gap between the bars, both should be
    given as ratios (since the multibar placements are standardised to integer indicies).
    '''
    
    # cast all data to numpy array format
    x = np.array(x)
    ys = np.array(ys)
    
    # define default width
    offset = np.zeros(ys.shape[1])
    if 'width' not in kwargs.keys():
        kwargs['width'] = (1-igap-bgap)/ys.shape[1]
        offset = np.arange(ys.shape[1])*(kwargs['width']+bgap/ys.shape[1])
    
    # for labelling xticks
    xlabel = x[::]
    x = np.arange(0,len(x))
    
    # group the kwargs
    thinKwargs = {}
    wideKwargs = set()
    for key in kwargs.keys():
        if key in kwargBroadcast:
            thinKwargs[key] = kwargs[key]
        elif isinstance(kwargs[key],supportedListTypes):
            for i in range(ys.shape[1]):
                wideKwargs.add(key)
        else:
            thinKwargs[key] = kwargs[key]
    
    # begin plotting
    for i in range(ys.shape[1]):
        # find the kwargs for this plot
        thisKwargs = thinKwargs.copy()
        for key in wideKwargs:
            thisKwargs[key] = kwargs[key][i]
        # end for
            
        axis.bar(x+offset[i], ys[::,i], **thisKwargs)
    # end for
    axis.set_xticks(x+offset[i]/2)
    axis.set_xticklabels(xlabel)
# end method
