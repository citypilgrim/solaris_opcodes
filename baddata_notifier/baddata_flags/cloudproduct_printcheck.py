# imports
import os
import pandas as pd

from ...file_readwrite import cloudproduct_reader
from ...global_imports.solaris_opcodes import *


# params
_msgprepend = """
cloudproduct_presentcheck
"""
_cloudprintduration = pd.Timedelta(CLOUDPRINTDURATION, 'm')


# main func
def main(endtime, lidarname):
    '''
    Checks whether the  YYYYMMddhhmm_cloudheight.txt is generated
    solaris_opcode.product_calc.cloudproduct_print in the last CLOUDPRINTDURATION minutes

    Parameters
        endtime (datetime like): endtime from which to check the data
        lidarname (str): name of lidar for which data we want to check

    Return
        msg (str): message output from printing any error
    '''
    # searching through the appropriate files
    starttime = endtime - _cloudprintduration
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

    # creating message if needed
    if not file_a.size:
        msg = '<pre>' + 'No cloud height file produced' + '</pre>\n'\
          + '<pre>' + f'in the last {CLOUDPRINTDURATION} mins from:' + '</pre>\n'\
          + '<pre>' + f'{endtime}' + '</pre>\n\n'
        msg =_msgprepend + msg
    else:
        msg = ''

    return msg


# testing
if __name__ ==  '__main__':
    msg = main(
        LOCTIMEFN('202102240000', 8), 'smmpl_E2'
    )

    print(msg)
