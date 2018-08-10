# broken_axis

Plot data in matplotlib-plots with a broken axes.

This is a simple approach. There is still alot to solve, such as plotting with lines instead of markers, probably histograms do not work, log scales, etc. Well, it's a starting point, anybody is welcome to contribute.  There are also other approaches, e.g. [here](https://github.com/matplotlib/matplotlib/issues/11682).

## Usage

### breaks along y axis

```
from broken_axis import broken_axis

fig = plt.figure()
fig, axs = broken_axis(t,  # x-data
                       x,  # y-data
                       [-1.0, 0.0],  # make braeks at these points
                       dbreaks=[0.25, 0.1],  # distances to leave out
                       along_x=False,  # to make breaks along the y-axis
                       figure=fig,
                       plt_kws=dict(marker='.'),  # plt kws to be forwarded to the plot function
                       )
```

### breaks along x axis
```
from broken_axis import broken_axis

fig = plt.figure()
fig, axs = broken_axis(t,  # x-data
                       x,  # y-data
                       [100, 600],  # make braeks at these points
                       dbreaks=[50, 200],  # distances to leave out
                       along_x=True,  # to make breaks along the y-axis
                       figure=fig,
                       plt_kws=dict(marker='.'),  # plt kws to be forwarded to the plot function
                       )
```
