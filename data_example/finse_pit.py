'''
Script to plot and analyse snowpit from Finse
'''

import pit_class as pc

path = '/home/arcticsnow/Github/snowpyt/'
#path = '/Users/tintino/github/snowpyt/'

# import snowpits as Snowpit class
fname_20161122 = 'data_example/Standard_pit.csv'  #[insert path to file]
fname_20161216 = 'data_example/20161216_snowpit.csv'  #[insert path to file]

fname_20170209 = 'data_example/20170209_Finse_snowpit.csv'

pit1 = pc.Snowpit_standard()

pit1.filename = path + fname_20170209
pit1.load_csv()
pit1.sample_name
#pit1.plot_temperature()
#pit1.plot_density()
pit1.summary_plot(metadata=False)



pit2 = pc.Snowpit_standard(path + fname_20161216)
pit2.load_csv()


import matplotlib.pyplot as plt
import numpy as np

plt.figure()
plt.gca().invert_yaxis()
plt.barh(pit1.layer_top+(pit1.layer_bot - pit1.layer_top)/2, np.repeat(1, pit1.layer_top.__len__()), (pit1.layer_bot - pit1.layer_top),
                       color=plt.cm.Blues(pit1.hardness_code / 6))
plt.plot(np.vstack((np.repeat(0, pit1.layer_top.__len__()),np.repeat(1, pit1.layer_top.__len__()))),
         np.vstack((pit1.layer_top, pit1.layer_top)), linewidth=.5, linestyle='--', c='k')

