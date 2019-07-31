#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 04 13:32:31 2017

@author: Simon Filhol

Collection of functions to import snowpit data stored in the CAAMLv6 xml standard

"""

import sys
from xml.dom import minidom
import snowpyt.pit_class as pc
import numpy as np
import snowpyt.snowflake.sf_dict as sfd

def get_temperature(path_xml):
    xmldoc = minidom.parse(path_xml)
    itemlist = xmldoc.getElementsByTagName('caaml:tempProfile')
    if itemlist.length > 0:
        TProfile = pc.temperature_profile()
        it_temp=itemlist[0].getElementsByTagName('caaml:snowTemp')
        it_depth = itemlist[0].getElementsByTagName('caaml:depth')

        itemlist = xmldoc.getElementsByTagName('caaml:snowPackCond')
        pit_depth = float(itemlist[0].getElementsByTagName('caaml:hS')[0].getElementsByTagName('caaml:height')[0].firstChild.nodeValue)


        temp = []
        for k in it_temp:
            temp.append(k.firstChild.nodeValue)
        TProfile.temp_unit = str(k.attributes.item(0).value)

        depth = []
        for k in it_depth:
            depth.append(k.firstChild.nodeValue)
        TProfile.depth_unit = str(k.attributes.item(0).value)

        TProfile.depth = pit_depth - np.array(depth).astype(float)
        TProfile.temp = np.array(temp).astype(float)
        return TProfile
    else:
        print('No temperature profile')

def get_density(path_xml):

    xmldoc = minidom.parse(path_xml)
    itemlist = xmldoc.getElementsByTagName('caaml:densityProfile')
    if itemlist.length > 0:
        DProfile = pc.density_profile()
        for id in range(0,itemlist.length):
            try:
                it_density = itemlist[id].getElementsByTagName('caaml:density')
                it_top = itemlist[id].getElementsByTagName('caaml:depthTop')
                it_thick = itemlist[id].getElementsByTagName('caaml:thickness')
            except:
                print('No density profile')

        itemlist = xmldoc.getElementsByTagName('caaml:snowPackCond')
        pit_depth = float(itemlist[0].getElementsByTagName('caaml:hS')[0].getElementsByTagName('caaml:height')[0].firstChild.nodeValue)

        density = []
        for k in it_density:
            density.append(float(k.firstChild.nodeValue))
        DProfile.density_unit = str(it_density[0].attributes.item(0).value)

        depth = []
        for i,k in enumerate(it_top):
            top = pit_depth - float(k.firstChild.nodeValue)
            thick = float(it_thick[i].firstChild.nodeValue)
            depth.append(top-thick/2)
        DProfile.depth_unit = str(it_top[0].attributes.item(0).value)

        DProfile.depth = np.array(depth).astype(float)
        DProfile.density = np.array(density).astype(float)
        return DProfile
    else:
        print('No density profile')


def childValueNoneTest(child):
    try:
        return child.nodeValue
    except:
        return None

def has_child(node, idx=0, dtype='str', unit_ret=False):
    if node.length > 0:
        if dtype == 'str':
            print(node)
            dest_var = str(childValueNoneTest(node[0].firstChild))
        elif dtype == 'float':
            dest_var = float(childValueNoneTest(node[idx].firstChild))
        else:
            dest_var = childValueNoneTest(node[idx].firstChild)

        if unit_ret:
            try:
                unit = node[idx].attributes.item(0).value
            except:
                unit = None
            return dest_var, unit
        else:
            return dest_var
    else:
        print('no data in this field')
        if unit_ret:
            dest_var = None
            unit_ret=None
            return dest_var, unit_ret

        else:
            dest_var = None
            return dest_var


def is_node(node):
    if node.length > 0:
        return True
    else:
        return False


def get_metadata(path_xml):
    print('\n=====================')
    print('Loding metadata... \n')
    Metadata = pc.metadata()

    Tree = minidom.parse(path_xml)

    Metadata.date = has_child(Tree.getElementsByTagName("caaml:timePosition"))
    Metadata.observer = has_child(Tree.getElementsByTagName("caaml:name"))
    Metadata.profile_depth, Metadata.profile_depth_unit = has_child(Tree.getElementsByTagName("caaml:profileDepth"), dtype='float', unit_ret=True)
    Metadata.air_temperature, Metadata.air_temperature_unit = has_child(Tree.getElementsByTagName("caaml:airTempPres"), dtype='float', unit_ret=True)
    Metadata.windspeed, Metadata.windspeed_unit = has_child(Tree.getElementsByTagName("caaml:windSpd"), dtype='float', unit_ret=True)
    Metadata.winddir = has_child(Tree.getElementsByTagName("caaml:windDir"))

    if is_node(Tree.getElementsByTagName("caaml:ElevationPosition")):
        Metadata.elevation, Metadata.elevation_unit = has_child(Tree.getElementsByTagName("caaml:ElevationPosition")[0].getElementsByTagName('caaml:position'), dtype='float', unit_ret=True)
    if is_node(Tree.getElementsByTagName('caaml:SlopeAnglePosition')):
        Metadata.slope, Metadata.slope_unit = has_child(Tree.getElementsByTagName('caaml:SlopeAnglePosition')[0].getElementsByTagName('caaml:position'), dtype='float', unit_ret=True)
    if is_node(Tree.getElementsByTagName('caaml:AspectPosition')):
        Metadata.aspect = has_child(Tree.getElementsByTagName('caaml:AspectPosition')[0].getElementsByTagName('caaml:position'))
    if is_node(Tree.getElementsByTagName('caaml:metaData')):
        Metadata.location_description = has_child(Tree.getElementsByTagName('caaml:metaData')[0].getElementsByTagName('caaml:comment'))
    if is_node(Tree.getElementsByTagName('caaml:snowPackCond')):
        Metadata.snowpack_condition = has_child(Tree.getElementsByTagName('caaml:snowPackCond')[0].getElementsByTagName('caaml:comment'))
    if is_node(Tree.getElementsByTagName('caaml:surfCond')):
        Metadata.surface_condition = has_child(Tree.getElementsByTagName('caaml:surfCond')[0].getElementsByTagName('caaml:comment'))

    if is_node(Tree.getElementsByTagName("gml:Point")):
        Metadata.srsName = Tree.getElementsByTagName("gml:Point")[0].attributes.item(0).value
        if Tree.getElementsByTagName("gml:Point")[0].childNodes[1].firstChild is not None:
            Metadata.east = float(
                Tree.getElementsByTagName("gml:Point")[0].childNodes[1].firstChild.nodeValue.split(" ")[0])
            Metadata.north = float(
                Tree.getElementsByTagName("gml:Point")[0].childNodes[1].firstChild.nodeValue.split(" ")[1])
    return Metadata

def get_layers(path_xml):
    xmldoc = minidom.parse(path_xml)

    itemlist = xmldoc.getElementsByTagName('caaml:snowPackCond')

    pit_depth = has_child(itemlist[0].getElementsByTagName('caaml:hS')[0].getElementsByTagName('caaml:height'), dtype='float')
    print('Total snowpit depth = ' + str(pit_depth))

    stratProfile = xmldoc.getElementsByTagName("caaml:stratProfile")
    Layers = []
    for Layer in stratProfile[0].childNodes[3:]:
        if Layer.nodeType not in {3, 8}:
            lay = pc.layer()
            for child in Layer.childNodes:
                if child.nodeType not in {3, 8}:
                    if child.localName == "depthTop" and child.firstChild is not None:
                        lay.dtop = pit_depth - float(child.firstChild.nodeValue)
                        lay.dtop_unit = str(child.attributes.item(0).value)
                    elif child.localName == "thickness" and child.firstChild is not None:
                        lay.thickness = float(child.firstChild.nodeValue)
                        lay.thickness_unit = child.attributes.item(0).value
                    elif child.localName == "grainFormPrimary" and child.firstChild is not None:
                        lay.grain_type1 = str(child.firstChild.nodeValue)
                    elif child.localName == "grainFormSecondary" and child.firstChild is not None:
                        lay.grain_type2 = str(child.firstChild.nodeValue)
                    elif child.localName == "grainSize":
                        lay.grain_size_unit = str(child.attributes.item(0).value)
                        for component in child.childNodes[1].childNodes:
                            if component.nodeType not in {3, 8}:
                                if component.localName == "avg" and component.firstChild is not None:
                                    lay.grainSize_mean = float(component.firstChild.nodeValue)
                                elif component.localName == "avgMax" and component.firstChild is not None:
                                    lay.grainSize_max = float(component.firstChild.nodeValue)
                    elif child.localName == "hardness" and child.firstChild is not None:
                        lay.hardness = str(child.firstChild.nodeValue)
                        lay.hardness_index = sfd.hardness_dict.get(lay.hardness)
                        lay.hardness_ram = 19.3 * lay.hardness_index ** 2.4
                    elif child.localName == "wetness" and child.firstChild is not None:
                        lay.lwc = str(child.firstChild.nodeValue)

                if lay.dtop is not None and lay.thickness is not None:
                    lay.dbot = lay.dtop - lay.thickness
            Layers += [lay]
    return Layers



