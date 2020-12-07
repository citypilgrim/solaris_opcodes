# imports
import datetime as dt
import subprocess as sub

from ...global_imports.solaris_opcodes import *



# main func
@verbose
@announcer
def main(
        lidar_ip, lidaruser,
        lidardata_dir,
        syncday_lst=None
):
    '''
    pulls the data from the lidar laptop.
    By default syncs current day and previous day's data.

    Parameters
        lidar_ip (str): IP address of the lidar laptop
        lidaruser (str): username of the lidar laptop
        lidardata_dir (str): directory containing all the date directories
                             that contain the lidar data
        syncday_lst (lst): list objects are strings of the format DATEFMT
    '''
    if not syncday_lst:           # normal operations transfer
        today = dt.datetime.now()    # getting timings; sync today and yesterday
        syncday_lst = [
            DATEFMT.format(today),
            DATEFMT.format(today - dt.timedelta(1))
        ]

    # rsync
    cmd_l = [
        'rsync',
        '-azzvi',
        # f"-e ssh -o 'StrictHostKeyChecking=no' -i '{IDRSADIR}'",
        '{}@{}:{}/./{{{}}}'.format(
            lidaruser, lidar_ip, lidardata_dir,
            ','.join(syncday_lst)
        ),
        SOLARISMPLDATADIR
    ]
    cmd_subrun = sub.run(cmd_l, stdout=sub.PIPE, stderr=sub.STDOUT)
    print(cmd_subrun.stdout.decode('utf-8'))


# running
if __name__ == '__main__':
    '''
    Test out the transfer without the need for using ssh
    '''
    main()
