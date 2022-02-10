#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 13 06:14:33 2022

@author: Astrophysics and Python
"""

from functions import plot_lightcurve

P = 2.6284734

plot_lightcurve(x_axis='t/P', y_axis='Mbol', csv_file='YY_Sgr.csv', time_period=P)
