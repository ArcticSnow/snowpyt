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
        self.sample_file = None
        self.metadata = metadata()
        self.temperature_profile = temperature_profile()
        self.density_profile = density_profile()
        self.sample_profile = sample_profile()
        self.table = pd.DataFrame()
        self.layers = None
        self.units = None

        self.layers_top = None
        self.layers_bot = None

    def _extract_layers(self, print2term=True):
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
            if print2term:
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

    def import_caamlv6(self, print2term=True):
        # Load metadata
        self.metadata = cxv6.get_metadata(self.caaml_file, print2term=print2term)

        # load temperature profile
        self.temperature_profile = cxv6.get_temperature(self.caaml_file, print2term=print2term)

        # load density profile
        self.density_profile = cxv6.get_density(self.caaml_file, print2term=print2term)

        # load layers
        self.layers = cxv6.get_layers(self.caaml_file, print2term=print2term)
        if self.layers is not None:
            self._extract_layers(print2term=print2term)


    def import_sample_csv(self, bar_plot=False):
        """
        Function to import sample profiles.

        Args:
            bar_plot (bool): plot sample profile as bar instead of line-scatter. Default is False
        """
        self.sample_profile.df = pd.read_csv(self.sample_file)
#        self.sample_profile.layer_top = self.sample_profile.df.height_top
#        self.sample_profile.layer_bot = self.sample_profile.df.height_bot
        self.sample_profile.names = self.sample_profile.df.columns[2:]
        self.sample_profile.bar_plot = bar_plot   

    def plot(self,
             save=False,
             metadata=False,
             invert_depth=False,
             figsize=(8,4),
             dpi=150,
             plot_order=['temperature', 'density', 'crystal size',
                         'stratigraphy', 'hardness', 'sample names',
                         'dD', 'd18O', 'dxs']):
        """
        Function to plot pit data
        Args:
            save (bool): save plot
            metadata (bool): add metadata to plot
            invert_depth (bool): invert depth/height axis. Default is height
            figsize (tuple): size of plot in inch. default matplotlib setting
            dpi (int): plot resolution, pixel per inches
            plot_order (list): list of plots to add to the figure, the order defines the order of the plots
        """
        fig = plt.figure(figsize=figsize, dpi=dpi)

        if metadata:
            my_rowspan = 3
        else:
            my_rowspan = 4

        # ===========================================================
        # Automatically adjust summary plot based on data available
        ncol = plot_order.__len__()

        if ncol == 1:
            ax1 = plt.subplot2grid((4, ncol), (0, ncol - 1), rowspan=my_rowspan)
            self.axs_list = [ax1]

        if ncol >= 2:
            ax1 = plt.subplot2grid((4, ncol), (0, 0), rowspan=my_rowspan)
            self.axs_list = []
            self.axs_list.append(ax1)
            for n in range(1, ncol):
                ax = plt.subplot2grid((4, ncol), (0, n), rowspan=my_rowspan, sharey=ax1)
                self.axs_list.append(ax)
            print(self.axs_list)

        def to_plot(plot_order=plot_order):
            # function to plot plots based on the order indicated in plot_order
            plots_dict = {'temperature': plot_temperature,
                          'density': plot_density,
                          'stratigraphy': plot_stratigraphy,
                          'hardness': plot_hardness,
                          'crystal size': plot_crystalSize,
                          'sample_name': plot_sample_names,
                          'dD': plot_dD,
                          'd18O': plot_d18O,
                          'dxs': plot_dxs}
            # include a little logic to check that iso is properly define
            for var in plot_order:
                if var not in ['temperature', 
                               'density', 
                               'stratigraphy', 
                               'hardness', 
                               'crystal_size', 
                               'sample_name',
                               'dD', 
                               'd18O', 
                               'dxs']:
                    print('\nERROR: plot_order only accepts: temperature, density, stratigraphy, hardness, crystal_size, sample_name, dD, d18O, dxs')
                    return
            for i, axs in enumerate(self.axs_list):
                plots_dict.get(plot_order[i])(axs)


        def add_grid(ax):
            xlim = ax.get_xlim() 
            ax.barh(self.layers_bot - (self.layers_bot - self.layers_top) / 2,
                    np.repeat(xlim[1] - xlim[0], self.layers_top.__len__()), - (self.layers_bot - self.layers_top),
                    np.repeat(xlim[0], self.layers_top.__len__()), 
                    alpha=0.5, edgecolor='m', linewidth=0.75, linestyle=':',zorder=20,fill=False)

        def plot_isotope(ax, iso='dD', std=None):
            if std is None:
                std = iso + '_SD'  #std column name default for data from FARLAB
            
                
            if ax is ax1:
                ax.set_ylabel("Depth (cm)")
            else:
                plt.setp(ax.get_yticklabels(), visible=False)
                ax.yaxis.tick_right()
                
            color_dict = {'dD': '#1f77b4',
                          'd18O': '#1f77b4','dxs':'#d62728'}
            title_dict = {'dD': "dD ($^{o}/_{oo}$)", 
                          'd18O': "d18O ($^{o}/_{oo}$)",
                          'dxs': "d-excess ($^{o}/_{oo}$)"}
            
            color=color_dict[iso]
            
            #sample-type layer color in gray scale
            col_vec=[]
            hatch_vec=[]
            symb_vec=[]
            cat=self.sample_profile.df.ice_type
            for let in cat:
                if let=='S':
                    col_vec=np.append(col_vec,'None')
                    hatch_vec=np.append(hatch_vec,'')
                    symb_vec=np.append(symb_vec,'o')
                if let=='I':
                    col_vec=np.append(col_vec,'0.7')
                    hatch_vec=np.append(hatch_vec,'.')
                    symb_vec=np.append(symb_vec,'sq')
                if let=='M':
                    col_vec=np.append(col_vec,'0.9')
                    hatch_vec=np.append(hatch_vec,'\\')
                    symb_vec=np.append(symb_vec,'d')

            #staircase step plot:
            im = ax.step(np.append(self.sample_profile.df[iso].values[0], self.sample_profile.df[iso].values),
                         np.append(self.sample_profile.df.height_top.values,0), where='post', color=color)
            #ax.set_title("dD ($^{o}/_{oo}$)")
            xlim = ax.get_xlim()    
            
            # Mika: add error-bar in isotope
            ax.barh(
                self.sample_profile.df.height_top,2*self.sample_profile.df[std].values,
                (self.sample_profile.df.height_bot-self.sample_profile.df.height_top),
                (self.sample_profile.df[iso].values-self.sample_profile.df[std].values),
                align='edge',edgecolor='k',linewidth=0,color=color,alpha=0.6,zorder=5)
            
            # Mika: add isotope-sample-layer type - this needs the col_vec.
            ax.barh(
                self.sample_profile.df.height_top,np.diff(xlim),
                (self.sample_profile.df.height_bot-self.sample_profile.df.height_top),xlim[0],
                align='edge',edgecolor='k',color=col_vec,linewidth=0,zorder=2)

            # Add grid following the layering
            add_grid(ax)
