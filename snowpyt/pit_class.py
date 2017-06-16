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
from matplotlib.ticker import MaxNLocator


snowflake_dict = {'faceted':'snowflake/faceted.png',
                    'wind packed':'snowflake/wind_packed.png',
                    'wind slab':'snowflake/wind_packed.png',
                    'windslab':'snowflake/wind_packed.png',
                    'horizontal ice layer':'snowflake/ice.png',
                    'ice layer':'snowflake/ice.png',
                    'clustered rounded':'snowflake/cluster_rounded.png',
                    'cluster rounded':'snowflake/cluster_rounded.png',
                    'wind broken':'snowflake/wind_broken_precip.png',
                    'rounded':'snowflake/large_rounded.png',
                    'faceted and rounded':'snowflake/faceted_rounded.png',
                    'faceted rounded':'snowflake/faceted_rounded.png',
                    'rounded and faceted':'snowflake/rounding_faceted.png',
                    'rounded faceted':'snowflake/rounding_faceted.png',
                    'depth hoar':'snowflake/hollow_cups.png',
                    'hollow cups':'snowflake/hollow_cups.png',
                    'hollow prism':'snowflake/hollow_prism.png',
                    'melt refreeze':'snowflake/melt_freeze_crust.png',
                    'melt refreeze crust':'snowflake/melt_freeze_crust.png',
                    'partly decomposed': 'snowflake/partly_decomposed.png',
                    'recent snow':'snowflake/recent_snow.png',
                    'ice column':'snowflake/ice_column.png',
                    'percolation column':'snowflake/ice_column.png',
                    'percolation':'snowflake/ice_column.png',
                    'rounding depth hoar':'snowflake/rounding_depth_hoar.png',
                    'cavity crevasse hoar':'snowflake/cavity_crevasse_hoar.png',
                    'rounding surface hoar':'snowflake/rounding_surface_hoar.png',
                    'basal ice':'snowflake/basal_ice.png',
                    'rain crust':'snowflake/rain_crust.png',
                    'sun crust':'snowflake/sun_crust.png',
                    'surface hoar':'snowflake/surface_hoar.png',
                    'hoar frost':'snowflake/surface_hoar.png',
                    'rounded polycrystals':'snowflake/rounded_polycrystals.png',

                    'slush':'snowflake/slush.png',
                    'chains of depth hoar':'snowflake/chains_of_depth_hoar.png',
                    'near surface faceted':'snowflake/near_surface_faceted.png'}

class Snowpit(object):

    def __init__(self):
        self.date = '2001/08/10'
        self.East = 0
        self.North = 0
        self.Elevation = 0
        self.Observer = 'Bob'
        self.AirTemp = np.nan
        self.filename = 'example.txt'
        self.snowflakeDICT = snowflake_dict


