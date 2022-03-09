<!-- markdownlint-disable -->

# API Overview

## Modules

- [`snowpyt`](./snowpyt.md#module-snowpyt)
- [`snowpyt.CAAMLv6_xml`](./snowpyt.CAAMLv6_xml.md#module-snowpytcaamlv6_xml): Created on Tue Jul 04 13:32:31 2017
- [`snowpyt.nirpy`](./snowpyt.nirpy.md#module-snowpytnirpy): Collection of NIR processing tools
- [`snowpyt.pit_class`](./snowpyt.pit_class.md#module-snowpytpit_class): File defining a python class for snowpit data
- [`snowpyt.snowflake`](./snowpyt.snowflake.md#module-snowpytsnowflake)
- [`snowpyt.snowflake.sf_dict`](./snowpyt.snowflake.sf_dict.md#module-snowpytsnowflakesf_dict): Created on 6 avr. 2017

## Classes

- [`nirpy.nir`](./snowpyt.nirpy.md#class-nir): Class to process NIR snowpit photograph.
- [`pit_class.Snowpit`](./snowpyt.pit_class.md#class-snowpit)
- [`pit_class.density_profile`](./snowpyt.pit_class.md#class-density_profile)
- [`pit_class.layer`](./snowpyt.pit_class.md#class-layer)
- [`pit_class.metadata`](./snowpyt.pit_class.md#class-metadata)
- [`pit_class.sample_profile`](./snowpyt.pit_class.md#class-sample_profile)
- [`pit_class.temperature_profile`](./snowpyt.pit_class.md#class-temperature_profile)

## Functions

- [`CAAMLv6_xml.childValueNoneTest`](./snowpyt.CAAMLv6_xml.md#function-childvaluenonetest)
- [`CAAMLv6_xml.get_density`](./snowpyt.CAAMLv6_xml.md#function-get_density): Function to extract density profile from CAAML xml file
- [`CAAMLv6_xml.get_layers`](./snowpyt.CAAMLv6_xml.md#function-get_layers): Function to extract layers from CAAML xml file
- [`CAAMLv6_xml.get_metadata`](./snowpyt.CAAMLv6_xml.md#function-get_metadata): Function to extract snowpit metadata profile from CAAML xml file
- [`CAAMLv6_xml.get_temperature`](./snowpyt.CAAMLv6_xml.md#function-get_temperature): Function to extract temperature profile from CAAML xml file
- [`CAAMLv6_xml.has_child`](./snowpyt.CAAMLv6_xml.md#function-has_child)
- [`CAAMLv6_xml.is_node`](./snowpyt.CAAMLv6_xml.md#function-is_node)
- [`nirpy.kernel_square`](./snowpyt.nirpy.md#function-kernel_square): Function to defin a square kernel of equal value for performing averaging
- [`nirpy.micmac_radiometric`](./snowpyt.nirpy.md#function-micmac_radiometric): List of commands to run for deriving a radiometric calibratino profile for the camera
- [`nirpy.smooth`](./snowpyt.nirpy.md#function-smooth): Function that produce a smoothed version of the 2D array


---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
