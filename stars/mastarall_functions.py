#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 22 11:31:33 2021

@author: astrophysics and python
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import describe as describe_statistics


def t_eff(pos):
    if pos == 'x':
        plt.xlabel('Effective Temperature [K]')
    else:
        plt.ylabel('Effective Temperature [K]')


def log_g(pos):
    if pos == 'x':
        plt.xlabel('Log surface gravity ' + r'[m/s$^2$]')
    else:
        plt.ylabel('Log surface gravity ' + r'[m/s$^2$]')


def make_hist_kde(data_frame, hist_bins):
    data_frame.plot.hist(bins=hist_bins)
    xmin, xmax = plt.gca().get_xlim()
    plt.legend(loc='best')
    if data_frame.name == 'effective_temperature':
        t_eff('x')
    else:
        log_g('x')
    plt.twinx()
    data_frame.plot.kde(color='r')
    plt.gca().set_ylim(bottom=0)
    plt.xlim(xmin, xmax)
    plt.tight_layout()

    return xmin, xmax


def make_histogram(plot_device, data_frame, key):
    plot_device.hist(data_frame[key], 128)
    if key == 'effective_temperature':
        plot_device.xlabel('Effective Temperature [K]')
    elif key == 'log_surface_gravity':
        plot_device.xlabel('Log surface gravity ' + r'[m/s$^2$]')
    plot_device.ylabel('Number of stars')
    plot_device.tight_layout()


def statistics(data_frame):
    n_obs, _, _mean, variance, _, _ = describe_statistics(data_frame)

    _min, _max, _median = min(data_frame), max(data_frame), np.median(data_frame)

    quantile = [round(data_frame.quantile(iterator), 4) for iterator in [0.25, 0.5, 0.75]]

    print(f'# of observations   = {round(n_obs, 4)}\n'
          f'Mean                = {_mean}\n'
          f'Median              = {_median}\n'
          f'Minimum             = {_min}\n'
          f'Maximum             = {_max}\n'
          f'Diff. b/w min/max   = {_max - _min}\n'
          f'Variance            = {round(variance, 4)}\n'
          f'Standard deviation  = {round(np.sqrt(variance), 4)}\n'
          f'Quantile .25/.5/.75 = {quantile[0]}, {quantile[1]}, {quantile[2]}')


def big_plot(data_frame, key, xlim_range):
    if key == 'effective_temperature':
        selected = data_frame[['effective_temperature', 'source_name']].groupby('source_name').effective_temperature
    else:
        selected = data_frame[['log_surface_gravity', 'source_name']].groupby('source_name').log_surface_gravity

    n_selected = selected.ngroups

    fig, axes = plt.subplots(n_selected // 2 + 1, 2, sharex=True, figsize=(14, 8))

    for i, (name, group) in enumerate(selected):
        r, c = i // 2, i % 2
        a1 = axes[r, c]
        a2 = a1.twinx()
        group.plot.hist(ax=a2, alpha=0.3, bins=16)
        group.plot.kde(title=name, ax=a1, c='r')

    selected.plot.kde(ax=axes[3, 1])
    plt.xlim(xlim_range[0], xlim_range[1])
    plt.tight_layout()
    axes[3, 1].legend(loc='best', ncol=4, frameon=False)

    return a1
