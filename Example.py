
# testing TO BE DELETED
import platform

if platform.system()=='Linux':
    filename = '/home/arcticsnow/github/snowpyt/data_example/htd_6.csv'
elif platform.system() == 'Darwin':
    filename = '/Users/tintino/Desktop/kbv2_3.txt'


a = Snowpit_svalbard_JC(filename)
a.filename = filename
a.load_csv()
a.summary_plot(save=False)

####################################################
# Plotting tool in development

fig = plt.figure(figsize=(10,10),dpi=150)
#fig = plt.figure()
ax1 = fig.add_subplot(1, 4, 1)
ax2 = fig.add_subplot(1, 4, 2, sharey=ax1)  # Share y-axes with subplot 1
ax3 = fig.add_subplot(1, 4, 3, sharey=ax2)
ax4 = fig.add_subplot(1, 4, 4, sharey=ax3)

# Set y-ticks of subplot 2 invisible
plt.setp(ax2.get_yticklabels(), visible=False)
plt.setp(ax2.get_xticklabels(), visible=False)
plt.setp(ax3.get_yticklabels(), visible=False)
plt.setp(ax4.get_yticklabels(), visible=False)

# Plot data
fig.gca().invert_yaxis()
im1 = ax1.plot(-a.snow_temperature, a.depth_temperature)

im2 = ax2.barh(a.layer_top, np.repeat(1,a.layer_top.__len__()), a.layer_bot-a.layer_top, color = cm.Blues(a.hardness_code/6))
ax2.set_xlim(0,1)

# include symbols

for i, flake in enumerate(a.grain_type1.astype(str)):
    if flake != 'nan':
        im = plt.imread(snowflake_dict.get(flake))
        im[im==0]=np.nan
        imagebox = OffsetImage(im, zoom=.02)
        if a.grain_type2.astype(str)[i]=='nan':
            hloc = 0.5
        else:
            hloc = 0.33
        xy = [hloc, ((a.layer_top[i]-a.layer_bot[i])/2+a.layer_bot[i])]               # coordinates to position this image
        ab = AnnotationBbox(imagebox, xy, xycoords='data', boxcoords='data',frameon=False)
        ax2.add_artist(ab)

for i, flake in enumerate(a.grain_type2.astype(str)):
    if flake != 'nan':
        im = plt.imread(snowflake_dict.get(flake))
        im[im==0]=np.nan
        imagebox = OffsetImage(im, zoom=.02)
        xy = [0.66, ((a.layer_top[i]-a.layer_bot[i])/2+a.layer_bot[i])]               # coordinates to position this image
        ab = AnnotationBbox(imagebox, xy, xycoords='data', boxcoords='data',frameon=False)
        ax2.add_artist(ab)

im3 = ax3.barh(a.layer_top, a.hardness_code, a.layer_bot-a.layer_top, color = cm.Blues(a.hardness_code/6))
ax3.set_xlim(0,7)

im4 = ax4.plot(a.density, a.depth_density)
ax4.yaxis.tick_right()

# add
ax1.set_title("Temperature ($^\circ$C)")
ax2.set_title("Stratigraphy")
ax3.set_title("Hardness")
ax4.set_title("Density")
ax1.set_ylabel("Depth (cm)")

ax1.grid()
ax4.grid()

# addind metadata information on layout:
metadata='Date: ' + self. + '\n'
plt.text(2,2,metadata)


fig.suptitle(metadata)
fig.autofmt_xdate()
# finalize and save as an image
plt.tight_layout()
plt.subplots_adjust(wspace=0)
fig.savefig('test.png')







f=open(filename)
for i, line in enumerate(f):
    if line[0:4] == 'Date':
        print line.split("\t")[1]
        print line.split("\t")[5]
    if line[0:4] == 'Time':
        print line.split("\t")[5]
    if line[0:4] == 'Area':
        print line.split()[6]
    if line[0:4] == 'Obse':
        print line.split("\t")
    if line[0:4] == 'Air ':
        print line.split("\t")[2]
    if line[0:4] == 'Glac':
        print line.split("\t")[1]
    if line[0:4] == 'Glac':
        print line.split("\t")[4]
    if line[0:4] == 'Gene':
        print line.split("\t")[1]


        self.North = split_f[20]
        self.Elevation = split_f[47]
        self.Observer = split_f[57]
        self.AirTemp = split_f[128]
        self.glacier = split_f[1]
        self.weather_conditions = split_f[4]
        self.comments = split_f[71] + "\n" + split_f[85]




