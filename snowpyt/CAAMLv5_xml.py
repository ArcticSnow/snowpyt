# -*- coding: utf-8 -*-
"""
Created on Tue Jul 04 13:32:31 2017

@author: Guillaume Sutter

Collection of functions to import snowpit data stored in the CAAMLv5 xml standard
    
"""

import xml.dom.minidom
import pit_class as pc

def get_metadata(path_xml):
    DOMTree = xml.dom.minidom.parse(path_xml)
    Tree = DOMTree.documentElement
    Metadata = pc.metadata()

    Metadata.date = Tree.getElementsByTagName("caaml:timePosition")[0].firstChild.nodeValue
    #Metadata.operation = Tree.getElementsByTagName("caaml:Operation")[0].childNodes[1].firstChild.nodeValue
    Metadata.observer = Tree.getElementsByTagName("caaml:name")[0].firstChild.nodeValue
    Metadata.profile_depth = float(Tree.getElementsByTagName("caaml:profileDepth")[0].firstChild.nodeValue)
    Metadata.profile_depth_unit = Tree.getElementsByTagName("caaml:profileDepth")[0].attributes.item(0).value
    Metadata.sky_condition = Tree.getElementsByTagName("caaml:skyCond")[0].firstChild.nodeValue
    #Metadata.precipitation = Tree.getElementsByTagName("caaml:precipTI")[0].firstChild.nodeValue
    Metadata.air_temperature = float(Tree.getElementsByTagName("caaml:airTempPres")[0].firstChild.nodeValue)
    Metadata.air_temperature_unit = Tree.getElementsByTagName("caaml:airTempPres")[0].attributes.item(0).value
    Metadata.windspeed = float(Tree.getElementsByTagName("caaml:windSpd")[0].firstChild.nodeValue)
    Metadata.windspeed_unit = Tree.getElementsByTagName("caaml:windSpd")[0].attributes.item(0).value
    Metadata.winddir = float(Tree.getElementsByTagName("caaml:windDir")[0].firstChild.nodeValue)

    Metadata.elevation = float(Tree.getElementsByTagName("caaml:ElevationPosition")[0].childNodes[1].firstChild.nodeValue)
    Metadata.elevation_unit = Tree.getElementsByTagName("caaml:ElevationPosition")[0].attributes.item(0).value
    Metadata.location_description = Tree.getElementsByTagName("caaml:ObsPoint")[0].childNodes[1].firstChild.nodeValue
    Metadata.srsName = Tree.getElementsByTagName("gml:Point")[0].attributes.item(0).value
    if Tree.getElementsByTagName("gml:Point")[0].childNodes[1].firstChild is not None:
        Metadata.east = float(
            Tree.getElementsByTagName("gml:Point")[0].childNodes[1].firstChild.nodeValue.split(" ")[0])
        Metadata.north = float(
            Tree.getElementsByTagName("gml:Point")[0].childNodes[1].firstChild.nodeValue.split(" ")[1])
    return Metadata

def get_layers(path_xml):
    DOMTree = xml.dom.minidom.parse(path_xml)
    Tree = DOMTree.documentElement
    stratProfile = Tree.getElementsByTagName("caaml:stratProfile")
    Layers = []
    for Layer in stratProfile[0].childNodes:
        if Layer.nodeType not in {3, 8}:
            lay = pc.layer()
            for child in Layer.childNodes:
                if child.nodeType not in {3, 8}:
                    if child.localName == "caaml:depthTop" and child.firstChild is not None:
                        lay.dtop = float(child.firstChild.nodeValue)
                        lay.dtop_unit = child.attributes.item(0).value
                    elif child.localName == "caaml:thickness" and child.firstChild is not None:
                        lay.thickness = float(child.firstChild.nodeValue)
                        lay.thickness_unit = child.attributes.item(0).value
                    elif child.localName == "caaml:grainFormPrimary" and child.firstChild is not None:
                        lay.grain_type1 = child.firstChild.nodeValue
                    elif child.localName == "caaml:grainFormSecondary" and child.firstChild is not None:
                        lay.grain_type2 = child.firstChild.nodeValue
                    elif child.localName == "caaml:grainSize":
                        lay.grain_size_unit = child.attributes.item(0).value
                        for component in child.childNodes[1].childNodes:
                            if component.nodeType not in {3, 8}:
                                if component.localName == "caaml:avg" and component.firstChild is not None:
                                    lay.grain_size_avg = float(component.firstChild.nodeValue)
                                elif component.localName == "caaml:avgMax" and component.firstChild is not None:
                                    lay.grain_size_max = float(component.firstChild.nodeValue)
                    elif child.localName == "caaml:hardness" and child.firstChild is not None:
                        lay.hardness = child.firstChild.nodeValue
                    elif child.localName == "caaml:lwc" and child.firstChild is not None:
                        lay.lwc = child.firstChild.nodeValue
            Layers += [lay]
    return Layers

