#!/usr/bin/python

'''
File defining a python class for snowpit data

November 2016, Simon Filhol
'''

from __future__ import division
import pickle
import numpy as np
import pandas as pd
import xlrd, inspect, os
import CAAML_xml as cx
import parse_xlsx as px

from matplotlib import pyplot as plt
import matplotlib.cm as cm
from matplotlib.offsetbox import AnnotationBbox, OffsetImage
from matplotlib.ticker import MaxNLocator

path2snowflake = os.path.dirname(inspect.getfile(px))+'/'

snowflake_dict = {'basal ice':'snowflake/basal_ice.png',
                    'cavity crevasse hoar':'snowflake/cavity_crevasse_hoar.png',
                    'chains of depth hoar':'snowflake/chains_of_depth_hoar.png',
                    'clustered rounded':'snowflake/cluster_rounded.png',
                    'cluster rounded':'snowflake/cluster_rounded.png',
                    'depth hoar':'snowflake/hollow_cups.png',
                    'faceted':'snowflake/faceted.png',
                    'faceted and rounded':'snowflake/faceted_rounded.png',
                    'faceted rounded':'snowflake/faceted_rounded.png',
                    'hollow cups':'snowflake/hollow_cups.png',
                    'hollow prism':'snowflake/hollow_prism.png',
                    'hoar frost':'snowflake/surface_hoar.png',
                    'horizontal ice layer':'snowflake/ice.png',
                    'ice':'snowflake/ice.png',
                    'ice column':'snowflake/ice_column.png',
                    'ice layer':'snowflake/ice.png',
                    'ice lenses':'snowflake/ice.png',
                    'melt refreeze':'snowflake/melt_freeze_crust.png',
                    'melt refreeze crust':'snowflake/melt_freeze_crust.png',
                    'melt freeze crust':'snowflake/melt_freeze_crust.png',
                    'near surface faceted':'snowflake/near_surface_faceted.png',
                    'partly decomposed': 'snowflake/partly_decomposed.png',
                    'percolation column':'snowflake/ice_column.png',
                    'percolation':'snowflake/ice_column.png',
                    'rain crust':'snowflake/rain_crust.png',
                    'recent snow':'snowflake/recent_snow.png',
                    'rounding depth hoar':'snowflake/rounding_depth_hoar.png',
                    'rounding surface hoar':'snowflake/rounding_surface_hoar.png',
                    'rounded':'snowflake/large_rounded.png',
                    'rounded and faceted':'snowflake/rounding_faceted.png',
                    'rounded faceted':'snowflake/rounding_faceted.png',
                    'rounded polycrystals':'snowflake/rounded_polycrystals.png',
                    'slush':'snowflake/slush.png',
                    'sun crust':'snowflake/sun_crust.png',
                    'surface hoar':'snowflake/surface_hoar.png',
                    'wind packed':'snowflake/wind_packed.png',
                    'wind slab':'snowflake/wind_packed.png',
                    'windslab':'snowflake/wind_packed.png',
                    'wind broken':'snowflake/wind_broken_precip.png'}

class layer(object):
    def __init__(self):
        self.dtop = None
        self.dtop_unit = None
        self.dbot = None
        #self.thickness = None
        self.thickness_unit = None
        self.grain_type1 = None
        self.grain_type2 = None
        self.grain_type3 = None
        self.grain_size_unit = None
        self.grain_size_avg = None
        self.gain_size_min = None
        self.grain_size_max = None
        self.hardness = None
        self.lwc = None
        self.id = None

        # # wrong syntax. Check how to have a automatic update of the following fields within the class:
        # if (self.dtop is not None) and (self.thickness is not None):
        #     self.dbot = self.dtop - self.thickness
        #
        # if (self.dtop is not None) and (self.dbot is not None):
        #     self.thickness = self.dtop - self.dbot

        # derive hardness code automatically

    # def __str__(self):
    #     return "-----layer object-----\ndepthTop={}{}\nthickness={}{}\ngrainFormPrimary={}\ngrainFormSecondary={}\ngrainSize\n\tavg={}{}\n\tavgMax={}{}\nhardness={}\nlwc={}".format(
    #         self.dtop, self.dtop_unit, self.thickness, self.thickness_unit, self.grain_type1, self.grain_type2,
    #         self.grain_size_avg, self.grain_size_unit, self.grain_size_max, self.grain_size_unit, self.hardness,
    #         self.lwc)

