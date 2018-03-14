# -*- coding: utf-8 -*-
"""
Created on Tue Jul 10, 2017

@author: Simon Filhol

Collection of functions to import snowpit data stored in the xlsx file format

******************
   Xlsx file must be formated following the package example
******************

"""
from __future__ import division
import sys

sys.path.append('/Users/tintino/github/snowpyt/snowpyt/')



import xlrd
import pit_class as pc
import pandas as pd

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
    # if value.value.__len__() == 0:
    # value.value = np.nan
    return str(value.value)

def open_xlsx(path_xlsx, sheetName=None):

    if path_xlsx[-4:] != 'xlsx':
            print 'Input file is not of .xlsx format'
            return

    wb = xlrd.open_workbook(path_xlsx)
    print '.xlsx file contains spreadsheets: '
    print wb.sheet_names()
    if sheetName is None:
        sheetName = wb.sheet_names()[0]
    sh = wb.sheet_by_name(sheetName)

    return sh

def get_metadata(sh):

    Metadata = pc.metadata()
    # Load metadata:
    fields = ['East', 'Nort', 'Elev', 'Date', 'Obse', 'Loca', 'Air ', 'Weat', 'Comm', 'Snow', 'Time', 'Gene',
              'Stra']
    values = find_row_with_values(sh, fields)

    Metadata.date = get_cell_val_str(sh, values.get('Date'), 1)
    Metadata.time = get_cell_val_str(sh, values.get('Time'), 1)
    Metadata.location_description = get_cell_val_str(sh, values.get('Gene'), 1)
    Metadata.east = get_cell_val_str(sh, values.get('East'), 1)
    Metadata.east_unit = get_cell_val_str(sh, values.get('East'), 2)
    Metadata.north = get_cell_val_str(sh, values.get('Nort'), 1)
    Metadata.north_unit = get_cell_val_str(sh, values.get('Nort'), 2)
    Metadata.elevation = get_cell_val_str(sh, values.get('Elev'), 1)
    Metadata.elevation_unit = get_cell_val_str(sh, values.get('Elev'), 2)
    Metadata.observer = get_cell_val_str(sh, values.get('Obse'), 1)
    Metadata.air_temperature = get_cell_val_str(sh, values.get('Air '), 1)
    Metadata.air_temperature_unit = get_cell_val_str(sh, values.get('Air '), 2)
    Metadata.sky_conditions = get_cell_val_str(sh, values.get('Weat'), 1)
    Metadata.comments = get_cell_val_str(sh, values.get('Comm'), 1)

    # Will need to add other fields (wind speed, precipitation, srsName, to be conform to CAAML terminology

    return Metadata

def get_table(sh, path_xlsx):
    values = find_row_with_values(sh, ['Stra'])

    rowtoskip = range(0, int(values.get('Stra'))+1)
    rowtoskip.append(int(values.get('Stra'))+2)
    print rowtoskip

    # read excel file to get data
    table = pd.read_excel(path_xlsx, sheetname=sh.name, skiprows=rowtoskip, engine='xlrd')

    # # read excel file to get headers
    # header = pd.read_excel(path_xlsx, sheetname=sh.name, skiprows=rowtoskip[:-1], engine='xlrd').columns
    #
    newCol = []
    for i, name in enumerate(table.columns):
        newCol += [name.replace(' ', '_').lower()]
    table.columns = newCol

    units = pd.read_excel(path_xlsx, sheet=sh.name, header=None, skiprows=int(values.get('Stra'))+2, engine='xlrd')
    units = units.loc[0]
    # return an extra dataframe containing units only
    return table, units

def get_layers(table):
    '''
    Function returning a list of all the layers of a snowpit
    :param table: dataframe returned by the function get_table()
    :return: return a list of layers
    '''
    layers = []
    for index, line in table.iterrows():
        layer = pc.layer()
        layer.id = line.layer_id
        layer.dbot = line.layer_top
        layer.dtop = line.layer_bottom
        layer.hardness = line.hardness_code
        #layer.dtop_unit = line
        layer.grain_size_max = line.diameter_min
        layer.grain_size_min = line.diameter_max
        layer.grain_type1 = line.type_1
        layer.grain_type2 = line.type_2
        layer.grain_type3 = line.type_3

        layers += [layer]
    return layers

def get_temperature(table):
    TProfile = pc.temperature_profile()

    TProfile.temp = table.temperature
    TProfile.depth = table.temp_depth

    TProfile.depth_unit = 'degC'
    TProfile.temp_unit = 'degC'

    return TProfile

def get_density(table):
    Pdensity = pc.density_profile()

    Pdensity.depth = table.density_depth
    Pdensity.density = table.density

    #Pdensity.density_unit =
    #Pdensity.depth_unit =

    return Pdensity

def get_sample(table):
    Sprofile = pc.sample_profile()

    Sprofile.depth = table.sample_depth
    Sprofile.sample_name = table.sample_name
    Sprofile.sample_value = table.sample_value

    return Sprofile

def load_xlsx(path=None, sheet=None):
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
        # if value.value.__len__() == 0:
        # value.value = np.nan
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
    self.profile_raw_table = pd.read_excel(path, sheet=sh, skiprows=int(values.get('Stra')) + 1, engine='xlrd')
    self.load_profile_from_raw_table()

def sheet_names_xlsx(path=None):
    '''
    Functiont to print and return the list of sheet included in an excel file
    :param path:
    :return:
    '''

    wb = xlrd.open_workbook(path)
    print wb.sheet_names()
    return wb.sheet_names()