def get_temperature(path_xml):
    DOMTree = xml.dom.minidom.parse(path_xml)
    Tree = DOMTree.documentElement
    temperatureProfile = Tree.getElementsByTagName("caaml:tempProfile")
    TProfile = pc.temperature_profile()
    TProfile.depth_unit = temperatureProfile[0].attributes.item(0).value
    TProfile.temp_unit = temperatureProfile[0].attributes.item(1).value
    for obs in temperatureProfile[0].childNodes:
        if obs.nodeType not in {3, 8}:
            for child in obs.childNodes:
                if child.nodeType not in {3, 8}:
                    if child.localName == "caaml:depth" and child.firstChild is not None:
                        TProfile.depth += [float(child.firstChild.nodeValue)]
                    elif child.localName == "caaml:snowTemp" and child.firstChild is not None:
                        TProfile.temp += [float(child.firstChild.nodeValue)]
    return TProfile

def get_density(path_xml):
    DOMTree = xml.dom.minidom.parse(path_xml)
    Tree = DOMTree.documentElement
    densityProfile = Tree.getElementsByTagName("caaml:densityProfile")
    DProfile = pc.density_profile()
    DProfile.depth_unit = densityProfile[0].attributes.item(0).value
    DProfile.thickness_unit = densityProfile[0].attributes.item(1).value
    DProfile.density_unit = densityProfile[0].attributes.item(2).value
    for layer in densityProfile[0].childNodes:
        if layer.nodeType not in {3, 8}:
            for child in layer.childNodes:
                if child.nodeType not in {3, 8}:
                    if child.localName == "caaml:depthTop" and child.firstChild is not None:
                        DProfile.depth += [float(child.firstChild.nodeValue)]
                    elif child.localName == "caaml:thickness" and child.firstChild is not None:
                        DProfile.thickness += [float(child.firstChild.nodeValue)]
                    elif child.localName == "caaml:density" and child.firstChild is not None:
                        DProfile.density += [float(child.firstChild.nodeValue)]
    return DProfile

# if __main__():
#     # Example on how to use the functions
#     path1 = "snowpyt/data_example/20160331_finse.xml"
#     A = get_layers(path1)
#     B = get_temperature(path1)
#     C = get_density(path1)
#     D = get_metadata(path1)





