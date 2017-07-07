import CAAML_xml as cx

xml = "snowpyt/data_example/20160331_finse.xml"
A = cx.get_layers(path1)
B = cx.get_temperature(path1)
C = cx.get_density(path1)
D = cx.get_metadata(path1)

