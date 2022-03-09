<!-- markdownlint-disable -->

<a href="https://github.com/ArcticSnow/snowpyt/snowpyt/CAAMLv6_xml.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `snowpyt.CAAMLv6_xml`
Created on Tue Jul 04 13:32:31 2017 

@author: Simon Filhol, Guillaume Sutter 

Collection of functions to import snowpit data stored in the CAAMLv6 xml standard 


---

<a href="https://github.com/ArcticSnow/snowpyt/snowpyt/CAAMLv6_xml.py#L17"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_temperature`

```python
get_temperature(path_xml, print2term=True)
```

Function to extract temperature profile from CAAML xml file 

**Args:**
 
 - <b>`path_xml`</b> (str):  path to xml file 
 - <b>`print2term`</b> (bool):  print profile to termninal 



**Returns:**
 
 - <b>`array`</b>:  temperature profile 


---

<a href="https://github.com/ArcticSnow/snowpyt/snowpyt/CAAMLv6_xml.py#L55"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_density`

```python
get_density(path_xml, print2term=True)
```

Function to extract density profile from CAAML xml file 

**Args:**
 
 - <b>`path_xml`</b> (str):  path to xml file 
 - <b>`print2term`</b> (bool):  print profile to termninal 



**Returns:**
 
 - <b>`array`</b>:  density profile 


---

<a href="https://github.com/ArcticSnow/snowpyt/snowpyt/CAAMLv6_xml.py#L101"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `childValueNoneTest`

```python
childValueNoneTest(child)
```






---

<a href="https://github.com/ArcticSnow/snowpyt/snowpyt/CAAMLv6_xml.py#L107"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `has_child`

```python
has_child(node, idx=0, dtype='str', unit_ret=False, print2term=True)
```






---

<a href="https://github.com/ArcticSnow/snowpyt/snowpyt/CAAMLv6_xml.py#L139"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `is_node`

```python
is_node(node)
```






---

<a href="https://github.com/ArcticSnow/snowpyt/snowpyt/CAAMLv6_xml.py#L146"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_metadata`

```python
get_metadata(path_xml, print2term=True)
```

Function to extract snowpit metadata profile from CAAML xml file 

**Args:**
 
 - <b>`path_xml`</b> (str):  path to xml file 
 - <b>`print2term`</b> (bool):  print profile to termninal 



**Returns:**
 metadata object 


---

<a href="https://github.com/ArcticSnow/snowpyt/snowpyt/CAAMLv6_xml.py#L192"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_layers`

```python
get_layers(path_xml, print2term=True)
```

Function to extract layers from CAAML xml file 

**Args:**
 
 - <b>`path_xml`</b> (str):  path to xml file 
 - <b>`print2term`</b> (bool):  print profile to termninal 



**Returns:**
 
 - <b>`list`</b>:  layers content 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