# ==============================================================================
# for child in Tree.childNodes:
#     if child.nodeType not in {3,8}:
#         print "\n"+child.localName
#         for child2 in child.childNodes:
#             if child2.nodeType not in {3,8} and str(child2.firstChild)!="None":
#                 if child2.hasAttributes():
#                     if child2.firstChild.nodeType not in {3,8}:
#                         print "\t{}: {} {}".format(child2.localName,child2.firstChild.nodeValue,child2.attributes.item(0).value)
#                     else:
#                         print "\t{}: {}".format(child2.localName,child2.attributes.item(0).value)
#                 else:
#                     if str(child2.firstChild.nodeValue).split(" ")[0]!="\n":
#                         print "\t{}: {}".format(child2.localName,child2.firstChild.nodeValue)
#                     else:
#                         print "\t{}".format(child2.localName)
#                 for child3 in child2.childNodes:
#                     if child3.nodeType not in {3,8} and str(child3.firstChild)!="None":
#                         if child3.hasAttributes():
#                             if child3.firstChild.nodeType not in {3,8}:
#                                 print "\t\t{}: {} {}".format(child3.localName,child3.firstChild.nodeValue,child3.attributes.item(0).value)
#                             else:
#                                 print "\t\t{}: {}".format(child3.localName,child3.attributes.item(0).value)
#                         else:
#                             if str(child3.firstChild.nodeValue).split(" ")[0]!="\n":
#                                 print "\t\t{}: {}".format(child3.localName,child3.firstChild.nodeValue)
#                             else:
#                                 print "\t\t{}".format(child3.localName)
#                         for child4 in child3.childNodes:
#                             if child4.nodeType not in {3,8} and str(child4.firstChild)!="None":
#                                 if child4.hasAttributes():
#                                     if child4.firstChild.nodeType not in {3,8}:
#                                         print "\t\t\t{}: {} {}".format(child4.localName,child4.firstChild.nodeValue,child4.attributes.item(0).value)
#                                     else:
#                                         print "\t\t\t{}: {}".format(child4.localName,child4.attributes.item(0).value)
#                                 else:
#                                     if str(child4.firstChild.nodeValue).split(" ")[0]!="\n":
#                                         print "\t\t\t{}: {}".format(child4.localName,child4.firstChild.nodeValue)
#                                     else:
#                                         print "\t\t\t{}".format(child4.localName)
#                                 for child5 in child4.childNodes:
#                                     if child5.nodeType not in {3,8} and str(child5.firstChild)!="None":
#                                         if child5.hasAttributes():
#                                             if child5.firstChild.nodeType not in {3,8}:
#                                                 print "\t\t\t\t{}: {} {}".format(child5.localName,child5.firstChild.nodeValue,child5.attributes.item(0).value)
#                                             else:
#                                                 print "\t\t\t\t{}: {}".format(child5.localName,child5.attributes.item(0).value)
#                                         else:
#                                             if str(child5.firstChild.nodeValue).split(" ")[0]!="\n":
#                                                 print "\t\t\t\t{}: {}".format(child5.localName,child5.firstChild.nodeValue)
#                                             else:
#                                                 print "\t\t\t\t{}".format(child5.localName)
#                                         for child6 in child5.childNodes:
#                                             if child6.nodeType not in {3,8} and str(child6.firstChild)!="\n":
#                                                 if child6.hasAttributes():
#                                                     if child6.firstChild.nodeType not in {3,8}:
#                                                         print "\t\t\t\t\t{}: {} {}".format(child6.localName,child6.firstChild.nodeValue,child6.attributes.item(0).value)
#                                                     else:
#                                                         print "\t\t\t\t\t{}: {}".format(child6.localName,child6.attributes.item(0).value)
#                                                 else:
#                                                     if str(child6.firstChild.nodeValue).split(" ")[0]!="\n":
#                                                         print "\t\t\t\t\t{}: {}".format(child6.localName,child6.firstChild.nodeValue)
#                                                     else:
#                                                         print "\t\t\t\t\t{}".format(child6.localName)
#                                                 for child7 in child6.childNodes:
#                                                     if child7.nodeType not in {3,8} and str(child7.firstChild)!="None":
#                                                         if child7.hasAttributes():
#                                                             if child7.firstChild.nodeType not in {3,8}:
#                                                                 print "\t\t\t\t\t\t{}: {} {}".format(child7.localName,child7.firstChild.nodeValue,child7.attributes.item(0).value)
#                                                             else:
#                                                                 print "\t\t\t\t\t\t{}: {}".format(child7.localName,child7.attributes.item(0).value)
#                                                         else:
#                                                             if str(child7.firstChild.nodeValue).split(" ")[0]!="\n":
#                                                                 print "\t\t\t\t\t\t{}: {}".format(child7.localName,child7.firstChild.nodeValue)
#                                                             else:
#                                                                 print "\t\t\t\t\t\t{}".format(child7.localName)
# ==============================================================================
