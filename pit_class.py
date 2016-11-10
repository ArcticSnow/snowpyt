#!/usr/bin/python

'''
File defining a python class for snowpit data

November 2016, Simon Filhol
'''

import numpy as np
import pandas as pd

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

    def load_csv(self):

        load_metadata()
        load_profile()

    def load_profile(self):
        self.profile_raw_table = pd.read_csv(self.filename, sep='\t', skiprows=14)
        self.layerID = np.int(profile_raw_table.ix[:,0])
        self.layer_top = profile_raw_table.ix[:,1]
        self.layer_bot = profile_raw_table.ix[:, 2]

        self.grain_type1 = profile_raw_table.ix[:,3]
        self.grain_type2 = profile_raw_table.ix[:, 4]
        self.grain_size_min = profile_raw_table.ix[:, 5]
        self.grain_size_max = profile_raw_table.ix[:, 6]

        self.hardness = profile_raw_table.ix[:, 7]
        self.hardness_code = profile_raw_table.ix[:, 8]

        self.depth_density = profile_raw_table.ix[:, 10]
        self.density = profile_raw_table.ix[:, 11]

        self.depth_temperature = profile_raw_table.ix[:,14]
        self.snow_temperature = profile_raw_table.ix[:, 15]


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
        self.comments = split_f[71]
        f.close()

    def print_metadata(self):
        print "Date: " + self.date
        print "East [deg]: " + self.East
        print "North [deg]: " + self.North
        print "Elevation [m]: " + self.Elevation
        print "Obsever: " + self.Observer
        print "Air temperature [C]: " + self.AirTemp
        print "Glacier: " + self.glacier
        print "Weather conditions: " + self.weather_conditions
        print "Comments: " + self.comments


# testing
filename = '/Users/tintino/Desktop/kbv2_6.txt'

profile = np.genfromtxt(filename, delimiter= '\t', skip_header=15)
profile = pd.read_csv(filename, sep='\t', skiprows=14)


f = open(filename)


























