
'''
Script to plot summary snowpit from data example of the standard snowpit format
Simon Filhol, December 2016

'''

from snowpyt import pit_class as pc

filename = '/home/arcticsnow/github/snowpyt/snowpyt/data_example/20170209_Finse_snowpit.xlsx'  #[insert path to file]

pit1 = Snowpit()
pit1.filename = filename
pit1.import_xlsx()

pit1.plot(metadata=True)
pit1.plot(plots_order=['density', 'temperature', 'stratigraphy','crystal size'])