#            ax.barh(self.layers_bot - (self.layers_bot - self.layers_top) / 2,
#                    np.repeat(xlim[1] - xlim[0], self.layers_top.__len__()), - (self.layers_bot - self.layers_top),
#                    np.repeat(xlim[0], self.layers_top.__len__()), 
#                    alpha=0.5, edgecolor='m', linewidth=0.75, linestyle=':',zorder=20,fill=False)
            
            ax.set_title(title_dict[iso])
            ax.set_xlim(xlim)
            ax.grid(axis='x', linewidth=0.5, linestyle=':')
            for tick in ax.get_xticklabels():
                tick.set_rotation(45)

            return im

        def plot_dD(ax):
            plot_isotope(ax,iso='dD')

        def plot_d18O(ax):
            plot_isotope(ax,iso='d18O')

        def plot_dxs(ax):
             plot_isotope(ax,iso='dxs')
            
        def plot_density(ax):
            if ax is ax1:
                ax.set_ylabel("Depth (cm)")
            else:
                plt.setp(ax.get_yticklabels(), visible=False)
                ax.yaxis.tick_right()
            im = ax.plot(self.density_profile.density, self.density_profile.depth)
            xlim = ax.get_xlim()

            # Add grid following the layering
            add_grid(ax)
#            ax.barh(self.layers_bot - (self.layers_bot - self.layers_top) / 2,
#                    np.repeat(xlim[1] - xlim[0], self.layers_top.__len__()), - (self.layers_bot - self.layers_top),
#                    np.repeat(xlim[0], self.layers_top.__len__()),
#                    color='w', alpha=0.5, edgecolor='m', linewidth=0.75, linestyle=':')
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
            add_grid(ax)
#            ax.barh(self.layers_bot - (self.layers_bot - self.layers_top) / 2,
#                     np.repeat(xlim[1] - xlim[0], self.layers_top.__len__()), - (self.layers_bot - self.layers_top),
#                     np.repeat(xlim[0], self.layers_top.__len__()),
#                     color='w', alpha=0.5, edgecolor='m', linewidth=0.75, linestyle=':')
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
            add_grid(ax)
#            ax.barh(self.layers_bot - (self.layers_bot - self.layers_top) / 2,
#                    np.repeat(xlim[1] - xlim[0], self.layers_top.__len__()), - (self.layers_bot - self.layers_top),
#                    np.repeat(xlim[0], self.layers_top.__len__()),
#                    color='w', alpha=0.2, edgecolor='k', linewidth=0.5, linestyle=':')
            ax.xaxis.set_ticks([0, 0.1, 0.2, 0.5, 1, 1.5, 2, 3, 4, 5, 10, 15, 20, 25, 30, 35, 40])
            ax.set_xlim(xlim)
            ax.set_title("Crystal size (mm)")
            ax.grid(axis='x', linewidth=0.5, linestyle=':')

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
            add_grid(ax)
