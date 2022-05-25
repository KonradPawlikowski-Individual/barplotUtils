# barplotUtils
Small individual project consisting of simple bar plotting utilities.
The point of barplotUtils is to provide simple and intuitive methods for
quickly plotting bar plots without losing the versitility provided by the
matplotlib library (which this project is based in), see Examples.ipynb
for simple examples of what the implemented methods can do and how.

Features:
- broadcasting kwargs, all methods implement this, this allows a high degree of customisation for plots.
- barplotUtils.stackbar, intuitive stack bar plots with little effort, can also rearange the stacks with zorder.
- barplotUtils.multibar, simple multiple bar plots.

Known Issues:
- the order of the elements in the legend for the barplotUtils.stackbar method are inverse to the order the elements were stacked
- both barplotUtils.stackbar and barplotUtils.multibar overly depend on pandas dataframes
- passing intuitive width parameters to the barplotUtils.multibar method is impossible
- barplotUtils.multibar's iwidth meaning is unintuitive
- requiring zorder to be passed as a kwarg may be too strict for barplotUtils.stackbar
- using 'supportedListTypes' in deciding how to broadcast is an awkward workaround to reach the intended goal
- args aren't broadcast (note: this is intentional but may be unintuitive)
- multiple stack bar plots are unsupported
