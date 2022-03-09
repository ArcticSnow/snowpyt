<!-- markdownlint-disable -->

<a href="https://github.com/ArcticSnow/snowpyt/snowpyt/nirpy.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `snowpyt.nirpy`
Collection of NIR processing tools S. Filhol, March 2022 



Inpired by the paper by Matzl and Schneebeli 2016 for more info 

A calibration profile was derived from the camera with Micmac. This calibration profile is for correcting vigneting. correct image for vignetting (calib profile is of the size of Raw images. Crop from center to use with jpegs detrend if needed the luminosity, as it can vary linearly from top to bottom of the snowpit sample targets for absolute reflectance calibration (white= 99%, and grey=50%). Fit a linear model Convert reflectance image to SSA with the conversion equation  𝑆𝑆𝐴=𝐴𝑒𝑟/𝑡 

Finally, use the ruler (or other object of know size) in image to scale image dimension to metric system. 



**TODO:**
 
- write function to extract SSA profile to import in niviz.org 
- Raw images are in 12 bit. Find a way to convert to BW from original while maintaining the 12bit resolution. Rawpy might be useful. Then make sure the processing pipeline can accept 12bit data (i.e. all skimage functions) 
- wrap micmac function to extract profile 'mm3d vodka'. At least provide the method on how to do it. 


---

<a href="https://github.com/ArcticSnow/snowpyt/snowpyt/nirpy.py#L31"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `kernel_square`

```python
kernel_square(nPix)
```

Function to defin a square kernel of equal value for performing averaging 

**Args:**
 
 - <b>`nPix`</b> (int):  size of the kernel in pixel 



**Returns:**
 
 - <b>`array`</b>:  kernel matrix 


---

<a href="https://github.com/ArcticSnow/snowpyt/snowpyt/nirpy.py#L48"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `smooth`

```python
smooth(mat, kernel)
```

Function that produce a smoothed version of the 2D array 

**Args:**
 
 - <b>`mat`</b>:  2D Array to smooth 
 - <b>`kernel`</b>:  kernel array (output) from the function kernel_square() 



**Returns:**
 
 - <b>`2D array`</b>:  smoothed array 


---

<a href="https://github.com/ArcticSnow/snowpyt/snowpyt/nirpy.py#L63"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `micmac_radiometric`

```python
micmac_radiometric()
```

List of commands to run for deriving a radiometric calibratino profile for the camera 


---

<a href="https://github.com/ArcticSnow/snowpyt/snowpyt/nirpy.py#L72"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `nir`
Class to process NIR snowpit photograph. 

<a href="https://github.com/ArcticSnow/snowpyt/snowpyt/nirpy.py#L76"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    fname_nir,
    fname_calib,
    highpass=True,
    kernel_size=2000,
    rotate_calib=False
)
```

Class initialization 

**Args:**
 
 - <b>`fname_nir`</b> (str):  path to NIR image 
 - <b>`fname_calib`</b> (str):  path to radiometric calibration image 
 - <b>`highpass`</b> (bool):  perform high pass filtering to remove luminosity gradient across the pit 
 - <b>`kernel_size`</b> (int):  size of the kernel for the highpass filter 




---

<a href="https://github.com/ArcticSnow/snowpyt/snowpyt/nirpy.py#L205"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `apply_calib`

```python
apply_calib(crop_calib=False)
```

Function to apply calibration profile to the NIR image. 

**Args:**
 
 - <b>`crop_calib`</b> (bool):  if calibration and image are of slightly different size, crop calib and align the two with center. 

---

<a href="https://github.com/ArcticSnow/snowpyt/snowpyt/nirpy.py#L189"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `convert_all`

```python
convert_all()
```

Function to convert pixel values to physical values using the targets 

---

<a href="https://github.com/ArcticSnow/snowpyt/snowpyt/nirpy.py#L169"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `convert_to_SSA`

```python
convert_to_SSA()
```

Function to convert reflectance to SSA 

---

<a href="https://github.com/ArcticSnow/snowpyt/snowpyt/nirpy.py#L179"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `convert_to_doptic`

```python
convert_to_doptic()
```

Function to convert SSA to optical diameter 

---

<a href="https://github.com/ArcticSnow/snowpyt/snowpyt/nirpy.py#L150"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `convert_to_reflectance`

```python
convert_to_reflectance()
```

Function to convert image to reflectance using at minimum 2 sets of reflectance targets previously picked 

---

<a href="https://github.com/ArcticSnow/snowpyt/snowpyt/nirpy.py#L280"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `extract_profile`

```python
extract_profile(
    imgs=['SSA', 'reflectance', 'd_optical'],
    param={'method': <module 'scipy' from '/home/simonfi/miniconda3/envs/dataAna/lib/python3.8/site-packages/scipy/__init__.py'>, 'n_samples': 1000}
)
```

Function to extract profile of values for a list of images 



**Args:**
 
 - <b>`imgs`</b> (list):  images from which to sample profile param (dict): 
 - <b>`method`</b> (str):  method to sample the profile. Avail: numpy, scipy, and skimage. 
 - <b>`n_sample`</b> (int, numpy and scipy method):  number of samples along profile 
 - <b>`linewidth`</b> (int, skimage method):  width of the profile 
 - <b>`reduce_func`</b> (func, skimage method):  function to agglomerate the pixels perpendicular to the line 
 - <b>`spline_order`</b> (int, 0-5, skimage method):  order of the spline applied to the sampled profile 



**examples:**
  {'method': scipy, 'n_samples':1000},  {'method': numpy, 'n_samples':1000},  {'method': skimage, 'linewidth':5, 'reduce_func':np.median, 'spline_order':1} 

---

<a href="https://github.com/ArcticSnow/snowpyt/snowpyt/nirpy.py#L197"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `load_calib`

```python
load_calib()
```

Function to load radiometrci calibration file 

---

<a href="https://github.com/ArcticSnow/snowpyt/snowpyt/nirpy.py#L238"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `load_nir`

```python
load_nir()
```

Function to load jpeg NIR images, and convert them to BW 

---

<a href="https://github.com/ArcticSnow/snowpyt/snowpyt/nirpy.py#L111"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `pick_targets`

```python
pick_targets(reflectances=[99, 50])
```

Function to pick reflectance targets 

**Args:**
 
 - <b>`reflectances`</b> (list of int):  List of reflectance targets to pick 

---

<a href="https://github.com/ArcticSnow/snowpyt/snowpyt/nirpy.py#L245"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `scale_spatially`

```python
scale_spatially()
```

Function to bring real spatial coordinate 

Method:  1. click two points  2. provide corresponding length  3. option to provide geometrical correction 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
