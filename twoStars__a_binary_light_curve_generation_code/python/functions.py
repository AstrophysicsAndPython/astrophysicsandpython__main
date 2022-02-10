#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 13 06:43:31 2022

@author: Astrophysics and Python
"""

import matplotlib.pyplot as plt
import pandas as pd


def plot_lightcurve(x_axis, y_axis, csv_file, time_period):
    t = pd.read_csv(csv_file)
    t.columns = [i.strip() for i in list(t.keys())]

    plt.plot(t[x_axis] * time_period, t[y_axis], 'k-.')
    plt.gca().invert_yaxis()
    plt.xlabel('Period [d]')
    plt.ylabel('Bolometric magnitude')
    plt.grid('on')
    plt.tight_layout()