class temperature_profile(object):
    def __init__(self):
        self.depth = []
        self.depth_unit = None
        self.temp = []
        self.temp_unit = None

    def __str__(self):
        return "-----temperature profile-----\ndepth={} {}\ntemp={} {}".format(self.depth, self.depth_unit, self.temp,
                                                                               self.temp_unit)

class density_profile(object):
    def __init__(self):
        self.depth = []
        self.depth_unit = None
        self.thickness = []
        self.thickness_unit = None
        self.density = []
        self.density_unit = None

    def __str__(self):
        return "-----density profile-----\ndepth={} {}\nthickness={} {}\ndensity={} {}".format(self.depth,
                                                                                               self.depth_unit,
                                                                                     self.density_unit)

class sample_profile(object):
    def __init__(self):
        self.depth = []
        self.depth_unit = None
        self.sample_name = []
        self.sample_value = []
        self.sample_value_unit = None
        self.comments = None

class metadata(object):
    def __init__(self):
        self.date = None
        self.time = None
        self.operation = None
        self.observer = None
        self.profile_depth = None
        self.profile_depth_unit = None
        self.location_description = None
        self.srsName = None
        self.east = None
        self.east_unit = None
        self.north = None
        self.north_unit = None
        self.elevation = None
        self.elevation_unit = None
        self.sky_condition = None
        self.precipitation = None
        self.air_temperature = None
        self.air_temperature_unit = None
        self.windspeed = None
        self.windspeed_unit = None
        self.comments = None

    def __str__(self):
        return "-----metadata-----\ndate={}\noperation={}\nobserver={}\nprofile depth={} {}\nlocation description={}\nsrs name={}\nE={}\nN={}\nelevation={} {}\nsky condition={}\nprecipitation={}\nair temperature={} {}\nwindspeed={} {}\ncomments={}".format(
            self.date, self.operation, self.observer, self.profile_depth, self.profile_depth_unit,
            self.location_description, self.srsName, self.east, self.north, self.elevation, self.elevation_unit,
            self.sky_condition, self.precipitation, self.air_temperature, self.air_temperature_unit, self.windspeed,
            self.windspeed_unit, self.comments)

