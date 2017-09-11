# -*- coding: utf-8 -*-
"""
Created on Tue Jul 06, 2017

@author: Simon Filhol

Collection of functions to import snowpit data stored in  xlslx file following the Snowpyt standard

"""

import pit_class as pc
import xlrd

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

def sheet_names(path_xlsx=None):
    '''
    Functiont to print and return the list of sheet included in an excel file
    :param path:
    :return:
    '''
    if path_xlsx is None:
        print 'No xlsx file indicated'
        return
    wb = xlrd.open_workbook(path_xlsx)
    print wb.sheet_names()
    return wb.sheet_names()

def get_metadata(path_xlsx, sheet=None):

    if path_xlsx[-4:] != 'xlsx':
        print 'Input file is not of .xlsx format'
        return
    wb = xlrd.open_workbook(path_xlsx)

    if sheet is None:
        sheet = wb.sheet_names()[0]
    sh = wb.sheet_by_name(sheet)

    # Load metadata:
    fields = ['East', 'Nort', 'Elev', 'Date', 'Obse', 'Loca', 'Air ', 'Weat', 'Comm', 'Snow', 'Time', 'Gene',
              'Stra']
    Metadata = pc.metadata()
    values = find_row_with_values(sh, fields)
    Metadata.date = get_cell_val_str(sh, values.get('Date'), 1)
    Metadata.time = get_cell_val_str(sh, values.get('Time'), 1)
    Metadata.observer = get_cell_val_str(sh, values.get('Obse'), 1)
    Metadata.east = get_cell_val_str(sh, values.get('East'), 1)
    Metadata.east_unit = get_cell_val_str(sh, values.get('East'), 2)
    Metadata.north = get_cell_val_str(sh, values.get('Nort'), 1)
    Metadata.north_unit = get_cell_val_str(sh, values.get('Nort'), 2)
    Metadata.elevation = get_cell_val_str(sh, values.get('Elev'), 1)
    Metadata.elevation_unit = get_cell_val_str(sh, values.get('Elev'), 2)
    Metadata.sky_conditions = get_cell_val_str(sh, values.get('Weat'), 1)
    Metadata.comments = get_cell_val_str(sh, values.get('Comm'), 1)
    Metadata.air_temperature = get_cell_val_str(sh, values.get('Air '), 1)
    Metadata.location_description = get_cell_val_str(sh, values.get('Gene'), 1)
    # possibility to add extra fields

    return Metadata


def get_layers(path_xlsx, sheet=None):

    if path_xlsx[-4:] != 'xlsx':
        print 'Input file is not of .xlsx format'
        return
    wb = xlrd.open_workbook(path_xlsx)

    if sheet is None:
        sheet = wb.sheet_names()[0]
    sh = wb.sheet_by_name(sheet)

    # Load data:
    self.profile_raw_table = pd.read_excel(path, sheet=sh, skiprows=int(values.get('Stra')) + 1, engine='xlrd')
    self.load_profile_from_raw_table()
