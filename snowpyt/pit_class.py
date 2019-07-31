#!/usr/bin/python

'''
File defining a python class for snowpit data

November 2016, Simon Filhol
'''


import numpy as np
import pandas as pd
import os
import snowpyt.CAAMLv6_xml as cxv6
from snowpyt.snowflake.sf_dict import snowflake_symbol_dict
import snowpyt.snowflake.sf_dict as sfd

from matplotlib import pyplot as plt
import matplotlib.cm as cm
from matplotlib.offsetbox import AnnotationBbox, OffsetImage
from matplotlib.ticker import MaxNLocator

path2snowflake = cxv6.__file__[:-14] + '/'


class layer(object):
    def __init__(self):
        self.dtop = None
        self.dtop_unit = None
        self.dbot = None
        self.thickness = None
        self.thickness_unit = None
        self.grain_type1 = None
        self.grain_type2 = None
        self.grain_type3 = None
        self.grainSize_unit = None
        self.grainSize_mean = None
        self.grainSize_max = None
        self.hardness_ram = None
        self.hardness_index = None
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

class isotope_profile(object):
    def __init__(self):
        self.layer_top = []
        self.layer_bot = []
        self.depth_unit = None
        self.names = []
        self.values = []
        self.values_units = None

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
        self.winddir=None
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
        self.snowflakeDICT = snowflake_symbol_dict
        self.caaml_file = None
        self.isotopes_file = None
        self.metadata = metadata()
        self.temperature_profile = temperature_profile()
        self.density_profile = density_profile()
        self.sample_profile = sample_profile()
        self.isotope_profile = isotope_profile()
        self.table = pd.DataFrame()
        self.layers = None
        self.units = None

        self.layers_top = None
        self.layers_bot = None

    def _extract_layers(self):
        # Function to reoganize layer data

        self.layers_bot = np.zeros(self.layers.__len__()) * np.nan
        self.layers_top = self.layers_bot * np.nan
        self.layers_hardness_ram = self.layers_bot * np.nan
        self.layers_hardness_index = self.layers_bot * np.nan
        self.layers_grainSize_mean = self.layers_top * np.nan
        self.layers_grainSize_max = self.layers_top * np.nan
        self.layers_id = self.layers_top * np.nan
        self.layers_grainType1 = np.empty(self.layers.__len__(), dtype=object)
        self.layers_grainType2 = np.empty(self.layers.__len__(), dtype=object)
        self.layers_grainType3 = np.empty(self.layers.__len__(), dtype=object)

        for i, layer in enumerate(self.layers):
            print('layer # ' + str(i))
            print(layer.__dict__)
            self.layers_bot[i] = layer.dbot
            self.layers_top[i] = layer.dtop
            self.layers_hardness_index[i] = sfd.hardness_dict.get(layer.hardness)
            try:
                self.layers_hardness_ram[i] = 19.3 * self.layers_hardness_index[i] ** 2.4
            except:
                print('WARNING: no hardness data')
            self.layers_grainSize_mean[i] = layer.grainSize_mean
            self.layers_grainSize_max[i] = layer.grainSize_max
            self.layers_id[i] = layer.id
            self.layers_grainType1[i] = layer.grain_type1
            self.layers_grainType2[i] = layer.grain_type2
            self.layers_grainType3[i] = layer.grain_type3

    def import_caamlv6(self):
        # Load metadata
        self.metadata = cxv6.get_metadata(self.caaml_file)

        # load temperature profile
        self.temperature_profile = cxv6.get_temperature(self.caaml_file)

        # load density profile
        self.density_profile = cxv6.get_density(self.caaml_file)

        # load layers
        self.layers = cxv6.get_layers(self.caaml_file)
        self._extract_layers()


    def import_isotope_csv(self):
        self.isotope_profile.df = pd.read_csv(self.isotopes_file)
        self.isotope_profile.layer_top = self.isotope_profile.df.height_top
        self.isotope_profile.layer_bot = self.isotope_profile.df.height_bot
        self.isotope_profile.names = self.isotope_profile.df.columns[2:]

    def plot(self, save=False, metadata=False, invert_depth=False,
                     plots_order=['temperature', 'density', 'crystal size',
                                  'stratigraphy', 'hardness', 'sample values',
                                  'sample names', 'dD', 'd18O', 'd-ex']):
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
                          'sample values': plot_sample_values,
                          'dD': plot_dD,
                          'd18O': plot_d18O,
                          'd-ex': plot_d_ex}
            for i, axs in enumerate(axis_list):
                plots_dict.get(plot_order[i])(axs)

        def plot_dD(ax):
            if ax is ax1:
                ax.set_ylabel("Depth (cm)")
            else:
                plt.setp(ax.get_yticklabels(), visible=False)
                ax.yaxis.tick_right()

            im = ax.step(np.append(self.isotope_profile.df.dD.values[0], self.isotope_profile.df.dD.values),
                         np.append(self.isotope_profile.df.height_top.values,0), where='post')
            ax.set_title("dD ($^{o}/_{oo}$)")
            xlim = ax.get_xlim()

            # Add grid following the layering
            ax.barh(self.layers_bot - (self.layers_bot - self.layers_top) / 2,
                    np.repeat(xlim[1] - xlim[0], self.layers_top.__len__()), - (self.layers_bot - self.layers_top),
                    np.repeat(xlim[0], self.layers_top.__len__()),
                    color='w', alpha=0.2, edgecolor='k', linewidth=0.5, linestyle=':')
            ax.set_xlim(xlim)
            #ax.grid(axis='x', linewidth=0.5, linestyle=':')
            for tick in ax.get_xticklabels():
                tick.set_rotation(45)

            return im

        def plot_d18O(ax):
            if ax is ax1:
                ax.set_ylabel("Depth (cm)")
            else:
                plt.setp(ax.get_yticklabels(), visible=False)
                ax.yaxis.tick_right()

            im = ax.step(np.append(self.isotope_profile.df.d18O.values[0], self.isotope_profile.df.d18O.values),
                         np.append(self.isotope_profile.df.height_top.values, 0), where='post', color='#d62728')
            ax.set_title("d18O ($^{o}/_{oo}$)")
            xlim = ax.get_xlim()

            # Add shading for the ice type of isotope sample
            ax.barh(
                self.isotope_profile.layer_bot - (self.isotope_profile.layer_bot - self.isotope_profile.layer_top) / 2,
                np.repeat(xlim[1] - xlim[0], self.isotope_profile.layer_top.__len__()), - (self.isotope_profile.layer_bot - self.isotope_profile.layer_top),
                np.repeat(xlim[0], self.isotope_profile.layer_top.__len__()),
                color=cm.bone(pd.Categorical(self.isotope_profile.df.ice_type).codes), alpha=0.2)

            # Add grid following the layering
            ax.barh(self.layers_bot - (self.layers_bot - self.layers_top) / 2,
                    np.repeat(xlim[1] - xlim[0], self.layers_top.__len__()), - (self.layers_bot - self.layers_top),
                    np.repeat(xlim[0], self.layers_top.__len__()),
                    color='w', alpha=0.2, edgecolor='k', linewidth=0.5, linestyle=':')
            ax.set_xlim(xlim)
            ax.grid(axis='x', linewidth=0.5, linestyle=':')
            for tick in ax.get_xticklabels():
                tick.set_rotation(45)
            return im

        def plot_d_ex(ax):
            if ax is ax1:
                ax.set_ylabel("Depth (cm)")
            else:
                plt.setp(ax.get_yticklabels(), visible=False)
                ax.yaxis.tick_right()

            im = ax.step(np.append(self.isotope_profile.df.dxs.values[0], self.isotope_profile.df.dxs.values),
                         np.append(self.isotope_profile.df.height_top.values, 0), where='post', color='#2ca02c')
            ax.set_title("d-excess ($^{o}/_{oo}$)")
            xlim = ax.get_xlim()

            # Add grid following the layering
            ax.barh(self.layers_bot - (self.layers_bot - self.layers_top) / 2,
                    np.repeat(xlim[1] - xlim[0], self.layers_top.__len__()), - (self.layers_bot - self.layers_top),
                    np.repeat(xlim[0], self.layers_top.__len__()),
                    color='w', alpha=0.2, edgecolor='k', linewidth=0.5, linestyle=':')
            ax.set_xlim(xlim)
            ax.grid(axis='x', linewidth=0.5, linestyle=':')
            for tick in ax.get_xticklabels():
                tick.set_rotation(45)
            return im

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

            im2 = ax.barh(self.layers_bot-(self.layers_bot-self.layers_top)/2,
                          np.repeat(1, self.layers_top.__len__()), - (self.layers_bot - self.layers_top),
                          color=cm.Blues(self.layers_hardness_index / 6), edgecolor='k', linewidth=0.5)

            #edgecolor='k', linewidth=0.5)
            ax.set_xlim(0, 1)

            # include sample name on pit face
            # for i, sample in enumerate(self.sample_name):


            # include snowflake symbols
            for i, flake in enumerate(self.layers_grainType1.astype(str)):
                if flake == 'nan':
                    flake = None
                if flake != None:
                    if snowflake_symbol_dict.get(flake) != None:

                        im = plt.imread(path2snowflake + snowflake_symbol_dict.get(flake))
                        im[im == 0] = np.nan
                        imagebox = OffsetImage(im, zoom=.01)
                        if (self.layers_grainType2[i] is None) and (self.layers_grainType3[i] is None):
                            hloc = 0.5
                        elif (self.layers_grainType2[i] != None) and (self.layers_grainType3[i] is None):
                            hloc = 0.33
                        else:
                            hloc = 0.25

                        xy = [hloc,
                              ((self.layers_top[i] - self.layers_bot[i]) / 2 + self.layers_bot[i])]  # coordinates to position this image
                        ab = AnnotationBbox(imagebox, xy, xycoords='data', boxcoords='data', frameon=False)
                        ax.add_artist(ab)
                    else:
                        print('WARNING: [' + flake + '] is not a compatible snowflake type. Check spelling!')

            for i, flake in enumerate(self.layers_grainType2.astype(str)):
                if flake == 'nan':
                    flake = None
                if flake is not None:
                    if snowflake_symbol_dict.get(flake) != None:
                        im = plt.imread(path2snowflake + snowflake_symbol_dict.get(flake))
                        im[im == 0] = np.nan
                        imagebox = OffsetImage(im, zoom=.01)
                        if (self.layers_grainType2[i] != None) and (self.layers_grainType3[i] is None):
                            hloc2 = 0.66
                        else:
                            hloc2 = 0.5
                        xy = [hloc2,
                              ((self.layers_top[i] - self.layers_bot[i]) / 2 + self.layers_bot[i])]  # coordinates to position this image
                        ab = AnnotationBbox(imagebox, xy, xycoords='data', boxcoords='data', frameon=False)
                        ax.add_artist(ab)
                    else:
                        print('WARNING: [' + flake + '] is not a compatible snowflake type. Check spelling!')

            for i, flake in enumerate(self.layers_grainType3.astype(str)):
                if flake == 'nan':
                    flake = None
                if flake != None:
                    if snowflake_symbol_dict.get(flake) != None:
                        im = plt.imread(path2snowflake + snowflake_symbol_dict.get(flake))
                        im[im == 0] = np.nan
                        imagebox = OffsetImage(im, zoom=.01)
                        xy = [0.75,
                              ((self.layers_top[i] - self.layers_bot[i]) / 2 + self.layers_bot[i])]  # coordinates to position this image
                        ab = AnnotationBbox(imagebox, xy, xycoords='data', boxcoords='data', frameon=False)
                        ax.add_artist(ab)
                    else:
                        print('WARNING: [' + flake + '] is not a compatible snowflake type. Check spelling!')

            ax.set_title("Stratigraphy")
            return im2

        def plot_hardness(ax):
            plt.setp(ax.get_yticklabels(), visible=False)

            # Add grid following the layering
            im = ax.barh(self.layers_bot - (self.layers_bot - self.layers_top) / 2, self.layers_hardness_index,
                         self.layers_bot - self.layers_top, color=cm.Blues(self.layers_hardness_index / 6), edgecolor='k',
                         linewidth=0.5)

            ax.set_xlim(0, 7)
            ax.set_title("Hardness")
            labels_ax = ['', 'Fist', '4F', '1F', 'P', 'K', 'I']
            ax.set_xticklabels(labels_ax, rotation=45)
            ax.xaxis.set_major_locator(MaxNLocator(integer=True, prune='upper'))
            return im

        def plot_crystalSize(ax):
            if ax is ax1:
                ax.set_ylabel("Depth (cm)")
            else:
                plt.setp(ax.get_yticklabels(), visible=False)
                ax.yaxis.tick_right()
            im = ax.barh(self.layers_bot-(self.layers_bot-self.layers_top)/2, self.layers_grainSize_max-self.layers_grainSize_mean, 1, self.layers_grainSize_mean)
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
            metadata_text = "Date: " + p.metadata.date + '; Time [24hr]: ' + '\n' + \
                            "Observer: " + p.metadata.observer + '\n' + \
                            "Location description: " + p.metadata.location_description + '\n' + \
                            "East : " + str(p.metadata.east) + ' ' + \
                            "North: " + str(p.metadata.north) + ' ' + \
                            "Elevation: " + str(p.metadata.elevation) + ' ' + p.metadata.elevation_unit + '\n' + \
                            "Air temperature: " + str(p.metadata.air_temperature) + '$^{\circ}C$' '\n'

            plt.figtext(0.08, 0.12 , metadata_text,
                        horizontalalignment='left',
                        verticalalignment='center', wrap=True, fontsize=4)

        to_plot(plots_order, axs_list)
        if invert_depth:
            fig.gca().invert_yaxis()
        plt.tight_layout()
        plt.subplots_adjust(wspace=0)

        if save == True:
            fig.savefig(self.filename.split('/')[-1][0:-4])
            print('Figure saved as ' + self.filename.split('/')[-1][0:-4] + '.png')



    def print_metadata(self):
        print('Not implemented [print_metadata()]')

    def print_layers(self):
        print('Not implemented [print_layers()]')



#

#
