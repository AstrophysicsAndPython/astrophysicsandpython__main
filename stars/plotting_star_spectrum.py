#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  1 23:17:31 2021

@author: astrophysics and python
"""

import numpy as np
from astropy.constants import codata2018 as cdata

h, c, k, G = cdata.h.value, cdata.c.value, cdata.k_B.value, cdata.G.value
sb, solRad, solMass, solLum = cdata.sigma_sb.value, 695700000, 1.9884E30, 3.828E26

def planck(wavelength, temperature):
    w, t = wavelength, temperature
    p1 = 2*h*pow(c, 2)
    p1 = p1/pow(w, 5)

    p2 = (h*c)/(w*k*t)
    p2 = np.exp(p2) - 1
    p2 = 1./p2

    return p1*p2

def vacuum_to_air(wavelength):
    p1 = 1.0 + 2.735182E-4
    p2 = 131.4182 / wavelength**2
    p3 = 2.76249E8 / wavelength**4

    num, den = wavelength, p1 + p2 + p3

    return num / den

def format_label(number):
    if number <= 9:
        out = f'000{number}'
    elif 10 <= number <= 99:
        out = f'00{number}'
    elif 100 <= number <= 999:
        out = f'0{number}'
    elif 1000 <= number <= 9999:
        out = f'{number}'

    return out


def plotting_stuff(plotting_surface):
    plt = plotting_surface
    plt.xlabel('Wavelength [Angstrom]')
    plt.ylabel('Flux ' + r'[erg/s/cm$^2$/A]' + '\n' + r'$\times10^{-17}$')
    plt.legend(loc='best')


def give_random(low_lim, up_lim):
    return np.random.uniform(low_lim, up_lim)

def temp_classification(temperature):
    if temperature < 3500:
        out = give_random(0.2, 0.6)
    elif 3500 < temperature < 5000:
        out = give_random(0.61, 1.05)
    elif 5000 < temperature < 6000:
        out = give_random(1.051, 1.25)
    elif 6000 < temperature < 7500:
        out = give_random(1.251, 2.3)
    elif 7500 < temperature < 11000:
        out = give_random(2.31, 6.0)
#    elif 11000 < temperature< 25000:
#        out = give_random(6.1, 13.0)
#    elif temperature > 25000:
#        out = give_random(13.1, 50.0)

    return out

def get_mass(surface_gravity, radius):
    return (surface_gravity*radius**2)/G


def plot_conditions(mastarall_df, num_plots):
    if num_plots == None:
        cond = list(mastarall_df['manga_id'])
        num_plots = [0]
    else:
        cond = list(mastarall_df['manga_id'])[num_plots[0]:num_plots[1]]

    return cond, num_plots


def get_the_list(mastarall_df, num_plots=None):

    cond, num_plots = plot_conditions(mastarall_df, num_plots)

    new_list = []

    for i, v in enumerate(cond, start=num_plots[0]):
        temp_id = np.where(mastarall_df['manga_id'] == v)[0][0]
        temp = mastarall_df['effective_temperature'][temp_id]

        log_g = 10**mastarall_df['log_surface_gravity'][temp_id]

        radius = temp_classification(temp)*solRad
        mass = get_mass(log_g, radius)

        new_list.append([temp, log_g, mass, radius])

    return new_list


def plotting_spectrum(plotting_device, mastarall_df, mastargood_df, plot_type, num_plots=None):
    plt = plotting_device

    cond, num_plots = plot_conditions(mastarall_df, num_plots)

    print(num_plots)

    for i, v in enumerate(cond, start=num_plots[0]):
        temp_id = np.where(mastarall_df['manga_id'] == v)[0][0]
        temp = mastarall_df['effective_temperature'][temp_id]

        plot_label = (f'ID = {v}\nT = {round(temp, 4)}')
        plt.figure(figsize=(10,5))

        wave_id = np.where(v == mastargood_df['manga_id'])[0]

        if plot_type == 'multiple':

            flux = mastargood_df['flux'][wave_id]
            wave = mastargood_df['wavelength'][wave_id]


            plt.title(f'{len(wave)} observation(s) present for MaNGA ID {v}')

            for j, w in enumerate(wave):
                if j == 0:
                    plt.plot(w, flux[j], label=plot_label)
                else:
                    plt.plot(w, flux[j])

            plotting_stuff(plt)

            plt.twinx()

            plt.ylabel('Black body radiation intensity\n[arbitrary units]')

            for j, w in enumerate(wave):
                pl = (planck(w*1E-10, temp)*1E-18)*1E6
                plt.plot(w, pl, 'r')

        elif plot_type == 'single':
            flux = mastargood_df['flux'][wave_id].iloc[0]
            wave = mastargood_df['wavelength'][wave_id].iloc[0]

            pl = (planck(wave*1E-10, temp)*1E-18)*1E6

            plt.plot(wave, flux, label=plot_label)

            plotting_stuff(plt)

            plt.twinx()

            plt.plot(wave, pl, 'r')
            plt.ylabel('Black body radiation intensity\n[arbitrary units]')
        else:
            print('Only \'multiple\' or \'single\' string is are allowed.')
            break

        plt.tight_layout()
        _get_out = format_label(i)
        plt.savefig(f'{_get_out}__{v}')
        plt.close()

def luminosity_of_the_star(radius, temperature, in_sol=False):
    _test = 4*np.pi*pow(radius, 2)*sb*pow(temperature, 4)
    if not in_sol:
        out = _test
    else:
        out = _test/solLum

    return out