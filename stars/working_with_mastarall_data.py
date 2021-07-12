#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 25 08:49:25 2021

@author: astrophysics and python
"""

import os
import warnings

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from astropy.io import fits

import mastar_goodspec_functions as mgf
import mastarall_functions as maf

warnings.filterwarnings('ignore')

solar_radius, solar_mass, solar_luminosity, solar_temperature, solar_g = 695700000, 1.9884E30, 3.828E26, 5800, 274

T_label, g_label, M_label = 'Temperature [K]', 'Surface gravity ' + r'[m/s$^2$]', 'Mass [kg]'
R_label, L_label = 'Radius [m]', 'Luminosity [J/s]'

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

current_working_directory = os.getcwd()

image_folder = [f for f in os.listdir(os.curdir) if os.path.isdir(f) and f.startswith('mastargood')][0]

os.chdir(image_folder)

plots_req = list(range(0, 2306))

mgf.plotting_spectrum(plotting_device=plt, data_frame=merged_df, num_plots=plots_req)

os.chdir(current_working_directory)

par_list = np.array(mgf.get_stellar_parameters(data_frame=merged_df, num_plots=plots_req))

parameter_df = pd.DataFrame(par_list)
parameter_df.columns = ['temperature', 'g', 'mass', 'radius', 'luminosity']

for i in list(parameter_df.keys()):
    print(f'\n------------\n{i.capitalize()}\n------------')
    maf.statistics(parameter_df[i])
    print('\n')

plt.figure()
_ = plt.hist(np.log(parameter_df['temperature'] / solar_temperature), bins=32)
plt.ylabel('Number of stars')
plt.xlabel('log(T/' + r'T$_0$)')
plt.tight_layout()
plt.figure()
_ = plt.hist(np.log(parameter_df['g'] / solar_g), bins=32)
plt.ylabel('Number of stars')
plt.xlabel('log(g/' + r'g$_0$)')
plt.tight_layout()
plt.figure()
_ = plt.hist(np.log(parameter_df['mass'] / solar_mass), bins=32)
plt.ylabel('Number of stars')
plt.xlabel('log(M/' + r'M$_0$)')
plt.tight_layout()
plt.figure()
_ = plt.hist(np.log(parameter_df['radius'] / solar_radius), bins=32)
plt.ylabel('Number of stars')
plt.xlabel('log(R/' + r'R$_0$)')
plt.tight_layout()
plt.figure()
_ = plt.hist(np.log(parameter_df['luminosity'] / solar_luminosity), bins=32)
plt.ylabel('Number of stars')
plt.xlabel('log(L/' + r'L$_0$)')
plt.tight_layout()

mgf.two_dimensional_plots(data_frame=parameter_df, x_val='temperature', y_val='g', x_lab=T_label, y_lab=g_label,
                          x_log=False, y_log=True)

mgf.two_dimensional_plots(parameter_df, 'temperature', 'mass', T_label, M_label, False, True)

mgf.two_dimensional_plots(parameter_df, 'temperature', 'radius', T_label, R_label, False, True)

mgf.two_dimensional_plots(parameter_df, 'temperature', 'luminosity', T_label, L_label, False, True)

mgf.two_dimensional_plots(parameter_df, 'g', 'mass', g_label, M_label, False, True)

mgf.two_dimensional_plots(parameter_df, 'g', 'radius', g_label, R_label, False, False)

mgf.two_dimensional_plots(parameter_df, 'g', 'luminosity', g_label, L_label, False, True)

mgf.two_dimensional_plots(parameter_df, 'luminosity', 'mass', L_label, M_label, True, True)

mgf.two_dimensional_plots(parameter_df, 'luminosity', 'radius', L_label, R_label, True, True)

mgf.two_dimensional_plots(parameter_df, 'mass', 'radius', M_label, R_label, True, True)
