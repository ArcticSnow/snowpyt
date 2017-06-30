#!/usr/bin/python

'''
File defining a python class for snowpit data

November 2016, Simon Filhol
'''
from __future__ import division
import pickle
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.cm as cm
from matplotlib.offsetbox import AnnotationBbox, OffsetImage
from matplotlib._png import read_png
from matplotlib.ticker import MaxNLocator
import xlrd

snowflake_dict = {'faceted':'snowpyt/snowflake/faceted.png',
                  'wind packed':'snowpyt/snowflake/wind_packed.png',
                  'wind slab':'snowpyt/snowflake/wind_packed.png',
                  'windslab':'snowpyt/snowflake/wind_packed.png',
                  'horizontal ice layer':'snowpyt/snowflake/ice.png',
                  'ice layer':'snowpyt/snowflake/ice.png',
                  'clustered rounded':'snowpyt/snowflake/cluster_rounded.png',
                  'cluster rounded':'snowpyt/snowflake/cluster_rounded.png',
                  'wind broken':'snowpyt/snowflake/wind_broken_precip.png',
                  'rounded':'snowpyt/snowflake/large_rounded.png',
                  'faceted and rounded':'snowpyt/snowflake/faceted_rounded.png',
                  'faceted rounded':'snowpyt/snowflake/faceted_rounded.png',
                  'rounded and faceted':'snowpyt/snowflake/rounding_faceted.png',
                  'rounded faceted':'snowpyt/snowflake/rounding_faceted.png',
                  'depth hoar':'snowpyt/snowflake/hollow_cups.png',
                  'hollow cups':'snowpyt/snowflake/hollow_cups.png',
                  'hollow prism':'snowpyt/snowflake/hollow_prism.png',
                  'melt refreeze':'snowpyt/snowflake/melt_freeze_crust.png',
                  'melt refreeze crust':'snowpyt/snowflake/melt_freeze_crust.png',
                  'partly decomposed': 'snowflake/partly_decomposed.png',
                  'recent snow':'snowpyt/snowflake/recent_snow.png',
                  'ice column':'snowpyt/snowflake/ice_column.png',
                  'percolation column':'snowpyt/snowflake/ice_column.png',
                  'percolation':'snowpyt/snowflake/ice_column.png',
                  'rounding depth hoar':'snowpyt/snowflake/rounding_depth_hoar.png',
                  'cavity crevasse hoar':'snowpyt/snowflake/cavity_crevasse_hoar.png',
                  'rounding surface hoar':'snowpyt/snowflake/rounding_surface_hoar.png',
                  'basal ice':'snowpyt/snowflake/basal_ice.png',
                  'rain crust':'snowpyt/snowflake/rain_crust.png',
                  'sun crust':'snowpyt/snowflake/sun_crust.png',
                  'surface hoar':'snowpyt/snowflake/surface_hoar.png',
                  'hoar frost':'snowpyt/snowflake/surface_hoar.png',
                  'rounded polycrystals':'snowpyt/snowflake/rounded_polycrystals.png',

                  'slush':'snowpyt/snowflake/slush.png',
                  'chains of depth hoar':'snowpyt/snowflake/chains_of_depth_hoar.png',
                  'near surface faceted':'snowpyt/snowflake/near_surface_faceted.png'}

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

    def summary_plot(self, save=False, metadata=True, plot_all=False,
                     plots_order=['temperature', 'density', 'crystal size', 'stratigraphy', 'hardness', 'sample names']):
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

        # ===========================================================
        # Automatically adjust summary plot based on data available
        ncol = plots_order.__len__()

        if ncol == 1:
            ax1 = plt.subplot2grid((4, ncol), (0, ncol-1), rowspan=my_rowspan)
            axs_list = [ax1]

        if ncol == 2:
            ax1 = plt.subplot2grid((4, ncol), (0, ncol-2), rowspan=my_rowspan)
            ax2 = plt.subplot2grid((4, ncol), (0, ncol-1), rowspan=my_rowspan, sharey=ax1)
            axs_list = [ax1, ax2]

        if ncol == 3:
            ax1 = plt.subplot2grid((4, ncol), (0, ncol-3), rowspan=my_rowspan)
            ax2 = plt.subplot2grid((4, ncol), (0, ncol-2), rowspan=my_rowspan, sharey=ax1)
            ax3 = plt.subplot2grid((4, ncol), (0, ncol-1), rowspan=my_rowspan, sharey=ax1)
            axs_list = [ax1, ax2, ax3]

        if ncol == 4:
            ax1 = plt.subplot2grid((4, ncol), (0, ncol-4), rowspan=my_rowspan)
            ax2 = plt.subplot2grid((4, ncol), (0, ncol-3), rowspan=my_rowspan, sharey=ax1)
            ax3 = plt.subplot2grid((4, ncol), (0, ncol-2), rowspan=my_rowspan, sharey=ax1)
            ax4 = plt.subplot2grid((4, ncol), (0, ncol-1), rowspan=my_rowspan, sharey=ax1)
            axs_list = [ax1, ax2, ax3, ax4]

        if ncol == 5:
            ax1 = plt.subplot2grid((4, ncol), (0, ncol-5), rowspan=my_rowspan)
            ax2 = plt.subplot2grid((4, ncol), (0, ncol-4), rowspan=my_rowspan, sharey=ax1)
            ax3 = plt.subplot2grid((4, ncol), (0, ncol-3), rowspan=my_rowspan, sharey=ax1)
            ax4 = plt.subplot2grid((4, ncol), (0, ncol-2), rowspan=my_rowspan, sharey=ax1)
            ax5 = plt.subplot2grid((4, ncol), (0, ncol-1), rowspan=my_rowspan, sharey=ax1)
            axs_list = [ax1, ax2, ax3, ax4, ax5]

        if ncol == 6:
            ax1 = plt.subplot2grid((4, ncol), (0, ncol-6), rowspan=my_rowspan)
            ax2 = plt.subplot2grid((4, ncol), (0, ncol-5), rowspan=my_rowspan, sharey=ax1)
            ax3 = plt.subplot2grid((4, ncol), (0, ncol-4), rowspan=my_rowspan, sharey=ax1)
            ax4 = plt.subplot2grid((4, ncol), (0, ncol-3), rowspan=my_rowspan, sharey=ax1)
            ax5 = plt.subplot2grid((4, ncol), (0, ncol-2), rowspan=my_rowspan, sharey=ax1)
            ax6 = plt.subplot2grid((4, ncol), (0, ncol-1), rowspan=my_rowspan, sharey=ax1)
            axs_list = [ax1, ax2, ax3, ax4, ax5, ax6]

        def to_plot(plot_order=plots_order, axis_list=axs_list):
            # function to plot plots based on the order indicated in plots_order
            plots_dict = {'temperature':plot_temperature,
                            'density':plot_density,
                            'stratigraphy':plot_stratigraphy,
                            'hardness':plot_hardness,
                            'crystal size':plot_crystalSize,
                            'sample names':plot_sample_names}
            for i, axs in enumerate(axis_list):
                plots_dict.get(plot_order[i])(axs)

        def plot_density(ax):
            if ax is ax1:
                ax.set_ylabel("Depth (cm)")
            else:
                plt.setp(ax.get_yticklabels(), visible=False)
                ax.yaxis.tick_right()
            im = ax.plot(self.density, self.density_depth)
            xlim = ax.get_xlim()
            ax.barh(self.layer_bot - (self.layer_bot - self.layer_top) / 2,
                    np.repeat(xlim[1]-xlim[0], self.layer_top.__len__()), - (self.layer_bot - self.layer_top),
                    np.repeat(xlim[0], self.layer_top.__len__()),
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

            im = ax.plot(self.temperature_snow, self.temperature_depth)
            xlim = ax.get_xlim()
            ax.barh(self.layer_bot - (self.layer_bot - self.layer_top) / 2,
                    np.repeat(xlim[1] - xlim[0], self.layer_top.__len__()), - (self.layer_bot - self.layer_top),
                    np.repeat(xlim[0], self.layer_top.__len__()),
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

            im2 = ax.barh(self.layer_bot-(self.layer_bot-self.layer_top)/2, np.repeat(1, self.layer_top.__len__()), - (self.layer_bot - self.layer_top),
                       color=cm.Blues(self.hardness_code / 7), edgecolor='k', linewidth=0.5)
            ax.set_xlim(0, 1)

            # include sample name on pit face
            # for i, sample in enumerate(self.sample_name):


            # include snowflake symbols
            for i, flake in enumerate(self.grain_type1.astype(str)):
                if flake != 'nan':
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
            if ax is ax1:
                ax.set_ylabel("Depth (cm)")
            else:
                plt.setp(ax.get_yticklabels(), visible=False)
                ax.yaxis.tick_right()
            im = ax.barh(self.layer_bot-(self.layer_bot-self.layer_top)/2, self.grain_size_max-self.grain_size_min, 1, self.grain_size_min)
            xlim = ax.get_xlim()
            ax.barh(self.layer_bot - (self.layer_bot - self.layer_top) / 2,
                    np.repeat(xlim[1] - xlim[0], self.layer_top.__len__()), - (self.layer_bot - self.layer_top),
                    np.repeat(xlim[0], self.layer_top.__len__()),
                    color='w', alpha=0.2, edgecolor='k', linewidth=0.5, linestyle=':')
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
            for i, name in enumerate(self.sample_name.astype(str)):
                if name != 'nan':
                    ax.text(0.5, self.sample_depth[i], name,
                            bbox={'facecolor':'red', 'edgecolor':'none', 'alpha':0.5, 'pad':1},fontsize=5)

            xlim = ax.get_xlim()
            ax.barh(self.layer_bot - (self.layer_bot - self.layer_top) / 2,
                    np.repeat(xlim[1] - xlim[0], self.layer_top.__len__()), - (self.layer_bot - self.layer_top),
                    np.repeat(xlim[0], self.layer_top.__len__()),
                    color='w', alpha=0.2, edgecolor='k', linewidth=0.5, linestyle=':')
            ax.set_xlim(xlim)
            ax.set_title("Samples")
            plt.setp(ax.get_xticklabels(), visible=False)

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

        to_plot(plots_order, axs_list)
        fig.gca().invert_yaxis()
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

        if self.filename[-3:] != 'csv':
            print 'Input file is not of .csv file format.'
            return

        self.load_metadata()
        self.load_profile()

    def load_profile_from_raw_table(self):
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

    def load_profile(self):
        f = open(self.filename)
        for k,line in enumerate(f):
            if line[0:12] == 'Stratigraphy':
                break
        f.close()

        self.profile_raw_table = pd.read_csv(self.filename, sep='\t', skiprows=k+1)
        self.load_profile_from_raw_table()

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

    def load_xslx_pit(self, path=None, sheet=None):
        '''
        Fucntion to load pit directly from a sheet of a xlsx file
        :param path: path to the file
        :param sheet: indicate the name of the sheet to load
        :return:
        '''

        def find_row_with_values(sh, val):
            '''
            Function to find cell location of particular values indicated by a field
            :param sh: excel sheet (open with xlrd library)
            :param val: values of the fields (the first 4 character for each field) in a list format
            :return: return a dictionnary of the row where the value wanted is
            '''

            rows = []
            values = []
            for row_index in xrange(sh.nrows):
                for value in val:
                    if value == (str(sh.row(row_index)[0].value)[:4]):
                        rows.append(row_index)
                        values.append(value)
            return dict(zip(values, rows))

        def get_cell_val_str(sh, cRrow, cCol):
            '''
            Function to grab cell value as str
            :param sh:
            :param cRrow:
            :param cCol:
            :return:
            '''
            value = sh.cell(cRrow, cCol)
            #if value.value.__len__() == 0:
                #value.value = np.nan
            return str(value.value)

        if path is None:
            path = self.filename

            if path[-4:] != 'xlsx':
                print 'Input file is not of .xlsx format'
                return

        wb = xlrd.open_workbook(path)
        if sheet is None:
            sheet = wb.sheet_names()[0]
        sh = wb.sheet_by_name(sheet)

        # Load metadata:
        fields = ['East', 'Nort', 'Elev', 'Date', 'Obse', 'Loca', 'Air ', 'Weat', 'Comm', 'Snow', 'Time', 'Gene',
                  'Stra']
        values = find_row_with_values(sh, fields)
        self.date = get_cell_val_str(sh, values.get('Date'), 1)
        self.Time = get_cell_val_str(sh, values.get('Time'), 1)
        self.General_loc = get_cell_val_str(sh, values.get('Gene'), 1)
        self.East = get_cell_val_str(sh, values.get('East'), 1)
        self.East_unit = get_cell_val_str(sh, values.get('East'), 2)
        self.North = get_cell_val_str(sh, values.get('Nort'), 1)
        self.North_unit = get_cell_val_str(sh, values.get('Nort'), 2)
        self.Elevation = get_cell_val_str(sh, values.get('Elev'), 1)
        self.Elevation_unit = get_cell_val_str(sh, values.get('Elev'), 2)
        self.Observer = get_cell_val_str(sh, values.get('Obse'), 1)
        self.AirTemp = get_cell_val_str(sh, values.get('Air '), 1)
        self.weather_conditions = get_cell_val_str(sh, values.get('Weat'), 1)
        self.comments = get_cell_val_str(sh, values.get('Comm'), 1)

        # Load data:
        self.profile_raw_table =pd.read_excel(path, sheet=sh, skiprows=int(values.get('Stra'))+1, engine='xlrd')
        self.load_profile_from_raw_table()

    def sheet_names_xlsx(self, path=None):
        '''
        Functiont to print and return the list of sheet included in an excel file
        :param path:
        :return:
        '''
        if path is None:
            path = self.filename
        wb = xlrd.open_workbook(path)
        print wb.sheet_names()
        return wb.sheet_names()

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

    def save_pickle_pit(self, path):
        # search how to save a python class to pickle
        with open(path, 'w') as f:
            pickle.dump(self, f)

    def load_pickle_pit(self, path):
        # search how to read pickle file
        with open(path, 'r') as f:
            self.__dict__.update(pickle.load(f).__dict__)


