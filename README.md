# Snowpyt: an open-source library to visualize snowpits in Python
Simon Filhol, November 2016, copyright under the MIT license terms, see the License.txt file

LAST MODIFIED: March 2018 (or see date on github file history)

Feel free to contribute to the project!!!! Many new features can be added...

## To do:

### High Priority

- write function to save and load pit to and from pickle format (currently not working)
- make ground appear to comfirm the user that the pit reached ground. add note about ground type.

### Low priority 
- specify the figure size and adjust font size in respect
- render the medatadata text better, convert date to a readable date
- put option to adjust figure size to desired size and dpi. Return axis variable from plotting function for more advanced plotting if needed (i.e. multiple samples)
- add option to save pits in Pickle format or CSV
- add option to save figure in matplotlib format
- add option to plot when multiple sample columns are given.



## Objective
The objective of this library is to provide visualization tool for snowpit data. 
Started for the need of the Svalbard Snow Research group, this package should evolve
 to include more snowpit type and visualization scheme. 

The snow grain classification follows the guidelines provided by the UNESCO 
[International Classification for Seasonal Snow on the Ground](http://unesdoc.unesco.org/images/0018/001864/186462e.pdf) 
(Fierz et al., 2009)

Fierz, C., Amstrong, R.L., Durand, Y., Etchevers, P., Greene, E., McClung, D.M., Nishimura, K., Satyawali, P.K. and Sokratov, S.A. 2009.The International Classification for Seasonal Snow on the Ground. IHP-VII Technical Documents in 
Hydrology N°83, IACS Contribution N°1, UNESCO-IHP, Paris. 

## Installation

### Last stable version from the Pypi repository

Simply run the following in your terminal:
```bash
pip install snowpyt
```
### Last development version for contributing to the project:

Clone the github repository to a local directory using the following command in your terminal

```bash
git clone https://github.com/ArcticSnow/snowpyt.git
```
or by downloading the package

The branch 'master' consists of the latest stable version. Other develepment versions are included in other git branches.

The package contains all the functions to plot the snowpit if library requirements are met. It also contains data samples to test the library.

### requirements

Python 2.7.9 with the following libraries:
- [numpy](http://www.numpy.org/)
- [matplotlib](http://matplotlib.org/)
- [pandas](http://pandas.pydata.org/)
- xlrd
- xlm

## Use

1. There are three ways to import data into Snowpyt:

   1. digitalize your pit with https://niviz.org/ and export your pit as a CAAMLv6 (This format follows an international standard for snowpit). Them use the import_caamlv6() function.

      More information about the [CAAML format](http://caaml.org/)

   2. digitalize you snowpit using the excel file template in the [excel file example here](https://github.com/ArcticSnow/snowpyt/blob/master/snowpyt/data_example/20170209_Finse_snowpit.xlsx). Save the excel or libreoffice file in .xslx format (default Excel format).

   3. input directly data into the snowpit class object

      ​

3. Example:

```python
from snowpyt import pit_class as pc

############################################################
# Example 1 - using a caamlv6 file:

filename = '[PATH TO YOUR FILE].caaml'

p = pc.Snowpit()
p.filename=filename
p.import_caamlv6()
p.plot(plots_order=['density', 'temperature', 'stratigraphy', 'hardness'])


############################################################
# Example 2 - using an excel file:

filename = '[PATH TO YOUR FILE].xlsx'  

pit1 = pc.Snowpit()
pit1.filename = filename
pit1.import_xlsx()
pit1.plot(metadata=True)
pit1.plot(plots_order=['density', 'temperature', 'stratigraphy','crystal size', 'sample value'])
pit1.plot(plots_order=['density', 'sample names','sample values'])

```

4. All the data table are loaded as a Pandas dataframe or Numpy arrays within the snowpyt class object

Type the following in your Python console to see the loaded datatable:
```python
mypit.table

```
This allows for custom plotting using the library of your choice on top of the existing plotting function

6. Extra Sample Values

Extra column of sample values can be added to the excel file. **Column name must be unique**

The current plotting functions will not plot these extra columns, only the first one. However the values are loaded via pandas in the table as a dataframe (see 5.)




## Want to contribute?
Once you have cloned the project to your home directory, create a git branch and here you go. When your edits are stable, merge with the master branch. See this neat tutorial about git branching and merging, [here](https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging)

### List of Contributor
- Simon Filhol
- Guillaume Sutter
- [add your name]

## Example
![Example snowpit](snowpyt/Standard_pit.png)







