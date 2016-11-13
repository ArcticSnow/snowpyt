#!/usr/bin/python

'''
File defining a python class for snowpit data

November 2016, Simon Filhol
'''
from __future__ import division
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.cm as cm
from matplotlib.offsetbox import AnnotationBbox, OffsetImage
from matplotlib._png import read_png

class Snowpit(object):

    def __init__(self):
        self.date = '2001/08/10'
        self.East = 0
        self.North = 0
        self.Elevation = 0
        self.Observer = 'Bob'
        self.AirTemp = np.nan
        self.filename = 'example.txt'


class Snowpit_svalbard_JC(Snowpit):
    '''
    Class for snowpit data as sorted by JC about Snow Svalbard Research
    '''

    def __init__(self, filename):
        super(Snowpit, self).__init__()
        self.filename = 'example.txt'

    def summary_plot(self):
        '''
        plot general snowpit plot
        :return:
        '''

        fig = plt.figure()

        ax1 = fig.add_subplot(1, 2, 1, aspect="equal")

        ax2 = fig.add_subplot(1, 2, 2, aspect="equal", sharey=ax1)  # Share y-axes with subplot 1
        #ax2.gca().invert_yaxis()
        # Set y-ticks of subplot 2 invisible
        plt.setp(ax2.get_yticklabels(), visible=False)


        # Plot data
        im1 = ax1.plot(self.snow_temperature, self.depth_temperature)
        ax1.gca().invert_yaxis()
        im2 = ax2.plot(self.density, self.depth_density)
        #im2.gca().invert_yaxis()
        plt.subplots_adjust(wspace=-.059)
        # subplot 0 - hardness
        # subplot 1 - stratigraphy
        # subplot 2 - density
        # subplot 3 - temperature

        # Include symbols


    def plot_temperature(self):
        '''
        Plot temperature profile

        TODO:
            - reverse depth axis
        '''
        plt.figure()
        plt.plot(self.snow_temperature, self.depth_temperature)
        plt.gca().invert_yaxis()
        plt.xlabel('Temperature (C)')
        plt.ylabel('Depth (cm)')
        plt.title('Temperature profile')
        plt.grid()

    def plot_density(self):
        '''
        Plot density profile

        TODO:
            - reverse depth axis
        '''
        plt.figure()
        plt.plot(self.density, self.depth_density)
        plt.xlabel('Density (kg/m3)')
        plt.ylabel('Depth (cm)')
        plt.title('Density profile')
        plt.grid()

    def load_csv(self):
        self.load_metadata()
        self.load_profile()

    def load_profile(self):
        self.profile_raw_table = pd.read_csv(self.filename, sep='\t', skiprows=14)
        self.layerID = self.profile_raw_table.ix[:,0]
        self.layer_top = self.profile_raw_table.ix[:,1]
        self.layer_bot = self.profile_raw_table.ix[:, 2]

        self.grain_type1 = self.profile_raw_table.ix[:,3]
        self.grain_type2 = self.profile_raw_table.ix[:, 4]
        self.grain_size_min = self.profile_raw_table.ix[:, 5]
        self.grain_size_max = self.profile_raw_table.ix[:, 6]

        self.hardness = self.profile_raw_table.ix[:, 7]
        self.hardness_code = self.profile_raw_table.ix[:, 8]

        self.depth_density = self.profile_raw_table.ix[:, 10]
        self.density = self.profile_raw_table.ix[:, 11]

        self.depth_temperature = self.profile_raw_table.ix[:,13]
        self.snow_temperature = self.profile_raw_table.ix[:, 14]


    def load_metadata(self):
        f = open(self.filename)
        split_f = f.readline().split("\t")
        self.date = split_f[29]
        self.East = split_f[34]
        self.North = split_f[20]
        self.Elevation = split_f[47]
        self.Observer = split_f[57]
        self.AirTemp = split_f[128]
        self.glacier = split_f[1]
        self.weather_conditions = split_f[4]
        self.comments = split_f[71] + "\n" + split_f[85]
        f.close()

    def print_metadata(self):
        print "Date: " + self.date
        print "East [deg]: " + self.East
        print "North [deg]: " + self.North
        print "Elevation [m]: " + self.Elevation
        print "Observer: " + self.Observer
        print "Air temperature [C]: " + self.AirTemp
        print "Glacier: " + self.glacier
        print "Weather conditions: " + self.weather_conditions
        print "Comments: " + self.comments


# testing TO BE DELETED
filename = '/Users/tintino/Desktop/kbv2_6.txt'


a = Snowpit_svalbard_JC(filename)
a.filename = filename
a.load_csv()
a.summary_plot()

####################################################
# Plotting tool in development

fig = plt.figure(figsize=(10,10),dpi=150)
#fig = plt.figure()
ax1 = fig.add_subplot(1, 4, 1)
ax2 = fig.add_subplot(1, 4, 2, sharey=ax1)  # Share y-axes with subplot 1
ax3 = fig.add_subplot(1, 4, 3, sharey=ax2)
ax4 = fig.add_subplot(1, 4, 4, sharey=ax3)

# Set y-ticks of subplot 2 invisible
plt.setp(ax2.get_yticklabels(), visible=False)
plt.setp(ax2.get_xticklabels(), visible=False)
plt.setp(ax3.get_yticklabels(), visible=False)
plt.setp(ax4.get_yticklabels(), visible=False)

# Plot data
plt.gca().invert_yaxis()
im1 = ax1.plot(-a.snow_temperature, a.depth_temperature)

im2 = ax2.barh(a.layer_top, np.repeat(1,a.layer_top.__len__()), a.layer_bot-a.layer_top, color = cm.Blues(a.hardness_code/6))
ax2.set_xlim(0,1)

# include symbols
im = plt.imread('snowflake/chains_of_depth_hoar.png')
im[im==0]=np.nan
imagebox = OffsetImage(im, zoom=.02)
xy = [0.25, 150]               # coordinates to position this image

ab = AnnotationBbox(imagebox, xy, xycoords='data', boxcoords='data',
    frameon=False)
ax2.add_artist(ab)


im3 = ax3.barh(a.layer_top, a.hardness_code, a.layer_bot-a.layer_top, color = cm.Blues(a.hardness_code/6))
ax3.set_xlim(0,7)

im4 = ax4.plot(a.density, a.depth_density)
ax4.yaxis.tick_right()

# add
ax1.set_title("Temperature ($^\circ$C)")
ax2.set_title("Stratigraphy")
ax3.set_title("Hardness")
ax4.set_title("Density")
ax1.set_ylabel("Depth (cm)")

ax1.grid()
ax4.grid()

# addind metadata information on layout:
metadata='sdsfaos;nfkajnsklbhbfjhwef\niebkbdksbdfkjbkuwbef\nsdfbehbwifeb'
fig.suptitle(metadata)

# finalize and save as an image
plt.tight_layout()
plt.subplots_adjust(wspace=0)
fig.savefig('test.png')















