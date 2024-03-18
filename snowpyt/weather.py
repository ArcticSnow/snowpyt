"""
Function to plot weather in a vizualisation relevant to identify specific weather events (melt, precip, wind) to snow pack metamosphism
S. Filhol, march 2024

See Github issue: https://github.com/ArcticSnow/snowpyt/issues/6

- function to plot weather record
	- temperature, blue below freezing, red abod (add fill in)
	- wind fill in when above 6 m/s

- try to make the plot a bokeh plot for interactivity
"""



import pandas as pd 
import matplotlib.pyplot as plt  
import numpy as np  



def plot_weather_history(df):

	fig, ax = plt.subplots(3,1,sharex=True)

	# ax[0] plot temperature


	# ax[1] plot wind


	# ax[2] plot precipitation


