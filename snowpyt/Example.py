
'''
Script to plot summary snowpit from data example of the standard snowpit format
Simon Filhol, December 2016

'''

import pit_class as pc

filename = 'data_example/20161216_snowpit.csv'  #[insert path to file]

pit1 = pc.Snowpit_standard()
pit1.filename = filename
pit1.load_csv()
pit1.summary_plot(metadata=False)



mypit = pc.Snowpit_standard(filename)
mypit.filename = filename
mypit.load_csv()
mypit.summary_plot(save=True, metadata=True)
mypit.print_metadata()
