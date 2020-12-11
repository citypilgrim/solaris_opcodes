# imports
import subprocess as sub

from ..global_imports.solaris_opcodes import *


# main func
@verbose
@announcer
def main(
        lidar_ip, lidaruser,
        lidardata_dir,
        lidarname,
        syncday_lst
):
    '''
    pulls the data from the lidar laptop.
    By default syncs current day and previous day's data.

    Parameters
        lidar_ip (str): IP address of the lidar laptop
        lidaruser (str): username of the lidar laptop
        lidardata_dir (str): directory containing all the date directories
                             that contain the lidar data
        lidarname (str): name of lidar in the solaris server
        syncday_lst (lst): list objects are strings of the format DATEFMT
    '''
    # correcting input directory for rsync program on windows to recognise
    if lidardata_dir[:2] == 'C:':
        lidardata_dir = lidardata_dir.replace('C:', '/cygdrive/c')

    # rsync
    cmd_l = [
        'rsync',
        '-azzvi',
        '{}@{}:{}/./{{{}}}'.format(
            lidaruser, lidar_ip, lidardata_dir,
            ','.join(syncday_lst)
        ),
        SOLARISMPLDIR.format(lidarname)
    ]
    cmd_subrun = sub.run(cmd_l, stdout=sub.PIPE, stderr=sub.STDOUT)
    print(cmd_subrun.stdout.decode('utf-8'))


# running
if __name__ == '__main__':
    '''
    Pulls the latest data from the lidar laptop
    '''

    # imports
    import datetime as dt
    from ..global_imports.smmpl_opcodes import LIDARIPADDRESS
    from ..global_imports.solaris_opcodes import *

    # mutable params
    lidarname = 'smmpl_E2'

    lidar_ip = LIDARIPADDRESS
    lidaruser = 'mpluser'
    lidardata_dir = f'C:/Users/mpluser/Desktop/{lidarname}'

    # pulling
    today = dt.datetime.today()
    yesterday = today - dt.timedelta(days=1)
    main(
        lidar_ip, lidaruser,
        lidardata_dir,
        lidarname,
        syncday_lst=[
            DATEFMT.format(today),
            DATEFMT.format(yesterday)
        ],
    )
