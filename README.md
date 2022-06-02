# barplotUtils
Small individual project consisting of simple bar plotting utilities.
The point of barplotUtils is to provide simple and intuitive methods for
quickly plotting bar plots without losing the versitility provided by the
matplotlib library (which this project is based in), see Examples.ipynb
for simple examples of what the implemented methods can do and how.

Features:
- broadcasting kwargs, all methods implement this, this allows a high degree of customisation for plots.
- barplotUtils.stackbar, intuitive stack bar plots with little effort, can also rearange the stacks with stackOrder param.
- barplotUtils.multibar, simple multiple bar plots.

Fixed:
- removed dependance on pandas
- 'ghost bars' in barplotUtils.stackbar
- allow zorder to be broadcast in barplotUtils.stackbar
- improved bottom compatability in barplotUtils.stackbar
- introduced igap and bgap for intuitive customisation of bar gaps in barplotUtils.multibar

Known Issues:
- the order of the elements in the legend for the barplotUtils.stackbar method are in reverse of the order the elements were stacked
- using 'supportedListTypes' in deciding how to broadcast is an awkward workaround to reach the intended goal
- multiple stack bar plots are unsupported
