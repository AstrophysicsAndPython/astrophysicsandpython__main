#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  1 23:17:31 2021

@author: astrophysics and python
"""

import matplotlib.pyplot as plt
import numpy as np
from astropy.constants import codata2018 as cdata

h, c, k, G, sb = cdata.h.value, cdata.c.value, cdata.k_B.value, cdata.G.value, cdata.sigma_sb.value
solar_radius, solar_mass, solar_luminosity, solar_temperature, solar_g = 695700000, 1.9884E30, 3.828E26, 5800, 274


def planck_function(wavelength, temperature):
    w, t = wavelength, temperature
    p1 = 2 * h * pow(c, 2)
    p1 = p1 / pow(w, 5)

    p2 = (h * c) / (w * k * t)
    p2 = np.exp(p2) - 1
    p2 = 1. / p2

    return p1 * p2


def vacuum_to_air(wavelength):
    p1 = 1.0 + 2.735182E-4
    p2 = 131.4182 / wavelength**2
    p3 = 2.76249E8 / wavelength**4

    num, den = wavelength, p1 + p2 + p3

    return num / den


def format_label(number):
    if number <= 9:
        formatted_number = f'000{number}'
    elif 10 <= number <= 99:
        formatted_number = f'00{number}'
    elif 100 <= number <= 999:
        formatted_number = f'0{number}'
    elif 1000 <= number <= 9999:
        formatted_number = f'{number}'
    else:
        formatted_number = None

    return formatted_number


def get_mass_of_star(temperature, surface_gravity):
    _p1 = G * temperature**4
    _p2 = surface_gravity * solar_radius**2 * solar_temperature**4
    _p3 = (solar_mass**3.5) / 1.4
    return pow((_p1 / _p2) * _p3, 1 / 2.5)


def get_luminosity_of_the_star(mass_of_the_star):
    cond = mass_of_the_star / solar_mass
    if cond < 0.43:
        luminosity_of_the_star = solar_luminosity * 0.23 * cond**2.3
    elif 0.43 < cond < 2:
        luminosity_of_the_star = solar_luminosity * cond**4
    elif 2 < cond < 55:
        luminosity_of_the_star = 1.4 * solar_luminosity * cond**3.5
    else:
        luminosity_of_the_star = 32000 * solar_luminosity * cond
    return luminosity_of_the_star


def get_radius_of_star(luminosity, temperature):
    return (luminosity / (4 * np.pi * sb * temperature**4))**0.5


def plotting_spectrum(plotting_device, data_frame, num_plots=None):
    data_frame = data_frame.loc[num_plots, :]

    plt = plotting_device

    for i, v in enumerate(data_frame.itertuples()):
        plot_label = f'ID = {v[1]}\nT = {round(v[2], 4)}'
        plt.figure(figsize=(10, 5))

        wave, flux = v[4], v[5]

        pl = (planck_function(wavelength=wave * 1E-10, temperature=v[2]) * 1E-18) * 1E6

        plt.plot(wave, flux, label=plot_label)

        plt.xlabel('Wavelength [Angstrom]')
        plt.ylabel('Flux ' + r'[erg/s/cm$^2$/A]' + '\n' + r'$\times10^{-17}$')
        plt.legend(loc='best')

        plt.twinx()

        plt.plot(wave, pl, 'r')
        plt.ylabel('Black body radiation intensity\n[arbitrary units]')

        plt.tight_layout()
        plt.savefig(f'{format_label(i)}__{v[1]}')
        plt.close()


def get_stellar_parameters(data_frame, num_plots=None):
    data_frame = data_frame.loc[num_plots, :]

    new_list = []

    for i, v in enumerate(data_frame.itertuples()):
        temperature, log_g = v[2], np.exp(v[3])

        mass = get_mass_of_star(temperature=temperature, surface_gravity=log_g)
        luminosity = get_luminosity_of_the_star(mass_of_the_star=mass)
        radius = get_radius_of_star(luminosity=luminosity, temperature=temperature)

        new_list.append([temperature, log_g, mass, radius, luminosity])

    return new_list


def two_dimensional_plots(data_frame, x_val, y_val, x_lab, y_lab, x_log=False, y_log=False):
    plt.figure()
    plt.plot(data_frame[x_val], data_frame[y_val], 'r.')
    plt.xlabel(f'{x_lab}')
    plt.ylabel(f'{y_lab}')
    if y_log:
        plt.yscale('log')
    if x_log:
        plt.xscale('log')
    plt.tight_layout()
