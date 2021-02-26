# imports
import os

import numpy as np
import pandas as pd

from ...file_readwrite import cloudproduct_reader
from ...global_imports.solaris_opcodes import *


# params
_msgprepend = """
cloudproduct_nancheck
"""
_cloudheightduration = pd.Timedelta(CLOUDHEIGHTDURATION, 'm')


# supp function
def _nancheck_func(cloudheights_pAl):
    '''
    Given the output from cloudproduct_reader, check whether all the pixels display no clouds.
    This is the case when all pixels contain a np.nan value
    '''
    cloudheights_pa = np.array([
        cloudheights_Aa[0] for cloudheights_Aa in cloudheights_pAl
    ])
    return np.isnan(cloudheights_pa).prod()



# main func
def main(endtime, lidarname):
    '''
    Checks the generated YYYYMMddhhmm_cloudheight.txt by
    solaris_opcode.product_calc.cloudproduct_print in the last CLOUDHEIGHTDURATION minutes
    for nan values.
    If the entire grid is nan for an extended duration of time, it is indicative that something
    is up with the lidar. Sometimes this could mean that the scanner head is pointing downwards,
    thereby not being able to detect any clouds

    Parameters
        endtime (datetime like): endtime from which to check the data
        lidarname (str): name of lidar for which data we want to check

    Return
        msg (str): message output from printing any error
    '''
    # searching through the appropriate files
    starttime = endtime - _cloudheightduration
    currentday = endtime - pd.Timedelta(SOLARISUTCOFFSET, 'h')
    previousday = currentday - pd.Timedelta(1, 'd')
    directories = [
        DIRCONFN(
            SOLARISMPLDIR.format(lidarname),
            DATEFMT.format(day)
        ) for day in [currentday, previousday]
    ]
    file_a = np.array(FINDFILESFN(CLOUDPRODUCTFILE, directories))
    ## filtering according to the endtime and starttime
    time_a = np.array([
        LOCTIMEFN(DIRPARSEFN(osp.basename(f), CLOUDPRODUCTTIMEFIELD), LIDARUTCOFFSET)
        for f in file_a
    ])
    file_a = file_a[(time_a >= starttime) * (time_a <= endtime)]

    if not file_a.size:                  # makesure that there are files to read
        msg = ''
        return msg

    # reading all files and checking if all nan
    nan_a = np.array([                      # ind -1 takes only the cloud heightb
        _nancheck_func(cloudproduct_reader(f)[-1])
        for f in file_a
    ])
    nan_boo = nan_a.prod()

    # creating message if needed
    if nan_boo:
        msg = '<pre>' + 'No cloud layers from:' + '</pre>\n'\
          + '<pre>' + f'{endtime}' + '</pre>\n'\
          + '<pre>' + 'to:' + '</pre>\n'\
          + '<pre>' + f'{starttime}' + '</pre>\n\n'
    else:
        msg = ''

    return msg


# testing
if __name__ ==  '__main__':
    msg = main(
        LOCTIMEFN('202102241400', 8), 'smmpl_E2'
    )

    print(msg)
