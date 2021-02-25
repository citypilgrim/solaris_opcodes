# imports
import datetime as dt
import os
import os.path as osp
import time

from .baddata_flags import baddataflags_l
from .telegram_API import main as telegram_API
from ..global_imports.solaris_opcodes import *


# params
_msgprepend = f'''Notification from {__name__}
'''


# main func
@verbose
@announcer(newlineboo=True)
def main(timestamp, lidarname):
    '''
    Performs a bad data check. Each bad data flag protocol is in the .baddata_flags
    directory. It will notify the user if there is a net message to send

    Parameters
        timestamp (datetime like): datetime like object which checks for, will be treated as the
                                   same utc offset as the solaris server
        lidarname (str): name of the lidar for which data we want to check
    '''

    msg = ''

    for baddataflags_func in baddataflags_l:
        msg += baddataflags_func(timestamp, lidarname) + '\n'

    if msg:
        telegram_API(_msgprepend + msg)
        print(TIMEFMT.format(timestamp) + ' sending notification')
        print('message:')
        print('\n'.join(['\t' + line for line in msg.split('\n')]))


# running
if __name__ == '__main__':
    # imports
    import datetime as dt

    timestamp = LOCTIMEFN(dt.datetime.now(), SOLARISUTCOFFSET)
    lidarname = LIDARNAME
    main(timestamp, lidarname)
