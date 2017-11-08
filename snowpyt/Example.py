
'''
Script to plot summary snowpit from data example of the standard snowpit format
Simon Filhol, December 2016

'''

from snowpyt import pit_class as pc

filename = '/home/tintino/github/snowpyt/snowpyt/data_example/20170209_Finse_snowpit.xlsx'  #[insert path to file]

pit1 = pc.Snowpit()
pit1.filename = filename
pit1.import_xlsx()
pit1.plot(metadata=True)
pit1.plot(plots_order=['density', 'temperature', 'stratigraphy','crystal size', 'sample value'])

pit1.plot(plots_order=['density', 'sample names','sample values'])



#================================================================================
#       Section for Debugging the package
#================================================================================
# Code to run my local version of the package the local
import sys
sys.path.append('/home/tintino/github/snowpyt/snowpyt/')
import pit_class as pc

p=pc.Snowpit()
p.filename='/home/tintino/github/snowpyt/snowpyt/data_example/20170209_Finse_snowpit.xlsx'  #[insert path to file]
p.import_xlsx()
p.plot(plots_order=['density', 'sample names','sample values'])