class Snowpit_standard(object):
    '''
    Class for snowpit data formated as in Standard_pit.csv (tab delimiter)
    '''

    def __init__(self):
        self.date = '2001/08/10'
        self.East = 0
        self.North = 0
        self.Elevation = 0
        self.Observer = 'Bob'
        self.AirTemp = np.nan
        self.filename = 'example.txt'
        self.snowflakeDICT = snowflake_dict

    def summary_plot(self, save=False, metadata=True):
        '''
        Function to plot a summary of snowpit data

        :param save: save figure to hardrive as png
        :param metadata: boolean to include or not metadata information to figure
        :return:
        '''

        fig = plt.figure(figsize=(8, 4), dpi=150)

        if metadata:
            my_rowspan = 3
        else:
            my_rowspan = 4

        ax1 = plt.subplot2grid((4,4),(0,0),rowspan = my_rowspan)
        ax2 = plt.subplot2grid((4,4),(0,1),rowspan = my_rowspan, sharey=ax1)  # Share y-axes with subplot 1
        ax3 = plt.subplot2grid((4,4),(0,2),rowspan = my_rowspan, sharey=ax2)
        ax4 = plt.subplot2grid((4,4),(0,3),rowspan = my_rowspan, sharey=ax3)

        # Set y-ticks of subplot 2 invisible
        plt.setp(ax2.get_yticklabels(), visible=False)
        plt.setp(ax2.get_xticklabels(), visible=False)
        plt.setp(ax3.get_yticklabels(), visible=False)
        plt.setp(ax4.get_yticklabels(), visible=False)

        # Plot data
        fig.gca().invert_yaxis()
        im1 = ax1.plot(-self.temperature_snow, self.temperature_depth)

        im2 = ax2.barh(self.layer_bot-(self.layer_bot-self.layer_top)/2, np.repeat(1, self.layer_top.__len__()), - (self.layer_bot - self.layer_top),
                       color=cm.Blues(self.hardness_code / 7), edgecolor='k', linewidth=0.5)
        ax2.set_xlim(0, 1)

        # include sample name on pit face
        for i, sample in enumerate(self.sample_name):


        # include snowflake symbols
        for i, flake in enumerate(self.grain_type1.astype(str)):
            if flake != 'nan':
                print 'flake 1'
                print flake
                im = plt.imread(snowflake_dict.get(flake))
                im[im == 0] = np.nan
                imagebox = OffsetImage(im, zoom=.01)
                if (self.grain_type2.astype(str)[i] == 'nan') and (self.grain_type3.astype(str)[i] == 'nan'):
                    hloc = 0.5
                elif (self.grain_type2.astype(str)[i] != 'nan') and (self.grain_type3.astype(str)[i] == 'nan'):
                    hloc = 0.33
                else:
                    hloc = 0.25

                xy = [hloc,
                      ((self.layer_top[i] - self.layer_bot[i]) / 2 + self.layer_bot[i])]  # coordinates to position this image
                ab = AnnotationBbox(imagebox, xy, xycoords='data', boxcoords='data', frameon=False)
                ax2.add_artist(ab)

        for i, flake in enumerate(self.grain_type2.astype(str)):
            if flake != 'nan':
                print 'flake 2'
                print flake
                im = plt.imread(snowflake_dict.get(flake))
                im[im == 0] = np.nan
                imagebox = OffsetImage(im, zoom=.01)
                if (self.grain_type2.astype(str)[i] != 'nan') and (self.grain_type3.astype(str)[i] == 'nan'):
                    hloc2 = 0.66
                else:
                    hloc2 = 0.5
                xy = [hloc2,
                      ((self.layer_top[i] - self.layer_bot[i]) / 2 + self.layer_bot[i])]  # coordinates to position this image
                ab = AnnotationBbox(imagebox, xy, xycoords='data', boxcoords='data', frameon=False)
                ax2.add_artist(ab)

        for i, flake in enumerate(self.grain_type3.astype(str)):
            if flake != 'nan':
                print 'flake 3'
                print flake
                im = plt.imread(snowflake_dict.get(flake))
                im[im == 0] = np.nan
                imagebox = OffsetImage(im, zoom=.01)
                xy = [0.75,
                      ((self.layer_top[i] - self.layer_bot[i]) / 2 + self.layer_bot[i])]  # coordinates to position this image
                ab = AnnotationBbox(imagebox, xy, xycoords='data', boxcoords='data', frameon=False)
                ax2.add_artist(ab)

        im3 = ax3.barh(self.layer_bot-(self.layer_bot-self.layer_top)/2, self.hardness_code, self.layer_bot - self.layer_top, color=cm.Blues(self.hardness_code / 7), edgecolor='k', linewidth=0.5)
        ax3.set_xlim(0, 8)

        im4 = ax4.plot(self.density, self.density_depth)
        ax4.yaxis.tick_right()

        # add
        ax1.set_title("Temperature ($^\circ$C)")
        ax2.set_title("Stratigraphy")
        ax3.set_title("Hardness")
        ax4.set_title("Density")
        ax1.set_ylabel("Depth (cm)")

        for tick in ax1.get_xticklabels():
            tick.set_rotation(45)

        labels_ax3 = ['','Feast', '4F', '3F','2F','1F','P','K']
        ax3.set_xticklabels(labels_ax3,rotation=45)
        ax3.xaxis.set_major_locator(MaxNLocator(integer=True, prune='upper'))

        ax1.grid()
        ax4.grid()

        if metadata:
            metadata_text = "Date: " + self.date + '; Time [24hr]: ' + self.Time + '\n' + \
                       "Observer: " + self.Observer + '\n' + \
                       "Location description: " + self.General_loc + '\n' + \
                       "East : " + self.East + ' ' + self.East_unit + '\n' + \
                       "North: " + self.North + ' ' + self.North_unit + '\n' + \
                       "Elevation: " + self.Elevation + ' ' + self.Elevation_unit + '\n' + \
                       "Weather Conditions: " + self.weather_conditions + '\n' + \
                       "Air temperature: " + self.AirTemp + '$^{\circ}C$' '\n' + \
                       "Comments: " + self.comments + '\n'

            plt.figtext(0.08, 0.12 , metadata_text,
                    horizontalalignment='left',
                    verticalalignment='center', wrap=True, fontsize=4)

        plt.tight_layout()
        plt.subplots_adjust(wspace=0)

        if save==True:
            fig.savefig(self.filename.split('/')[-1][0:-4])
            print 'Figure saved as ' + self.filename.split('/')[-1][0:-4] + '.png'

    def plot_temperature(self):
        '''
        Plot temperature profile

        TODO:
            - reverse depth axis
        '''
        plt.figure()
        plt.plot(self.temperature_snow, self.temperature_depth)
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
        plt.plot(self.density, self.density_depth)
        plt.xlabel('Density (kg/m3)')
        plt.ylabel('Depth (cm)')
        plt.title('Density profile')
        plt.grid()

    def load_csv(self):
        self.load_metadata()
        self.load_profile()

    def load_profile(self):
        f = open(self.filename)
        for k,line in enumerate(f):
            if line[0:12] == 'Stratigraphy':
                break
        f.close()

        self.profile_raw_table = pd.read_csv(self.filename, sep='\t', skiprows=k+1)
        self.layerID = self.profile_raw_table['Layer ID']
        self.layer_top = self.profile_raw_table['Top [cm]']
        self.layer_bot = self.profile_raw_table['Bottom [cm]']

        self.grain_type1 = self.profile_raw_table['Type 1']
        self.grain_type2 = self.profile_raw_table['Type 2']
        self.grain_type3 = self.profile_raw_table['Type 3']
        self.grain_size_min = self.profile_raw_table['Diameter min [mm]']
        self.grain_size_max = self.profile_raw_table['Diameter max [mm]']

        self.hardness = self.profile_raw_table['Hardness']
        self.hardness_code = self.profile_raw_table['Hardness code']

        self.density_depth = self.profile_raw_table['Depth Center [cm]']
        self.density = self.profile_raw_table['Snow Density [g/cm3]']

        self.temperature_depth = self.profile_raw_table['Depth [cm]']
        self.temperature_snow = self.profile_raw_table['Temp [deg C]']

        self.sample_depth = self.profile_raw_table['Depth Center [cm].1']
        self.sample_name = self.profile_raw_table['ID_sample'].astype(str)


    def load_metadata(self):
        f = open(self.filename)
        try:
            for i, line in enumerate(f):
                if line[0:4] == 'Date':
                    self.date = line.split("\t")[1]
                if line[0:4] == 'Time':
                    self.Time = line.split("\t")[1]
                if line[0:4] == 'Gene':
                    self.General_loc = line.split("\t")[1]
                if line[0:4] == 'East':
                    self.East = line.split("\t")[1]
                    self.East_unit = line.split("\t")[2]
                if line[0:4] == 'Nort':
                    self.North = line.split("\t")[1]
                    self.North_unit = line.split("\t")[2]
                if line[0:4] == 'Elev':
                    self.Elevation = line.split("\t")[1]
                    self.Elevation_unit = line.split("\t")[2]
                if line[0:4] == 'Obse':
                    self.Observer = line.split("\t")[1]
                if line[0:4] == 'Air ':
                    self.AirTemp = line.split("\t")[1]
                if line[0:4] == 'Weat':
                    self.weather_conditions = line.split("\t")[1]
                if line[0:4] == 'Comm':
                    self.comments = line.split("\t")[1]
        except ValueError:
            print "Could not load metadata. Check file formating"
        f.close()

    def print_metadata(self):
        print "===================================="
        print "Date: " + self.date
        print "Observer: " + self.Observer
        print "------------------------------------"
        print "Location: " + self.General_loc
        print "East: " + self.East + ' ' + self.East_unit
        print "North: " + self.North + ' ' + self.North_unit
        print "Elevation: " + self.Elevation + ' ' + self.Elevation_unit
        print "------------------------------------"
        print "Air temperature [C]: " + self.AirTemp
        print "Weather conditions: " + self.weather_conditions
        print "------------------------------------"
        print "Comments: " + self.comments
        print "===================================="


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
        ax1 = plt.subplot2grid((4,4),(0,0),rowspan = 3)
        ax2 = plt.subplot2grid((4,4),(0,1),rowspan = 3, sharey=ax1)  # Share y-axes with subplot 1
        ax3 = plt.subplot2grid((4,4),(0,2),rowspan = 3, sharey=ax2)
        ax4 = plt.subplot2grid((4,4),(0,3),rowspan = 3, sharey=ax3)

        # Set y-ticks of subplot 2 invisible
        plt.setp(ax2.get_yticklabels(), visible=False)
        plt.setp(ax2.get_xticklabels(), visible=False)
        plt.setp(ax3.get_yticklabels(), visible=False)
        plt.setp(ax4.get_yticklabels(), visible=False)

        # Plot data
        fig.gca().invert_yaxis()
        im1 = ax1.plot(-self.temperature_snow, self.temperature_depth)

        im2 = ax2.barh(self.layer_top, np.repeat(1, self.layer_top.__len__()), self.layer_bot - self.layer_top,
                       color=cm.Blues(self.hardness_code / 7))
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

        im4 = ax4.plot(self.density, self.density_depth)
        ax4.yaxis.tick_right()

        # add
        ax1.set_title("Temperature ($^\circ$C)")
        ax2.set_title("Stratigraphy")
        ax3.set_title("Hardness")
        ax4.set_title("Density")
        ax1.set_ylabel("Depth (cm)")

        ax1.grid()
        ax4.grid()

        metadata = "Date: " + self.date + '\n' + \
                   "Observer: " + self.Observer + '\n' + \
                   "Glacier: " + self.glacier + '\n' + \
                   "East : " + self.East + '\n' + \
                   "North: " + self.North + '\n' + \
                   "Elevation: " + self.Elevation + '\n' + \
                   "Weather Conditions: " + self.weather_conditions + '\n' + \
                   "Air temperature: " + self.AirTemp + '\n' + \
                   "Comments: " + self.comments + '\n'
        left, width = .25, .5
        bottom, height = .25, .5
        right = left + width
        top = bottom + height

        plt.figtext(0.08, 0.15 , metadata,
                horizontalalignment='left',
                verticalalignment='center',wrap=True, fontsize=6)
        #fig.autofmt_xdate()

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
        plt.plot(self.temperature_snow, self.temperature_depth)
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
        plt.plot(self.density, self.density_depth)
        plt.xlabel('Density (kg/m3)')
        plt.ylabel('Depth (cm)')
        plt.title('Density profile')
        plt.grid()

    def load_csv(self):
        self.load_metadata()
        self.load_profile()

    def load_profile(self):
        self.profile_raw_table = pd.read_csv(self.filename, sep='\t', skiprows=14)
        self.layerID = self.profile_raw_table['Layer']
        self.layer_top = self.profile_raw_table['Top [cm]']
        self.layer_bot = self.profile_raw_table['Bottom [cm]']

        self.grain_type1 = self.profile_raw_table['Type 1']
        self.grain_type2 = self.profile_raw_table['Type 2']
        self.grain_type2 = self.profile_raw_table['Type 3']
        self.grain_size_min = self.profile_raw_table['Diameter min [mm]']
        self.grain_size_max = self.profile_raw_table['Diameter max [mm]']

        self.hardness = self.profile_raw_table['Hardness']
        self.hardness_code = self.profile_raw_table['Hardness code']

        self.density_depth = self.profile_raw_table['Depth Center [cm]']
        self.density = self.profile_raw_table['Snow Density [g/cm3]']

        self.temperature_depth = self.profile_raw_table['Depth [cm]']
        self.temperature_snow = self.profile_raw_table['Temp [deg C]']

        self.depth_sample = self.profile_raw_table['Depth Center [cm].1']
        self.name_sample = self.profile_raw_table['ID_sample']



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





