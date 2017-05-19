'''
Script to plot and analyse snowpit from Finse
'''

import pit_class as pc

path = '/home/arcticsnow/Github/snowpyt/'

# import snowpits as Snowpit class
fname_20161122	 = 'data_example/Standard_pit.csv'  #[insert path to file]
fname_20161216	 = 'data_example/20161216_snowpit.csv'  #[insert path to file]

pit1 = pc.Snowpit_standard( )

pit1.filename = path + fname_20161122
pit1.load_csv()
pit1.plot_temperature()
pit1.plot_density()
pit1.summary_plot()
pit2 = pc.Snowpit_standard(path + fname_20161216)
pit2.load_csv()


