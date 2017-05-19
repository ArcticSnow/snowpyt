
'''
Script to plot summary snowpit from data example of the standard snowpit format
Simon Filhol, December 2016

'''

filename = '/home/arcticsnow/Escymo/Snowprofiles Finse/20170321_snowdrfit.csv'  #[insert path to file]

filename = '/home/arcticsnow/Github/snowpyt/data_example/Standard_pit.csv'
mypit = Snowpit_standard(filename)
mypit.filename = filename
mypit.load_csv()
mypit.summary_plot(save=True, metadata=True)
mypit.print_metadata()
