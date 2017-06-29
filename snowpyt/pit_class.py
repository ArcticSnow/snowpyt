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
from openpyxl import load_workbook


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

        self.temp_plot = False
        self.density_plot = False
        self.stratigraphy_plot = False
        self.crystalsize_plot = False
        self.hardness_plot = False

    def summary_plot(self, save=False, metadata=True, plot_all=False, plots_order=['temperature', 'stratigraphy', 'hardness', 'crystal size', 'density']):
        '''
        Function to plot a summary of snowpit data

        :param save: save figure to hardrive as png
        :param metadata: boolean to include or not metadata information to figure
        :return:
        '''

        fig = plt.figure(figsize=(8, 4), dpi=150)
        fig.gca().invert_yaxis()

        if metadata:
            my_rowspan = 3
        else:
            my_rowspan = 4

        # ===========================================================
        # Automatically adjust summary plot based on data available
        ncol = plots_order.__len__()

        if ncol == 1:
            plt.subplot2grid((4, ncol), (0, ncol-1), rowspan=my_rowspan)

        if ncol == 2:
            ax1 = plt.subplot2grid((4, ncol), (0, ncol-2), rowspan=my_rowspan)
            ax2 = plt.subplot2grid((4, ncol), (0, ncol-1), rowspan=my_rowspan, sharey=ax1)

        if ncol == 3:
            ax1 = plt.subplot2grid((4, ncol), (0, ncol-3), rowspan=my_rowspan)
            ax2 = plt.subplot2grid((4, ncol), (0, ncol-2), rowspan=my_rowspan, sharey=ax1)
            ax3 = plt.subplot2grid((4, ncol), (0, ncol-1), rowspan=my_rowspan, sharey=ax1)

        if ncol == 4:
            ax1 = plt.subplot2grid((4, ncol), (0, ncol-4), rowspan=my_rowspan)
            ax2 = plt.subplot2grid((4, ncol), (0, ncol-3), rowspan=my_rowspan, sharey=ax1)
            ax3 = plt.subplot2grid((4, ncol), (0, ncol-2), rowspan=my_rowspan, sharey=ax1)
            ax4 = plt.subplot2grid((4, ncol), (0, ncol-1), rowspan=my_rowspan, sharey=ax1)

        if ncol == 5:
            ax1 = plt.subplot2grid((4, ncol), (0, ncol-5), rowspan=my_rowspan)
            ax2 = plt.subplot2grid((4, ncol), (0, ncol-4), rowspan=my_rowspan, sharey=ax1)
            ax3 = plt.subplot2grid((4, ncol), (0, ncol-3), rowspan=my_rowspan, sharey=ax1)
            ax4 = plt.subplot2grid((4, ncol), (0, ncol-2), rowspan=my_rowspan, sharey=ax1)
            ax5 = plt.subplot2grid((4, ncol), (0, ncol-1), rowspan=my_rowspan, sharey=ax1)

        if ncol == 6:
            ax1 = plt.subplot2grid((4, ncol), (0, ncol-6), rowspan=my_rowspan)
            ax2 = plt.subplot2grid((4, ncol), (0, ncol-5), rowspan=my_rowspan, sharey=ax1)
            ax3 = plt.subplot2grid((4, ncol), (0, ncol-4), rowspan=my_rowspan, sharey=ax1)
            ax4 = plt.subplot2grid((4, ncol), (0, ncol-3), rowspan=my_rowspan, sharey=ax1)
            ax5 = plt.subplot2grid((4, ncol), (0, ncol-2), rowspan=my_rowspan, sharey=ax1)
            ax6 = plt.subplot2grid((4, ncol), (0, ncol-1), rowspan=my_rowspan, sharey=ax1)


        def check_data_availability():
            # Function to check if data for the plot indicatted are available. If not only select plot where data exist form the list indicated

            if plot_all:
                # create a list with plots using all types of data available


            else:
                for data_type in plots_order:
                    # check the self. are not nan


        def to_plot(plots_order):
            # function to plot plots based on the order indicated in plots_order
            axs_dict = ['ax1', 'ax2', 'ax3', 'ax4', 'ax5']
            plots_dict = {'temperature':plot_temperature(),
                            'density':plot_density(),
                            'stratigraphy':plot_stratigraphy(),
                            'hardness':plot_hardness(),
                            'crystal size':plot_crystalSize()}
            for i,axs in enumerate(axs_dict[0:ncol-1]):
                plots_dict

        def plot_density(ax):
            plt.setp(ax.get_yticklabels(), visible=False)
            im = ax_dens.plot(self.density, self.density_depth)
            ax.yaxis.tick_right()
            ax.grid()
            ax.set_title("Density")
            return im

        def plot_temperature(ax):
            im = ax.plot(-self.temperature_snow, self.temperature_depth)
            ax.set_ylabel("Depth (cm)")
            ax.set_title("Temperature ($^\circ$C)")
            ax.grid()

            for tick in ax_temp.get_xticklabels():
                tick.set_rotation(45)
            return im

        def plot_stratigraphy(ax):
            plt.setp(ax.get_yticklabels(), visible=False)
            plt.setp(ax.get_xticklabels(), visible=False)

            im2 = ax.barh(self.layer_bot-(self.layer_bot-self.layer_top)/2, np.repeat(1, self.layer_top.__len__()), - (self.layer_bot - self.layer_top),
                       color=cm.Blues(self.hardness_code / 7), edgecolor='k', linewidth=0.5)
            ax.set_xlim(0, 1)

            # include sample name on pit face
            # for i, sample in enumerate(self.sample_name):


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
                    ax.add_artist(ab)

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
                    ax.add_artist(ab)

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
                    ax.add_artist(ab)

            ax.set_title("Stratigraphy")
            return im2

        def plot_hardness(ax):
            plt.setp(ax.get_yticklabels(), visible=False)
            im = ax.barh(self.layer_bot-(self.layer_bot-self.layer_top)/2, self.hardness_code, self.layer_bot - self.layer_top, color=cm.Blues(self.hardness_code / 7), edgecolor='k', linewidth=0.5)
            ax.set_xlim(0, 8)
            ax.set_title("Hardness")
            labels_ax = ['','Feast', '4F', '3F','2F','1F','P','K']
            ax.set_xticklabels(labels_ax,rotation=45)
            ax.xaxis.set_major_locator(MaxNLocator(integer=True, prune='upper'))
            return im


        def plot_crystalSize(ax):
            plt.setp(ax.get_yticklabels(), visible=False)
            im = ax.barh(self.layer_bot-(self.layer_bot-self.layer_top)/2, self.grain_size_max-self.grain_size_min, 1, self.grain_size_min)
            ax.set_title("Crystal size (mm)")
            return im

        def plot_sample_name(ax):
            # add here code for plotting column of sample names



        #====================================
        # INCLUDE HERE code to plot 
        #====================================


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

        # # Set y-ticks of subplot 2 invisible
        # plt.setp(ax_strat.get_yticklabels(), visible=False)
        # plt.setp(ax_strat.get_xticklabels(), visible=False)
        # plt.setp(ax_hard.get_yticklabels(), visible=False)
        # plt.setp(ax_csize.get_yticklabels(), visible=False)
        # plt.setp(ax_dens.get_yticklabels(), visible=False)

        # # Plot data
        # fig.gca().invert_yaxis()
        # im1 = ax_temp.plot(-self.temperature_snow, self.temperature_depth)

        # im2 = ax_strat.barh(self.layer_bot-(self.layer_bot-self.layer_top)/2, np.repeat(1, self.layer_top.__len__()), - (self.layer_bot - self.layer_top),
        #                color=cm.Blues(self.hardness_code / 7), edgecolor='k', linewidth=0.5)
        # ax_strat.set_xlim(0, 1)

        # # include sample name on pit face
        # # for i, sample in enumerate(self.sample_name):


        # # include snowflake symbols
        # for i, flake in enumerate(self.grain_type1.astype(str)):
        #     if flake != 'nan':
        #         print 'flake 1'
        #         print flake
        #         im = plt.imread(snowflake_dict.get(flake))
        #         im[im == 0] = np.nan
        #         imagebox = OffsetImage(im, zoom=.01)
        #         if (self.grain_type2.astype(str)[i] == 'nan') and (self.grain_type3.astype(str)[i] == 'nan'):
        #             hloc = 0.5
        #         elif (self.grain_type2.astype(str)[i] != 'nan') and (self.grain_type3.astype(str)[i] == 'nan'):
        #             hloc = 0.33
        #         else:
        #             hloc = 0.25

        #         xy = [hloc,
        #               ((self.layer_top[i] - self.layer_bot[i]) / 2 + self.layer_bot[i])]  # coordinates to position this image
        #         ab = AnnotationBbox(imagebox, xy, xycoords='data', boxcoords='data', frameon=False)
        #         ax_strat.add_artist(ab)

        # for i, flake in enumerate(self.grain_type2.astype(str)):
        #     if flake != 'nan':
        #         print 'flake 2'
        #         print flake
        #         im = plt.imread(snowflake_dict.get(flake))
        #         im[im == 0] = np.nan
        #         imagebox = OffsetImage(im, zoom=.01)
        #         if (self.grain_type2.astype(str)[i] != 'nan') and (self.grain_type3.astype(str)[i] == 'nan'):
        #             hloc2 = 0.66
        #         else:
        #             hloc2 = 0.5
        #         xy = [hloc2,
        #               ((self.layer_top[i] - self.layer_bot[i]) / 2 + self.layer_bot[i])]  # coordinates to position this image
        #         ab = AnnotationBbox(imagebox, xy, xycoords='data', boxcoords='data', frameon=False)
        #         ax_strat.add_artist(ab)

        # for i, flake in enumerate(self.grain_type3.astype(str)):
        #     if flake != 'nan':
        #         print 'flake 3'
        #         print flake
        #         im = plt.imread(snowflake_dict.get(flake))
        #         im[im == 0] = np.nan
        #         imagebox = OffsetImage(im, zoom=.01)
        #         xy = [0.75,
        #               ((self.layer_top[i] - self.layer_bot[i]) / 2 + self.layer_bot[i])]  # coordinates to position this image
        #         ab = AnnotationBbox(imagebox, xy, xycoords='data', boxcoords='data', frameon=False)
        #         ax_strat.add_artist(ab)

        # im3 = ax_hard.barh(self.layer_bot-(self.layer_bot-self.layer_top)/2, self.hardness_code, self.layer_bot - self.layer_top, color=cm.Blues(self.hardness_code / 7), edgecolor='k', linewidth=0.5)
        # ax_hard.set_xlim(0, 8)

        # im4 = ax_csize.barh(self.layer_bot-(self.layer_bot-self.layer_top)/2, self.grain_size_max-self.grain_size_min, 1, self.grain_size_min)

        # im5 = ax_dens.plot(self.density, self.density_depth)
        # ax_dens.yaxis.tick_right()

        # # add
        # ax_temp.set_title("Temperature ($^\circ$C)")
        # ax_strat.set_title("Stratigraphy")
        # ax_hard.set_title("Hardness")
        # ax_csize.set_title("Crystal size (mm)")
        # ax_dens.set_title("Density")
        # ax_temp.set_ylabel("Depth (cm)")

        # for tick in ax_temp.get_xticklabels():
        #     tick.set_rotation(45)

        # labels_ax_hard = ['','Feast', '4F', '3F','2F','1F','P','K']
        # ax_hard.set_xticklabels(labels_ax_hard,rotation=45)
        # ax_hard.xaxis.set_major_locator(MaxNLocator(integer=True, prune='upper'))

        # ax_temp.grid()
        # ax_dens.grid()

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

    def load_xslx_pit():
        # library openpyxl can do the work. Pandas also has a read_excel() function
        # https://openpyxl.readthedocs.io/en/default/usage.html

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

    def save_pickle_pit(self):
        # search how to save a python class to pickle
        self.

    def load_pickle_pit(self):
        # search how to read pickle file



