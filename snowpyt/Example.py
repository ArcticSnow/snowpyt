
'''
Script to plot summary snowpit from data example of the standard snowpit format
Simon Filhol, December 2016

'''

import pit_class as pc

filename = 'snowpyt/data_example/20161216_snowpit.csv'  #[insert path to file]

pit1 = pc.Snowpit_standard()
pit1.filename = filename
pit1.load_csv()
pit1.summary_plot(metadata=False)



mypit = pc.Snowpit_standard(filename)
mypit.filename = filename
mypit.load_csv()
mypit.summary_plot(save=True, metadata=True)
mypit.print_metadata()

filename = 'snowpyt/data_example/20170209_Finse_snowpit.xlsx'
pit1 = Snowpit_standard()
pit1.filename = filename
pit1.load_xslx_pit()
pit1.summary_plot(metadata=False)

plt.figure()
plt.ylim([0,100])
for i, name in enumerate(pit1.sample_name.astype(str)):
    print name
    print pit1.sample_depth[i]

    if name != 'nan':
        plt.text(0.5, pit1.sample_depth[i], name)




plt.text(0, pit1.sample_depth[3], pit1.sample_name.astype(str)[3])