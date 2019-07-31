'''
Created on 6 avr. 2017

@author: hagenmullerp
'''

import numpy as np
from matplotlib.colors import LinearSegmentedColormap

MEPRA_dict = {'PP': 0,      # fr
              'PP+DF': 1,   # fr_lb
              'DF': 2,      # lb
              'DF+RG': 3,   # lb_fin
              'DF+FC': 4,   # lb_ang
              'PPgp': 5,    # roul
              'RG': 6,      # fin
              'MF+RG': 7,   # fin_ar
              'RG+FC': 8,   # fin_ang
              'FC': 9,      # pl
              'FC+DH': 10,  # pl_gob
              'DH': 11,     # gob
              'MF': 12,     # gel
              'MF+DH': 13,  # gob_fon
              'MF+FC': 14   # ron_ang
              }

MEPRA_labels = ['PP', 'PP+DF', 'DF', 'DF+RG', 'DF+FC', 'PPgp', 'RG', 'MF+RG', 'RG+FC', 'FC', 'FC+DH', 'DH', 'MF', 'MF+DH', 'MF+FC']

coloring = {'PP': np.array([0, 255, 0]) / 255.0,
            'MM': np.array([255, 215, 0]) / 255.0,
            'DF': np.array([34, 139, 34]) / 255.0,
            'RG': np.array([255, 182, 193]) / 255.0,
            'FC': np.array([173, 216, 230]) / 255.0,
            'DH': np.array([0, 0, 255]) / 255.0,
            'SH': np.array([250, 0, 255]) / 255.0,
            'MF': np.array([255, 0, 0]) / 255.0,
            'MFcr': np.array([255, 255, 255]) / 255.0,
            'IF': np.array([0, 255, 255]) / 255.0,
            'NO': np.array([200, 200, 200]) / 255.0}

color_grain = {MEPRA_dict['PP']: coloring['PP'],
               MEPRA_dict['PP+DF']: 0.5 * (coloring['PP'] + coloring['DF']),
               MEPRA_dict['DF']: coloring['DF'],
               MEPRA_dict['DF+RG']: 0.5 * (coloring['DF'] + coloring['RG']),
               MEPRA_dict['DF+FC']: 0.5 * (coloring['DF'] + coloring['FC']),
               MEPRA_dict['PPgp']: [0, 0, 0],
               MEPRA_dict['RG']: coloring['RG'],
               MEPRA_dict['MF+RG']: 0.5 * (coloring['MF'] + coloring['RG']),
               MEPRA_dict['RG+FC']: 0.5 * (coloring['RG'] + coloring['FC']),
               MEPRA_dict['FC']: coloring['FC'],
               MEPRA_dict['FC+DH']: 0.5 * (coloring['FC'] + coloring['DH']),
               MEPRA_dict['DH']: coloring['DH'],
               MEPRA_dict['MF']: coloring['MF'],
               MEPRA_dict['MF+DH']: 0.5 * (coloring['MF'] + coloring['DH']),
               MEPRA_dict['MF+FC']: 0.5 * (coloring['MF'] + coloring['FC'])}

grain_colormap = LinearSegmentedColormap.from_list("custom", [[i / 14., color_grain[i]] for i in range(15)])



hardness_dict = {
                    'F-':0.5,
                    'F':1,
                    'F+':1.25,
                    'F-4F':1.5,
                    '4F-':1.75,
                    '4F':2,
                    '4F+':2.25,
                    '4F-1F':2.5,
                    '1F-':2.75,
                    '1F':3,
                    '1F+':3.25,
                    '1F-P':3.5,
                    'P+':3.75,
                    'P':4,
                    'P+':4.3,
                    'P-K':4.6,
                    'K':5,
                    'K+':5.3,
                    'K-I':5.6,
                    'I':6}

