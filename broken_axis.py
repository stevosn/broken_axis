# -*- coding: utf-8 -*-
# Broken axis for matplotlib Axes
# Author: Steve Simmert
# Email: steve.simmert@fremiste.de
# Copyright: 2018
# Licence: GPLv3
################################################################################
__author__ = "Steve Simmert"
__copyright__ = "Copyright 2018"
__license__ = "GPLv3"
__maintainer__ = "Steve Simmert"
__email__ = "steve.simmert@fremiste.de"
__status__ = "testing"

from numpy import pi, cos, sin, logical_and
from matplotlib import rcParams
from inspect import getfullargspec
import matplotlib.gridspec as gridspec


def check_and_separate(fun, kws, exclude=True):
    """
    Checks if keywords of a given dictionary match the signature of
    the given function and separates the keywords.
    """
    argspec = getfullargspec(fun)

    sep = {}
    for k in kws:
        if k in argspec.args:
            sep[k] = kws[k]

    if exclude:
        for k in sep:
            kws.pop(k)

    return sep


def draw_breaks(ax, total_size, pos='right', size=1.5, angle=60, width=None, **kws):
    """
    Draw bars at the end of an axis break.
    """
    def gen_points(pos, xlim, ylim, dx, dy):
        """
        Generate the points that the break line connects.
        """
        for p in pos.split(' '):
            if p in ['up', 'upper', 'top']:
                y = ylim[1]
            elif p in ['low', 'lower', 'bottom']:
                y = ylim[0]
            elif p == 'right':
                x = xlim[1]
            elif p == 'left':
                x = xlim[0]
            else:
                raise Error('Unknown position "{}"'.format(p))
        px = (x-dx, x+dx)
        py = (y-dy, y+dy)
        
        return (px, py)
    
    def tuple_diff(lim):
        """ Return the difference of the given 2-tuple. """
        return lim[1] - lim[0]
                
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()    
    
    if pos in ['left', 'right']:
        pos_conj = ['upper', 'lower']
        dx = size * cos(angle * pi / 180) / 100 * total_size
        dy = size * sin(angle * pi / 180) / 100 * tuple_diff(ylim)
    elif pos in ['up', 'upper', 'low', 'lower', 'top', 'bottom']:
        pos_conj = ['left', 'right']
        dx = size * cos(angle * pi / 180) / 100 * tuple_diff(xlim)
        dy = size * sin(angle * pi / 180) / 100 * total_size

    args = (xlim, ylim, dx, dy)
    kws = dict(color='k', clip_on=False, linewidth=width or rcParams['axes.linewidth'])
    
    lns = []
    for p in pos_conj:
        pos_ = ' '.join([p, pos])
        lns.append(ax.plot(*gen_points(pos_, *args), **kws))

    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    
    return lns


def broken_axis(x, y, breaks, dbreaks=None, along_x=True, dgrid=100, space=1, figure=None, plt_kws={}, **kws):
    """
    Plot data, x and y, in a broken axis.

    Arguments
    ---------
    x : array-like
    y : arraylike
    breaks : float or list of float
        Value or list of values to break the axis.
    dbreaks : float or list of float
        Distances to leave plotting.
    along_x : bool
        Whether the breaks are along the x-axis.
    dgrid : int
        Fineness of the grid for the different axes.
    space : int
        The space betweent the breaks in units of the grid defined by dgrid.
    figure : None or figure object
    plt_kws : dict
        Key-word arguments forwarded to plot.
    """    
    n_brks = len(breaks)
    
    try:
        dbrks = iter(dbreaks)
    except TypeError:
        # only one value
        dbrks = (dbreaks if dbreaks else 0 for i in range(n_brks))
        
    # rename data to be broken
    s = x if along_x else y
    
    # partition the data
    last_brk = min(s)
    x_ = []
    y_ = []
    sizes = []
    
    for brk, dbrk in zip(breaks, dbrks):
        keep = logical_and(s >= last_brk, s < brk)
        x_.append(x[keep])
        y_.append(y[keep])
        sizes.append(brk - last_brk)
        last_brk = brk + dbrk
    
    keep = s >= last_brk
    x_.append(x[keep])
    y_.append(y[keep])
    sizes.append(max(s) - last_brk)
    
    total_size = sum(sizes)
    
    fig = figure or plt.figure()
    
    dgrid = int(dgrid)
    space = int(space)
    grid = (1, dgrid) if along_x else (dgrid, 1)
    draw_break_kws = check_and_separate(draw_breaks, kws)

    last_end = 0 if along_x else dgrid
    axs = []
    break_positions = []
    for idx, (x_part, y_part, size) in enumerate(zip(x_, y_, sizes)):
        ratio = size / total_size
        
        try:
            last_ax = axs[-1]
        except IndexError:
            last_ax = None            
        
        if along_x:
            new_end = last_end + int(dgrid * ratio)
            sl = slice(last_end, new_end - space)
            last_end = new_end + space
            gs = gridspec.GridSpec(*grid)
            ax = fig.add_subplot(gs[sl], sharey=last_ax, **kws)
            ax.plot(x_part, y_part, **plt_kws)
            ax.margins(x=0)
            if idx > 0:
                ax.tick_params(left=False, labelleft=False)
                ax.spines['left'].set_visible(False)
                # draw_breaks(ax, total_size, pos='left', **draw_break_kws)
                break_positions.append((ax, 'left'))
            if idx < n_brks:
                ax.tick_params(right=False, labelright=False)
                ax.spines['right'].set_visible(False)
                #draw_breaks(ax, total_size, pos='right', **draw_break_kws)
                break_positions.append((ax, 'right'))
            ax.set_xlim([min(x_part), max(x_part)])
        else:
            # drawing of axes is done from top to bottom -- must be reversed
            start = last_end - int(dgrid * ratio)
            sl = slice(start if start >= 0 else 0, last_end)
            last_end = start - space
            gs = gridspec.GridSpec(*grid)
            ax = fig.add_subplot(gs[sl], sharex=last_ax, **kws)
            ax.scatter(x_part, y_part, **plt_kws)
            ax.margins(y=0)
            if idx > 0:
                ax.tick_params(bottom=False, labelbottom=False)
                ax.spines['bottom'].set_visible(False)
                #draw_breaks(ax, total_size, pos='bottom', **draw_break_kws)
                break_positions.append((ax, 'bottom'))
            if idx < n_brks:
                ax.tick_params(top=False, labeltop=False)
                ax.spines['top'].set_visible(False)
                #draw_breaks(ax, total_size, pos='top', **draw_break_kws)
                break_positions.append((ax, 'top'))
        axs.append(ax)
    
    for ax, pos in break_positions:
        draw_breaks(ax, total_size, pos=pos, **draw_break_kws)
    return (fig, axs)
