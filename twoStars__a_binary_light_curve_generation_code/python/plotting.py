"""
Created on Thu Jan 13 06:14:33 2022
"""

import pandas as pd

from functions import plot_lightcurve

mydf = pd.read_csv('YY_Sgr.csv')
mydf.columns = [i.strip() for i in list(mydf.keys())]

P = 2.6284734

plot_lightcurve(df=mydf, x_axis='t/P', y_axis='Mbol', time_period=P)