class Snowpit(object):

    # try to modify the snowpit class to use medata, layers and profile as class object
    def __init__(self):
        self.snowflakeDICT = snowflake_dict
        self.filename = None
        self.metadata = metadata()
        self.temperature_profile = temperature_profile()
        self.density_profile = density_profile()
        self.sample_profile = sample_profile()
        self.table = pd.DataFrame()
        self.layers = None
        self.units = None

        self.layers_top = None
        self.layers_bot = None

    def _extract_layers(self):
        # Function to reoganize layer data

        self.layers_bot = np.zeros(self.layers.__len__()) * np.nan
        self.layers_top = self.layers_bot * np.nan
        self.layers_hardness = self.layers_bot * np.nan
        self.layers_grainSize_min = self.layers_top * np.nan
        self.layers_grainSize_max = self.layers_top * np.nan
        self.layers_id = self.layers_top * np.nan
        self.layers_grainType1 = np.empty(self.layers.__len__(), dtype=object)
        self.layers_grainType2 = np.empty(self.layers.__len__(), dtype=object)
        self.layers_grainType3 = np.empty(self.layers.__len__(), dtype=object)

        for i, layer in enumerate(self.layers):
            print 'layer # ' + str(i)
            print layer.__dict__
            print layer.dbot
            self.layers_bot[i] = layer.dbot
            self.layers_top[i] = layer.dtop
            self.layers_hardness[i] = layer.hardness
            self.layers_grainSize_min[i] = layer.grain_size_min
            self.layers_grainSize_max[i] = layer.grain_size_max
            self.layers_id[i] = layer.id
            self.layers_grainType1[i] = layer.grain_type1
            self.layers_grainType2[i] = layer.grain_type2
            self.layers_grainType3[i] = layer.grain_type3

    def import_xml(self):
        # Load metadata
        self.metadata = cx.get_metadata(self.filename)

        # load temperature profile
        self.temperature_profile = cx.get_temperature(self.filename)

        # load density profile
        self.density_profile = cx.get_density()

        # load layers
        self.layers = cx.get_layers(self.filename)
        self._extract_layers()


    def print_xlsx_sheets(self):
        '''
        Function to print in console the sheets within the xlsx file
        :return:
        '''
        if self.filename[-4:]=='xlsx':
            print('File ' + self.filename + ' contains the following sheets:')
            px.sheet_names_xlsx(self.filename)
        else:
            print('The file is not of .xlsx format')


    def import_xlsx(self, sheet=None):
        if sheet == None:
            sheets = px.sheet_names_xlsx(self.filename)
            sheet = sheets[0]

        sh = px.open_xlsx(self.filename, sheetName=sheet)
        self.table, self.units = px.get_table(sh, self.filename)
        self.metadata = px.get_metadata(sh)
        self.density_profile = px.get_density(self.table)
        self.temperature_profile = px.get_temperature(self.table)
        self.layers = px.get_layers(self.table)
        self.sample_profile = px.get_sample(self.table)

        self._extract_layers()

        print 'Snowpit loaded from xlsx file'

    def import_csv(self):
        print 'Not implemented'

    #==========================

    def plot(self, save=False, metadata=False, plot_all=False,
                     plots_order=['temperature', 'density', 'crystal size', 'stratigraphy', 'hardness', 'sample values','sample names']):
        fig = plt.figure(figsize=(8, 4), dpi=150)

        if metadata:
            my_rowspan = 3
        else:
            my_rowspan = 4

        # ===========================================================
        # Automatically adjust summary plot based on data available
        ncol = plots_order.__len__()

        if ncol == 1:
            ax1 = plt.subplot2grid((4, ncol), (0, ncol - 1), rowspan=my_rowspan)
            axs_list = [ax1]

        if ncol == 2:
            ax1 = plt.subplot2grid((4, ncol), (0, ncol - 2), rowspan=my_rowspan)
            ax2 = plt.subplot2grid((4, ncol), (0, ncol - 1), rowspan=my_rowspan, sharey=ax1)
            axs_list = [ax1, ax2]

        if ncol == 3:
            ax1 = plt.subplot2grid((4, ncol), (0, ncol - 3), rowspan=my_rowspan)
            ax2 = plt.subplot2grid((4, ncol), (0, ncol - 2), rowspan=my_rowspan, sharey=ax1)
            ax3 = plt.subplot2grid((4, ncol), (0, ncol - 1), rowspan=my_rowspan, sharey=ax1)
            axs_list = [ax1, ax2, ax3]

        if ncol == 4:
            ax1 = plt.subplot2grid((4, ncol), (0, ncol - 4), rowspan=my_rowspan)
            ax2 = plt.subplot2grid((4, ncol), (0, ncol - 3), rowspan=my_rowspan, sharey=ax1)
            ax3 = plt.subplot2grid((4, ncol), (0, ncol - 2), rowspan=my_rowspan, sharey=ax1)
            ax4 = plt.subplot2grid((4, ncol), (0, ncol - 1), rowspan=my_rowspan, sharey=ax1)
            axs_list = [ax1, ax2, ax3, ax4]

        if ncol == 5:
            ax1 = plt.subplot2grid((4, ncol), (0, ncol - 5), rowspan=my_rowspan)
            ax2 = plt.subplot2grid((4, ncol), (0, ncol - 4), rowspan=my_rowspan, sharey=ax1)
            ax3 = plt.subplot2grid((4, ncol), (0, ncol - 3), rowspan=my_rowspan, sharey=ax1)
            ax4 = plt.subplot2grid((4, ncol), (0, ncol - 2), rowspan=my_rowspan, sharey=ax1)
            ax5 = plt.subplot2grid((4, ncol), (0, ncol - 1), rowspan=my_rowspan, sharey=ax1)
            axs_list = [ax1, ax2, ax3, ax4, ax5]

        if ncol == 6:
            ax1 = plt.subplot2grid((4, ncol), (0, ncol - 6), rowspan=my_rowspan)
            ax2 = plt.subplot2grid((4, ncol), (0, ncol - 5), rowspan=my_rowspan, sharey=ax1)
            ax3 = plt.subplot2grid((4, ncol), (0, ncol - 4), rowspan=my_rowspan, sharey=ax1)
            ax4 = plt.subplot2grid((4, ncol), (0, ncol - 3), rowspan=my_rowspan, sharey=ax1)
            ax5 = plt.subplot2grid((4, ncol), (0, ncol - 2), rowspan=my_rowspan, sharey=ax1)
            ax6 = plt.subplot2grid((4, ncol), (0, ncol - 1), rowspan=my_rowspan, sharey=ax1)
            axs_list = [ax1, ax2, ax3, ax4, ax5, ax6]

        if ncol == 7:
            ax1 = plt.subplot2grid((4, ncol), (0, ncol - 7), rowspan=my_rowspan)
            ax2 = plt.subplot2grid((4, ncol), (0, ncol - 6), rowspan=my_rowspan, sharey=ax1)
            ax3 = plt.subplot2grid((4, ncol), (0, ncol - 5), rowspan=my_rowspan, sharey=ax1)
            ax4 = plt.subplot2grid((4, ncol), (0, ncol - 4), rowspan=my_rowspan, sharey=ax1)
            ax5 = plt.subplot2grid((4, ncol), (0, ncol - 3), rowspan=my_rowspan, sharey=ax1)
            ax6 = plt.subplot2grid((4, ncol), (0, ncol - 2), rowspan=my_rowspan, sharey=ax1)
            ax7 = plt.subplot2grid((4, ncol), (0, ncol - 1), rowspan=my_rowspan, sharey=ax1)
            axs_list = [ax1, ax2, ax3, ax4, ax5, ax6, ax7]

        def to_plot(plot_order=plots_order, axis_list=axs_list):
            # function to plot plots based on the order indicated in plots_order
            plots_dict = {'temperature': plot_temperature,
                          'density': plot_density,
                          'stratigraphy': plot_stratigraphy,
                          'hardness': plot_hardness,
                          'crystal size': plot_crystalSize,
                          'sample names': plot_sample_names,
                          'sample values': plot_sample_values}
            for i, axs in enumerate(axis_list):
                plots_dict.get(plot_order[i])(axs)

        def plot_density(ax):
            if ax is ax1:
                ax.set_ylabel("Depth (cm)")
            else:
                plt.setp(ax.get_yticklabels(), visible=False)
                ax.yaxis.tick_right()
            im = ax.plot(self.density_profile.density, self.density_profile.depth)
            xlim = ax.get_xlim()

            # Add grid following the layering
            ax.barh(self.layers_bot - (self.layers_bot - self.layers_top) / 2,
                    np.repeat(xlim[1] - xlim[0], self.layers_top.__len__()), - (self.layers_bot - self.layers_top),
                    np.repeat(xlim[0], self.layers_top.__len__()),
                    color='w', alpha=0.2, edgecolor='k', linewidth=0.5, linestyle=':')
            ax.set_xlim(xlim)
            ax.grid(axis='x', linewidth=0.5, linestyle=':')
            ax.set_title("Density")
            for tick in ax.get_xticklabels():
                tick.set_rotation(45)
            return im

        def plot_temperature(ax):
            if ax is ax1:
                ax.set_ylabel("Depth (cm)")
            else:
                plt.setp(ax.get_yticklabels(), visible=False)
                ax.yaxis.tick_right()

            im = ax.plot(self.temperature_profile.temp, self.temperature_profile.depth)
            xlim = ax.get_xlim()

            # # Add grid following the layering
            ax.barh(self.layers_bot - (self.layers_bot - self.layers_top) / 2,
                     np.repeat(xlim[1] - xlim[0], self.layers_top.__len__()), - (self.layers_bot - self.layers_top),
                     np.repeat(xlim[0], self.layers_top.__len__()),
                     color='w', alpha=0.2, edgecolor='k', linewidth=0.5, linestyle=':')
            ax.set_xlim(xlim)
            ax.set_title("Temperature ($^\circ$C)")
            ax.grid(axis='x', linestyle=':', linewidth=0.5)

            for tick in ax.get_xticklabels():
                tick.set_rotation(45)
            return im

        def plot_stratigraphy(ax):
            if ax is ax1:
                ax.set_ylabel("Depth (cm)")
            else:
                plt.setp(ax.get_yticklabels(), visible=False)
                ax.yaxis.tick_right()
            plt.setp(ax.get_xticklabels(), visible=False)

            im2 = ax.barh(self.layers_bot-(self.layers_bot-self.layers_top)/2, np.repeat(1, self.layers_top.__len__()), - (self.layers_bot - self.layers_top),
                       color=cm.Blues(self.layers_hardness / 7), edgecolor='k', linewidth=0.5)
            ax.set_xlim(0, 1)

            # include sample name on pit face
            # for i, sample in enumerate(self.sample_name):


            # include snowflake symbols
            for i, flake in enumerate(self.layers_grainType1.astype(str)):
                if flake != 'nan':
                    if snowflake_dict.get(flake) is not None:

                        im = plt.imread(path2snowflake + snowflake_dict.get(flake))
                        im[im == 0] = np.nan
                        imagebox = OffsetImage(im, zoom=.01)
                        if (self.layers_grainType2.astype(str)[i] == 'nan') and (self.layers_grainType3.astype(str)[i] == 'nan'):
                            hloc = 0.5
                        elif (self.layers_grainType2.astype(str)[i] != 'nan') and (self.layers_grainType3.astype(str)[i] == 'nan'):
                            hloc = 0.33
                        else:
                            hloc = 0.25

                        xy = [hloc,
                              ((self.layers_top[i] - self.layers_bot[i]) / 2 + self.layers_bot[i])]  # coordinates to position this image
                        ab = AnnotationBbox(imagebox, xy, xycoords='data', boxcoords='data', frameon=False)
                        ax.add_artist(ab)
                    else:
                        print 'WARNING: [' + flake + '] is not a compatible snowflake type. Check spelling!'

            for i, flake in enumerate(self.layers_grainType2.astype(str)):
                if flake != 'nan':
                    if snowflake_dict.get(flake) is not None:
                        im = plt.imread(path2snowflake + snowflake_dict.get(flake))
                        im[im == 0] = np.nan
                        imagebox = OffsetImage(im, zoom=.01)
                        if (self.layers_grainType2.astype(str)[i] != 'nan') and (self.layers_grainType3.astype(str)[i] == 'nan'):
                            hloc2 = 0.66
                        else:
                            hloc2 = 0.5
                        xy = [hloc2,
                              ((self.layers_top[i] - self.layers_bot[i]) / 2 + self.layers_bot[i])]  # coordinates to position this image
                        ab = AnnotationBbox(imagebox, xy, xycoords='data', boxcoords='data', frameon=False)
                        ax.add_artist(ab)
                    else:
                        print 'WARNING: [' + flake + '] is not a compatible snowflake type. Check spelling!'

            for i, flake in enumerate(self.layers_grainType3.astype(str)):
                if flake != 'nan':
                    if snowflake_dict.get(flake) is not None:
                        im = plt.imread(path2snowflake + snowflake_dict.get(flake))
                        im[im == 0] = np.nan
                        imagebox = OffsetImage(im, zoom=.01)
                        xy = [0.75,
                              ((self.layers_top[i] - self.layers_bot[i]) / 2 + self.layers_bot[i])]  # coordinates to position this image
                        ab = AnnotationBbox(imagebox, xy, xycoords='data', boxcoords='data', frameon=False)
                        ax.add_artist(ab)
                    else:
                        print 'WARNING: [' + flake + '] is not a compatible snowflake type. Check spelling!'

            ax.set_title("Stratigraphy")
            return im2

        def plot_hardness(ax):
            plt.setp(ax.get_yticklabels(), visible=False)

            # Add grid following the layering
            im = ax.barh(self.layers_bot - (self.layers_bot - self.layers_top) / 2, self.layers_hardness,
                         self.layers_bot - self.layers_top, color=cm.Blues(self.layers_hardness / 7), edgecolor='k',
                         linewidth=0.5)

            ax.set_xlim(0, 8)
            ax.set_title("Hardness")
            labels_ax = ['', 'Feast', '4F', '3F', '2F', '1F', 'P', 'K']
            ax.set_xticklabels(labels_ax, rotation=45)
            ax.xaxis.set_major_locator(MaxNLocator(integer=True, prune='upper'))
            return im

        def plot_crystalSize(ax):
            if ax is ax1:
                ax.set_ylabel("Depth (cm)")
            else:
                plt.setp(ax.get_yticklabels(), visible=False)
                ax.yaxis.tick_right()
            im = ax.barh(self.layers_bot-(self.layers_bot-self.layers_top)/2, self.layers_grainSize_max-self.layers_grainSize_min, 1, self.layers_grainSize_min)
            xlim = ax.get_xlim()
            ax.barh(self.layers_bot - (self.layers_bot - self.layers_top) / 2,
                    np.repeat(xlim[1] - xlim[0], self.layers_top.__len__()), - (self.layers_bot - self.layers_top),
                    np.repeat(xlim[0], self.layers_top.__len__()),
                    color='w', alpha=0.2, edgecolor='k', linewidth=0.5, linestyle=':')
            ax.xaxis.set_ticks([0, 0.1, 0.2, 0.5, 1, 1.5, 2, 3, 4, 5, 10, 15, 20, 25, 30, 35, 40])
            ax.set_xlim(xlim)
            ax.set_title("Crystal size (mm)")
            ax.grid(axis='x', linewidth=0.5, linestyle=':')

            for tick in ax.get_xticklabels():
                tick.set_rotation(45)

            return im

        def plot_sample_values(ax):
            if ax is ax1:
                ax.set_ylabel("Depth (cm)")
            else:
                plt.setp(ax.get_yticklabels(), visible=False)
                ax.yaxis.tick_right()
            im = ax.plot(self.sample_profile.sample_value, self.sample_profile.depth)
            xlim = ax.get_xlim()

            # Add grid following the layering
            ax.barh(self.layers_bot - (self.layers_bot - self.layers_top) / 2,
                    np.repeat(xlim[1] - xlim[0], self.layers_top.__len__()), - (self.layers_bot - self.layers_top),
                    np.repeat(xlim[0], self.layers_top.__len__()),
                    color='w', alpha=0.2, edgecolor='k', linewidth=0.5, linestyle=':')
            ax.set_xlim(xlim)
            ax.grid(axis='x', linewidth=0.5, linestyle=':')
            ax.set_title("Sample Value")
            for tick in ax.get_xticklabels():
                tick.set_rotation(45)
            return im

        def plot_sample_names(ax):
            # add here code for plotting column of sample names
            ax.set_xlim([0,1])
            for i, name in enumerate(self.sample_profile.sample_name.astype(str)):
                if name != 'nan':
                    ax.text(0.5, self.sample_profile.depth[i], name,
                            bbox={'facecolor':'red', 'edgecolor':'none', 'alpha':0.5, 'pad':1},fontsize=5)

            xlim = ax.get_xlim()
            ax.barh(self.layers_bot - (self.layers_bot - self.layers_top) / 2,
                    np.repeat(xlim[1] - xlim[0], self.layers_top.__len__()), - (self.layers_bot - self.layers_top),
                    np.repeat(xlim[0], self.layers_top.__len__()),
                    color='w', alpha=0.2, edgecolor='k', linewidth=0.5, linestyle=':')
            ax.set_xlim(xlim)
            ax.set_title("Sample Name")
            plt.setp(ax.get_xticklabels(), visible=False)

        if metadata:
            metadata_text = "Date: " + self.metadata.date + '; Time [24hr]: ' + self.metadata.time + '\n' + \
                            "Observer: " + self.metadata.observer + '\n' + \
                            "Location description: " + self.metadata.location_description + '\n' + \
                            "East : " + self.metadata.east + ' ' + self.metadata.east_unit + '\n' + \
                            "North: " + self.metadata.north + ' ' + self.metadata.north_unit + '\n' + \
                            "Elevation: " + self.metadata.elevation + ' ' + self.metadata.elevation_unit + '\n' + \
                            "Weather Conditions: " + self.metadata.sky_conditions + '\n' + \
                            "Air temperature: " + self.metadata.air_temperature + '$^{\circ}C$' '\n' + \
                            "Comments: " + self.metadata.comments + '\n'

            plt.figtext(0.08, 0.12 , metadata_text,
                        horizontalalignment='left',
                        verticalalignment='center', wrap=True, fontsize=4)

        to_plot(plots_order, axs_list)
        fig.gca().invert_yaxis()
        plt.tight_layout()
        plt.subplots_adjust(wspace=0)

        if save == True:
            fig.savefig(self.filename.split('/')[-1][0:-4])
            print 'Figure saved as ' + self.filename.split('/')[-1][0:-4] + '.png'



    def print_metadata(self):
        print 'Not implemented [print_metadata()]'

    def print_layers(self):
        print 'Not implemented [print_layers()]'