#            ax.barh(self.layers_bot - (self.layers_bot - self.layers_top) / 2,
#                    np.repeat(xlim[1] - xlim[0], self.layers_top.__len__()), - (self.layers_bot - self.layers_top),
#                    np.repeat(xlim[0], self.layers_top.__len__()),
#                    color='w', alpha=0.2, edgecolor='k', linewidth=0.5, linestyle=':')
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

        to_plot(plot_order)
        if invert_depth:
            fig.gca().invert_yaxis()
        plt.tight_layout()
        plt.subplots_adjust(wspace=0)

        if save == True:
            fig.savefig(fig_fname)
            print('Figure saved as ' + fig_fname)


    def print_metadata(self):
        print('Not implemented [print_metadata()]')

    def print_layers(self):
        print('Not implemented [print_layers()]')
        
    
    def calc_SWE(self, method='avg', ice_layer_density=680):
        """
        Functino to compute SWE using three methods: avg SWE for all pit 'avg', SWE based on density samples 'samples', and SWE based
        Args:
            method (str): 'avg', 'samples' or 'layers'. no default
                        - 'avg' is simply the
                        - 'samples' is density by density samples. Top and bottom layer from all top to all bottom
                        to half between density sample 1;2 and N-1;N. All others, make layer horizons between samples,
                        use density sample in middle of these layers as density
                        - 'layers' is density by strat-layer, find matching density sample.Ice layer density a given
                        density.if more than one match, use average. if no matches, search for neareast. (or search for nearest two, upper and lower, and make average)
            ice_layer_density (int): assign a constant density to ice layers (An ice layer is detected when hand hardness index = knife = 6)

        Returns:
            float: SWE in [cm]
        """
        if method == 'avg':
            SWE=(self.density_profile.density.mean()*self.layers_top[0])/1000
            
        if method == 'samples':
            if self.layers is not None:
                #make layer boundaries, horizons, at half-points between density samples
                #make into pandas to use rolling mean, make back into numpy array
                self.density_profile.layer_horz = pd.DataFrame(self.density_profile.depth).rolling(2,min_periods=2).mean().to_numpy()
                #override first value of rolling mean, nan, with top max height of snowpit
                self.density_profile.layer_horz[0] = self.layers_top[0]
                #app bottom of snowpit, yes 0
                self.density_profile.layer_horz = np.append(self.density_profile.layer_horz,self.layers_bot[-1])
                #calculate thicknsesses:
                self.density_profile.layer_thickness = abs(np.diff(self.density_profile.layer_horz))
               
                SWE=(self.density_profile.layer_thickness*self.density_profile.density / 1000).sum()
            else:
                print('No layers: choose another method')
                return
       
        if method == 'layers':
            """
            Correction to do: If the first density sample is below the bottom of the second layer then it fails
            one logic could be: take height of upper density. Assign this density to any layer above unless flagged as ice. Do the opposite for bootom layers
10:30
then assign density o layers which have a density sample within their height range
10:30
and finally do interpolation for the one having no value after this
            """

            if self.layers is not None:

                def nearest(direction, lookin, lookfor):
                    if direction == 'up':
                        idx = np.where(lookin > lookfor)[0][-1]
                    elif direction == 'down':
                        idx = np.where(lookin < lookfor)[0][0]
                    else:
                        print('ERROR: You must provide a direction, up or down')
                    return idx
                
                
                #get thickness or our strat-layers:        
                self.layers_thickness = self.layers_top-self.layers_bot

                #initialize numpy array for our strat-densities, length of the strat-layers
                self.layers_density = np.zeros(len(self.layers_top))

                #get the density of strat-layers, with different conditions
                for i in range(len(self.layers_top)):
                    
                    #if ice layer, set arbitrary density:
                    if self.layers_hardness_index[i] == 6:
                        self.layers_density[i] = ice_layer_density

                    #if not ice, check if there are NO density samples within the strat-layer:    
                    elif np.sum((self.density_profile.depth > self.layers_bot[i]) & (self.density_profile.depth < self.layers_top[i])) == 0:
                        #if yes:
                        #take care of first layer, bottom layer, since they both have only one of idxlower/idxupper
                        if i == 0:
                            self.layers_density[i] = self.density_profile.density[nearest('down',self.density_profile.depth,self.layers_bot[i])]
                
                        elif i == len(self.layers_top)-1:
                            self.layers_density[i]=self.density_profile.density[nearest('up',self.density_profile.depth,self.layers_top[i])]
            
                        #for all other layers, look both up and down:    
                        else:
                            print(i)
                            idxupper = nearest('up',self.density_profile.depth,self.layers_top[i])
                            idxlower = nearest('down',self.density_profile.depth,self.layers_top[i])
                            self.layers_density[i] = self.density_profile.density[idxupper:idxlower+1].mean()
                
                    #if there ARE samples within the layer, take mean of those samples:    
                    else:
                        self.layers_density[i]=self.density_profile.density[(self.density_profile.depth >= self.layers_bot[i]) & (self.density_profile.depth <= self.layers_top[i])].mean()
            
            
                SWE = (self.layers_thickness * self.layers_density / 1000).sum()
            else:
                print('No layers: choose another method')
                return
            
        return SWE
        print(SWE)

