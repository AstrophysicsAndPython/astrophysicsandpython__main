#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 19 23:28:12 2021

@author: astrophysics and python
"""

# libraries
import warnings

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from astropy.io import fits
from matplotlib.colors import LogNorm

from mastarall_functions import statistics, make_hist_kde, t_eff, log_g, big_plot

warnings.filterwarnings('ignore')

# loading the fits file
mastar_all = fits.open('mastarall-v2_4_3-v1_0_2.fits')[1]

# loading the required fields
manga_id = mastar_all.data['MANGAID']
source_name = mastar_all.data['INPUT_SOURCE']
log_surface_gravity = mastar_all.data['INPUT_LOGG']
effective_temperature = mastar_all.data['INPUT_TEFF']

# changing the fields into data frame
mastar_df = pd.DataFrame([manga_id, effective_temperature, log_surface_gravity, source_name]).T
mastar_df.columns = ['manga_id', 'effective_temperature', 'log_surface_gravity', 'source_name']

# creating a filter with effective_temperature > 0 and log_surface_gravity > 0
_mastar_df = mastar_df[(mastar_df['effective_temperature'] > 0) & (mastar_df['log_surface_gravity'] > 0)]
# drop the index and replace it with new index
_mastar_df.reset_index(drop=True, inplace=True)

# forcefully change the python data series type to numeric
# the filterwarnings('ignore') command is to remove the warnings that follow these commands
_mastar_df['effective_temperature'] = pd.to_numeric(_mastar_df['effective_temperature'])
_mastar_df['log_surface_gravity'] = pd.to_numeric(_mastar_df['log_surface_gravity'])

##############################################
# working on the data
##############################################

##############################################
# effective temperature
##############################################

# get the statistics
print('Statistics of effective temperature in the MaStar catalog\n')
statistics(_mastar_df['effective_temperature'])

# making a histogram and KDE plot
plt.figure()
min_x_teff, max_x_teff = make_hist_kde(_mastar_df['effective_temperature'], 64)

# making a displot
sns.displot(data=_mastar_df[['effective_temperature', 'source_name']], x='effective_temperature', hue='source_name',
            multiple='fill')
t_eff(pos='x')

# making a boxplot
plt.figure(figsize=(10, 5))
pd.plotting.boxplot(data=_mastar_df, column='effective_temperature', vert=False)
t_eff('x')
plt.tight_layout()

# separating the boxplots based on the source_name values
pd.plotting.boxplot(data=_mastar_df, column='effective_temperature', by='source_name', vert=False, figsize=(10, 5))
t_eff('x')
plt.suptitle('')
plt.title('Boxplot grouped by source_name')
plt.tight_layout()

# separating the histogram and KDE plots based on the source_name values
big_plot(_mastar_df, 'effective_temperature', [min_x_teff, max_x_teff])

##############################################
# log surface gravity
##############################################

# get the statistics
print('Statistics of log surface gravity in the MaStar catalog\n')
statistics(_mastar_df['log_surface_gravity'])

# making a histogram and KDE plot
plt.figure()
min_x_logg, max_x_logg = make_hist_kde(_mastar_df['log_surface_gravity'], 64)

# making a displot
sns.displot(data=_mastar_df[['log_surface_gravity', 'source_name']], x='log_surface_gravity', hue='source_name', multiple='fill')
log_g(pos='x')

# making a boxplot
plt.figure(figsize=(10, 5))
pd.plotting.boxplot(data=_mastar_df, column='log_surface_gravity', vert=False)
log_g('x')
plt.tight_layout()

# separating the boxplots based on the source_name values
pd.plotting.boxplot(data=_mastar_df, column='log_surface_gravity', by='source_name', vert=False, figsize=(10, 5))
log_g('x')
plt.suptitle('')
plt.title('Boxplot grouped by source_name')
plt.tight_layout()

# separating the histogram and KDE plots based on the source_name values
big_plot(_mastar_df, 'log_surface_gravity', [min_x_logg, max_x_logg])

##############################################
# effective temperature vs log surface gravity
##############################################

# 2D histogram
fig, ax = plt.subplots()
h = ax.hist2d(_mastar_df['effective_temperature'], _mastar_df['log_surface_gravity'], bins=128, norm=LogNorm())
ax.invert_xaxis()
fig.colorbar(h[3], ax=ax)
t_eff('x')
log_g('y')
plt.tight_layout()

# scatter plot
plt.figure()
sns.scatterplot(x='effective_temperature', y='log_surface_gravity', hue='source_name', data=_mastar_df)
plt.gca().invert_xaxis()
plt.tight_layout()

# pair-plot
f = sns.pairplot(data=_mastar_df, hue='source_name', corner=True)
f.fig.set_figwidth(13)
f.fig.set_figheight(8)
plt.show()
