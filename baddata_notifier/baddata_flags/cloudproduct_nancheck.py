# imports
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
    Given the output from cloudproduct_reader, check whether all the pixels display no clouds
    '''


# main func
def main(starttime, lidarname):
    '''
    Checks the generated YYYYMMddhhmm_cloudheight.txt by
    solaris_opcode.product_calc.cloudproduct_print in the last CLOUDHEIGHTDURATION minutes
    for nan values.
    If the entire grid is nan for an extended duration of time, it is indicative that something
    is up with the lidar. Sometimes this could mean that the scanner head is pointing downwards,
    thereby not being able to detect any clouds

    Parameters
        starttime (datetime like): starttime from which to check the data
        lidarname (str): name of lidar for which data we want to check

    Return
        msg (str): message output from printing any error
    '''
    # searching through the appropriate files
    endtime = starttime - _cloudheightduration
    currentday = starttime - pd.Timedelta(SOLARISUTCOFFSET, 'h')
    previousday = currentday - pd.Timedelta(1, 'd')
    directories = [
        DIRCONFN(
            SOLARISMPLDIR.format(lidarname),
            DATEFMT.format(day)
        ) for day in [currentday, previousday]
    ]
    file_l = FINDFILESFN(CLOUDPRODUCTFILE, directories)

    # reading all files and checking if all nan
    nan_boo = False

    # creating message if needed
    if nan_boo:
        msg = '<pre>' + 'No new profile since:' + '</pre>\n'\
          # + '<pre>' + f'{profile_dt}' + '</pre>\n'\

    else:
        msg = ''

    return msg


# testing
if __name__ ==  '__main__':
    main(
        LOCTIMEFN('202102241700', 8), 'smmpl_E2'
    )
