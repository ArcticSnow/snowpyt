
'''
Script to plot summary snowpit from data example of the standard snowpit format
Simon Filhol, December 2016

'''

filename = 'data_example/20161216_snowpit.csv'  #[insert path to file]

mypit = Snowpit_standard(filename)
mypit.filename = filename
mypit.load_csv()
mypit.summary_plot(save=True, metadata=True)
mypit.print_metadata()
