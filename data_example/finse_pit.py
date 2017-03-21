'''
Script to plot and analyse snowpit from Finse
'''

import pit_class as pc

# import snowpits as Snowpit class
fname_20161122	 = 'data_example/Standard_pit.csv'  #[insert path to file]
fname_20161216	 = 'data_example/20161216_snowpit.csv'  #[insert path to file]

pit1 = pc.Snowpit_standard(fname_20161122)
pit1.load_csv()
pit2 = pc.Snowpit_standard(fname_20161216)
pit2.load_csv()


