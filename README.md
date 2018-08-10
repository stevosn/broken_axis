# broken_axis

Plot data in matplotlib-plots with a broken axes.

## breaks along y axis

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

## breaks along x axis
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