snowflake_symbol_dict = {'PP':'snowflake/recent_snow.png',
                    'DF':'snowflake/partly_decomposed.png',
                    'DFdc':'snowflake/partly_decomposed.png',
                    'DFbk':'snowflake/wind_broken_precip.png',
                    'MM':'',
                    'RG':'snowflake/large_rounded.png',
                    'RGsr':'snowflake/large_rounded.png',
                    'RGlr':'snowflake/large_rounded.png',
                    'RGwp': 'snowflake/wind_packed.png',
                    'RGxf':'snowflake/faceted_rounded.png',
                    'FC':'snowflake/faceted.png',
                    'FCso':'snowflake/faceted.png',
                    'FCsf':'snowflake/near_surface_faceted.png',
                    'FCxr':'snowflake/rounding_faceted.png',
                    'DH':'snowflake/hollow_cups.png',
                    'DHcp':'snowflake/hollow_cups.png',
                    'DHpr':'snowflake/hollow_prism.png',
                    'DHch':'snowflake/chains_of_depth_hoar.png',
                    'DHla':'',
                    'DHxr':'snowflake/rounding_depth_hoar.png',
                    'SH':'snowflake/surface_hoar.png',
                    'SHsu':'snowflake/surface_hoar.png',
                    'SHcv':'snowflake/cavity_crevasse_hoar.png',
                    'SHxr':'snowflake/rounding_surface_hoar.png',
                    'MF':'snowflake/cluster_rounded.png',  # need to be verified
                    'MFcl':'snowflake/cluster_rounded.png',
                    'MFpc':'snowflake/rounded_polycrystals.png',
                    'MFsl':'snowflake/slush.png',
                    'MFcr':'snowflake/melt_freeze_crust.png',
                    'IF':'snowflake/ice.png',
                    'IFil':'snowflake/ice.png',
                    'IFic':'snowflake/ice_column.png',
                    'IFbi':'snowflake/basal_ice.png',
                    'IFrc':'snowflake/rain_crust.png',
                    'IFsc':'',
                    'basal ice':'snowflake/basal_ice.png',
                    'cavity crevasse hoar':'snowflake/cavity_crevasse_hoar.png',
                    'chains of depth hoar':'snowflake/chains_of_depth_hoar.png',
                    'clustered rounded':'snowflake/cluster_rounded.png',
                    'cluster rounded':'snowflake/cluster_rounded.png',
                    'depth hoar':'snowflake/hollow_cups.png',
                    'faceted':'snowflake/faceted.png',
                    'faceted and rounded':'snowflake/faceted_rounded.png',
                    'faceted rounded':'snowflake/faceted_rounded.png',
                    'hollow cups':'snowflake/hollow_cups.png',
                    'hollow prism':'snowflake/hollow_prism.png',
                    'hoar frost':'snowflake/surface_hoar.png',
                    'horizontal ice layer':'snowflake/ice.png',
                    'ice':'snowflake/ice.png',
                    'ice column':'snowflake/ice_column.png',
                    'ice layer':'snowflake/ice.png',
                    'ice lenses':'snowflake/ice.png',
                    'melt refreeze':'snowflake/melt_freeze_crust.png',
                    'melt refreeze crust':'snowflake/melt_freeze_crust.png',
                    'melt freeze crust':'snowflake/melt_freeze_crust.png',
                    'near surface faceted':'snowflake/near_surface_faceted.png',
                    'partly decomposed': 'snowflake/partly_decomposed.png',
                    'percolation column':'snowflake/ice_column.png',
                    'percolation':'snowflake/ice_column.png',
                    'rain crust':'snowflake/rain_crust.png',
                    'recent snow':'snowflake/recent_snow.png',
                    'rounding depth hoar':'snowflake/rounding_depth_hoar.png',
                    'rounding surface hoar':'snowflake/rounding_surface_hoar.png',
                    'rounded':'snowflake/large_rounded.png',
                    'rounded and faceted':'snowflake/rounding_faceted.png',
                    'rounded faceted':'snowflake/rounding_faceted.png',
                    'rounded polycrystals':'snowflake/rounded_polycrystals.png',
                    'slush':'snowflake/slush.png',
                    'sun crust':'snowflake/sun_crust.png',
                    'surface hoar':'snowflake/surface_hoar.png',
                    'wind packed':'snowflake/wind_packed.png',
                    'wind slab':'snowflake/wind_packed.png',
                    'windslab':'snowflake/wind_packed.png',
                    'wind broken':'snowflake/wind_broken_precip.png'}