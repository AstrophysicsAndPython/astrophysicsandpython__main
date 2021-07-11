#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 25 08:49:25 2021

@author: astrophysics and python
"""

import warnings

import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from astropy.io import fits

from plotting_star_spectrum import plotting_spectrum, luminosity_of_the_star, get_the_list

warnings.filterwarnings('ignore')

mastarall = fits.open('mastarall-v2_4_3-v1_0_2.fits')[1]
mastargood = fits.open('mastar-goodspec-v2_4_3-v1_0_2.fits')[1]

mastarall_manga_id = mastarall.data['MANGAID']
log_surface_gravity = mastarall.data['INPUT_LOGG']
effective_temperature = mastarall.data['INPUT_TEFF']

mastarall_df = pd.DataFrame([mastarall_manga_id, effective_temperature, log_surface_gravity]).T
mastarall_df.columns = ['manga_id', 'effective_temperature', 'log_surface_gravity']

_mastarall_df = mastarall_df[(mastarall_df['effective_temperature'] > 0) & (mastarall_df['log_surface_gravity'] > 0)]
_mastarall_df.reset_index(drop=True, inplace=True)

_mastarall_df['effective_temperature'] = pd.to_numeric(_mastarall_df['effective_temperature'])
_mastarall_df['log_surface_gravity'] = pd.to_numeric(_mastarall_df['log_surface_gravity'])

mastargood_manga_id = mastargood.data['MANGAID']
wave = mastargood.data['WAVE']
flux = mastargood.data['FLUX']

mastargood_df = pd.DataFrame([mastargood_manga_id, wave, flux]).T
mastargood_df.columns = ['manga_id', 'wavelength', 'flux']

# removing the duplicate values
# taken from https://www.kite.com/python/answers/how-to-select-unique-pandas-dataframe-rows-in-python
mastargood_df = mastargood_df.drop_duplicates(subset=['manga_id']).reset_index(drop=True)

# getting common manga_id from both dataframes
# taken form https://stackoverflow.com/a/30535957
merged_df = pd.merge(_mastarall_df, mastargood_df, how='inner', on=['manga_id'])

curdir = os.getcwd()

fold = [f for f in os.listdir(os.curdir) if os.path.isdir(f) and f.endswith('images')][0]

os.chdir(fold)

plots_req = [0, len(_mastarall_df['manga_id'])]

#plotting_spectrum(plotting_device=plt, mastarall_df=_mastarall_df, mastargood_df=mastargood_df, plot_type='single', num_plots=plots_req)

stellar_parameter_list = get_the_list(mastarall_df=_mastarall_df, num_plots=plots_req)

lums = [luminosity_of_the_star(i[-1], i[0], True) for i in stellar_parameter_list]

plt.plot(np.array(stellar_parameter_list)[:, 0], lums, 'r.', ls='')
plt.yscale('log')
plt.xlabel('Temperature [K]')
plt.ylabel('Luminosity of the star [in Solar Luminosity]')
plt.gca().invert_xaxis()
#plt.savefig('temp_vs_lum.png')

os.chdir(curdir)
