
'''
Script to plot summary snowpit from data example of the standard snowpit format
Simon Filhol, December 2016

'''

filename = 'data_example/Standard_pit.csv'  #[insert path to file]
a = Snowpit_standard(filename)
a.filename = filename
a.load_csv()
a.summary_plot(save=True)
