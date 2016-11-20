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


snowflake_dict = {'faceted':'snowflake/faceted.png',
                    'wind packed':'snowflake/wind_packed.png',
                    'horizontal ice layer':'snowflake/ice.png',
                    'clustered rounded':'snowflake/cluster_rounded.png',
                    'wind broken':'snowflake/wind_broken_precip.png',
                    'rounded':'snowflake/large_rounded.png',
                    'faceted and rounded':'snowflake/faceted_rounded.png',
                    'rounded and faceted':'snowflake/rounding_faceted.png',
                    'depth hoar':'snowflake/hollow_cups.png',
                    'melt refreeze':'snowflake/melt_freeze_crust.png',
                    'melt refreeze crust':'snowflake/melt_freeze_crust.png',
                    'dendrites':'snowflake/'}
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

    def summary_plot(self, save=False):
        '''
        plot general snowpit plot
        :return:
        '''

        fig = plt.figure(figsize=(10, 10), dpi=150)
        # fig = plt.figure()
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
        fig.gca().invert_yaxis()
        im1 = ax1.plot(-self.snow_temperature, self.depth_temperature)

        im2 = ax2.barh(self.layer_top, np.repeat(1, self.layer_top.__len__()), self.layer_bot - self.layer_top,
                       color=cm.Blues(self.hardness_code / 6))
        ax2.set_xlim(0, 1)

        # include symbols

        for i, flake in enumerate(self.grain_type1.astype(str)):
            if flake != 'nan':
                im = plt.imread(snowflake_dict.get(flake))
                im[im == 0] = np.nan
                imagebox = OffsetImage(im, zoom=.02)
                if self.grain_type2.astype(str)[i] == 'nan':
                    hloc = 0.5
                else:
                    hloc = 0.33
                xy = [hloc,
                      ((self.layer_top[i] - self.layer_bot[i]) / 2 + self.layer_bot[i])]  # coordinates to position this image
                ab = AnnotationBbox(imagebox, xy, xycoords='data', boxcoords='data', frameon=False)
                ax2.add_artist(ab)

        for i, flake in enumerate(self.grain_type2.astype(str)):
            if flake != 'nan':
                im = plt.imread(snowflake_dict.get(flake))
                im[im == 0] = np.nan
                imagebox = OffsetImage(im, zoom=.02)
                xy = [0.66,
                      ((self.layer_top[i] - self.layer_bot[i]) / 2 + self.layer_bot[i])]  # coordinates to position this image
                ab = AnnotationBbox(imagebox, xy, xycoords='data', boxcoords='data', frameon=False)
                ax2.add_artist(ab)

        im3 = ax3.barh(self.layer_top, self.hardness_code, self.layer_bot - self.layer_top, color=cm.Blues(self.hardness_code / 6))
        ax3.set_xlim(0, 7)

        im4 = ax4.plot(self.density, self.depth_density)
        ax4.yaxis.tick_right()

        # add
        ax1.set_title("Temperature ($^\circ$C)")
        ax2.set_title("Stratigraphy")
        ax3.set_title("Hardness")
        ax4.set_title("Density")
        ax1.set_ylabel("Depth (cm)")

        ax1.grid()
        ax4.grid()

        plt.tight_layout()
        plt.subplots_adjust(wspace=0)
        if save==True:
            fig.savefig(self.filename.split('/')[-1][0:-4])


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
        try:
            for i, line in enumerate(f):
                if line[0:4] == 'Date':
                    self.date = line.split("\t")[1]
                    self.East = line.split("\t")[6]
                if line[0:4] == 'Time':
                    self.Elevation = line.split("\t")[5]
                if line[0:4] == 'Area':
                    self.North = line.split("\t")[7]
                if line[0:4] == 'Obse':
                    self.Observer = line.split("\t")[1]
                if line[0:4] == 'Air ':
                    self.AirTemp = line.split("\t")[2]
                if line[0:4] == 'Glac':
                    self.glacier = line.split("\t")[1]
                if line[0:4] == 'Glac':
                    self.weather_conditions = line.split("\t")[4]
                if line[0:4] == 'Gene':
                    self.comments = line.split("\t")[1]
        except ValueError:
            print "Could not load metadata. Check file formating"
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
import platform

if platform.system()=='Linux':
    filename = '/home/arcticsnow/github/snowpyt/data_example/kvg2_3.csv'
elif platform.system() == 'Darwin':
    filename = '/Users/tintino/Desktop/kbv2_3.txt'


a = Snowpit_svalbard_JC(filename)
a.filename = filename
a.load_csv()
a.summary_plot(save=True)

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
fig.gca().invert_yaxis()
im1 = ax1.plot(-a.snow_temperature, a.depth_temperature)

im2 = ax2.barh(a.layer_top, np.repeat(1,a.layer_top.__len__()), a.layer_bot-a.layer_top, color = cm.Blues(a.hardness_code/6))
ax2.set_xlim(0,1)

# include symbols

for i, flake in enumerate(a.grain_type1.astype(str)):
    if flake != 'nan':
        im = plt.imread(snowflake_dict.get(flake))
        im[im==0]=np.nan
        imagebox = OffsetImage(im, zoom=.02)
        if a.grain_type2.astype(str)[i]=='nan':
            hloc = 0.5
        else:
            hloc = 0.33
        xy = [hloc, ((a.layer_top[i]-a.layer_bot[i])/2+a.layer_bot[i])]               # coordinates to position this image
        ab = AnnotationBbox(imagebox, xy, xycoords='data', boxcoords='data',frameon=False)
        ax2.add_artist(ab)

for i, flake in enumerate(a.grain_type2.astype(str)):
    if flake != 'nan':
        im = plt.imread(snowflake_dict.get(flake))
        im[im==0]=np.nan
        imagebox = OffsetImage(im, zoom=.02)
        xy = [0.66, ((a.layer_top[i]-a.layer_bot[i])/2+a.layer_bot[i])]               # coordinates to position this image
        ab = AnnotationBbox(imagebox, xy, xycoords='data', boxcoords='data',frameon=False)
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
metadata=''
fig.suptitle(metadata)

# finalize and save as an image
plt.tight_layout()
plt.subplots_adjust(wspace=0)
fig.savefig('test.png')







f=open(filename)
for i, line in enumerate(f):
    if line[0:4] == 'Date':
        print line.split("\t")[1]
        print line.split("\t")[5]
    if line[0:4] == 'Time':
        print line.split("\t")[5]
    if line[0:4] == 'Area':
        print line.split()[6]
    if line[0:4] == 'Obse':
        print line.split("\t")
    if line[0:4] == 'Air ':
        print line.split("\t")[2]
    if line[0:4] == 'Glac':
        print line.split("\t")[1]
    if line[0:4] == 'Glac':
        print line.split("\t")[4]
    if line[0:4] == 'Gene':
        print line.split("\t")[1]


        self.North = split_f[20]
        self.Elevation = split_f[47]
        self.Observer = split_f[57]
        self.AirTemp = split_f[128]
        self.glacier = split_f[1]
        self.weather_conditions = split_f[4]
        self.comments = split_f[71] + "\n" + split_f[85]




