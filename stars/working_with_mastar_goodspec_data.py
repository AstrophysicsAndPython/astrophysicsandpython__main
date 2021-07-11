#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 25 08:49:25 2021

@author: astrophysics and python
"""

import os
import warnings

import numpy as np
import pandas as pd
from astropy.io import fits

from plotting_star_spectrum import get_stellar_parameters

warnings.filterwarnings('ignore')

mastarall = fits.open('mastarall-v2_4_3-v1_0_2.fits')[1]
mastargood = fits.open('mastar-goodspec-v2_4_3-v1_0_2.fits')[1]

mastarall_manga_id = mastarall.data['MANGAID']
log_surface_gravity = mastarall.data['INPUT_LOGG']
effective_temperature = mastarall.data['INPUT_TEFF']

_temp_df = pd.DataFrame([mastarall_manga_id, effective_temperature, log_surface_gravity]).T
_temp_df.columns = ['manga_id', 'effective_temperature', 'log_surface_gravity']

mastarall_df = _temp_df[(_temp_df['effective_temperature'] > 0) & (_temp_df['log_surface_gravity'] > 0)]
mastarall_df.reset_index(drop=True, inplace=True)

mastarall_df['effective_temperature'] = pd.to_numeric(mastarall_df['effective_temperature'])
mastarall_df['log_surface_gravity'] = pd.to_numeric(mastarall_df['log_surface_gravity'])

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
merged_df = pd.merge(mastarall_df, mastargood_df, how='inner', on=['manga_id'])

curdir = os.getcwd()

fold = [f for f in os.listdir(os.curdir) if os.path.isdir(f) and f.endswith('images')][0]

os.chdir(fold)

plots_req = list(range(0, 2306))

# plotting_spectrum(plotting_device=plt, data_frame=merged_df, num_plots=plots_req)

par_list = np.array(get_stellar_parameters(data_frame=merged_df, num_plots=plots_req))

os.chdir(curdir)
