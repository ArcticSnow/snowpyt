<!-- markdownlint-disable -->

<a href="https://github.com/ArcticSnow/snowpyt/snowpyt/pit_class.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `snowpyt.pit_class`
File defining a python class for snowpit data 

November 2016, Simon Filhol 

**Global Variables**
---------------
- **snowflake_symbol_dict**
- **path2snowflake**


---

<a href="https://github.com/ArcticSnow/snowpyt/snowpyt/pit_class.py#L26"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `layer`




<a href="https://github.com/ArcticSnow/snowpyt/snowpyt/pit_class.py#L27"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__()
```









---

<a href="https://github.com/ArcticSnow/snowpyt/snowpyt/pit_class.py#L60"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `temperature_profile`




<a href="https://github.com/ArcticSnow/snowpyt/snowpyt/pit_class.py#L61"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__()
```









---

<a href="https://github.com/ArcticSnow/snowpyt/snowpyt/pit_class.py#L71"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `density_profile`




<a href="https://github.com/ArcticSnow/snowpyt/snowpyt/pit_class.py#L72"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__()
```









---

<a href="https://github.com/ArcticSnow/snowpyt/snowpyt/pit_class.py#L85"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `sample_profile`




<a href="https://github.com/ArcticSnow/snowpyt/snowpyt/pit_class.py#L86"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__()
```









---

<a href="https://github.com/ArcticSnow/snowpyt/snowpyt/pit_class.py#L94"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `metadata`




<a href="https://github.com/ArcticSnow/snowpyt/snowpyt/pit_class.py#L95"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__()
```









---

<a href="https://github.com/ArcticSnow/snowpyt/snowpyt/pit_class.py#L126"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Snowpit`




<a href="https://github.com/ArcticSnow/snowpyt/snowpyt/pit_class.py#L129"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__()
```








---

<a href="https://github.com/ArcticSnow/snowpyt/snowpyt/pit_class.py#L567"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `calc_SWE`

```python
calc_SWE(method='avg', ice_layer_density=680)
```

Functino to compute SWE using three methods: avg SWE for all pit 'avg', SWE based on density samples 'samples', and SWE based 

**Args:**
 
 - <b>`method`</b> (str):  'avg', 'samples' or 'layers'. no default 
                - 'avg' is simply the 
                - 'samples' is density by density samples. Top and bottom layer from all top to all bottom  to half between density sample 1;2 and N-1;N. All others, make layer horizons between samples,  use density sample in middle of these layers as density 
                - 'layers' is density by strat-layer, find matching density sample.Ice layer density a given  density.if more than one match, use average. if no matches, search for neareast. (or search for nearest two, upper and lower, and make average) 
 - <b>`ice_layer_density`</b> (int):  assign a constant density to ice layers (An ice layer is detected when hand hardness index = knife = 6) 



**Returns:**
 
 - <b>`float`</b>:  SWE in [cm] 

---

<a href="https://github.com/ArcticSnow/snowpyt/snowpyt/pit_class.py#L176"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `import_caamlv6`

```python
import_caamlv6(print2term=True)
```





---

<a href="https://github.com/ArcticSnow/snowpyt/snowpyt/pit_class.py#L192"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `import_sample_csv`

```python
import_sample_csv(bar_plot=False)
```

Function to import sample profiles. 



**Args:**
 
 - <b>`bar_plot`</b> (bool):  plot sample profile as bar instead of line-scatter. Default is False 

---

<a href="https://github.com/ArcticSnow/snowpyt/snowpyt/pit_class.py#L205"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `plot`

```python
plot(
    save=False,
    metadata=False,
    invert_depth=False,
    figsize=(8, 4),
    dpi=150,
    plot_order=['temperature', 'density', 'crystal size', 'stratigraphy', 'hardness', 'sample names', 'dD', 'd18O', 'd-ex']
)
```

Function to plot pit data 

**Args:**
 
 - <b>`save`</b> (bool):  save plot 
 - <b>`metadata`</b> (bool):  add metadata to plot 
 - <b>`invert_depth`</b> (bool):  invert depth/height axis. Default is height 
 - <b>`figsize`</b> (tuple):  size of plot in inch. default matplotlib setting 
 - <b>`dpi`</b> (int):  plot resolution, pixel per inches 
 - <b>`plot_order`</b> (list):  list of plots to add to the figure, the order defines the order of the plots 

---

<a href="https://github.com/ArcticSnow/snowpyt/snowpyt/pit_class.py#L563"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `print_layers`

```python
print_layers()
```





---

<a href="https://github.com/ArcticSnow/snowpyt/snowpyt/pit_class.py#L560"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `print_metadata`

```python
print_metadata()
```








---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
