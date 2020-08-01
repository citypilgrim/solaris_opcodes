# imports
import datetime as dt
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from ..file_readwrite.mpl_reader import smmpl_reader
from ..globalimports import *

def main(
        lidarname,
        starttime, endtime,
):
    '''
    Compares the scanpatterns produced with the actual sucessful angles measured
    '''
    # reading scanpatterns
    ## getting list of directories to search
    date_l = list(filter(lambda x: x[0] == '2',
                         os.listdir(SOLARISMPLDIR.format(lidarname))))
    date_l = list(filter(
        lambda x: (
            pd.Timestamp(x) >= dt.datetime.combine(starttime, dt.time())
            and pd.Timestamp(x) <= dt.datetime.combine(endtime, dt.time())
        ), date_l
    ))
    date_l = list(map(lambda x: DIRCONFN(SOLARISMPLDIR.format(lidarname), x), date_l))
    ## reading scanpattern files for angles
    sp_l = FINDFILESFN(SCANPATFILE, date_l)
    sp_l.sort()
    sp_l = list(filter(lambda x:
                    pd.Timestamp(DIRPARSEFN(x, fieldsli=SCANPATSTFIELD)) >= starttime
                    and
                    pd.Timestamp(DIRPARSEFN(x, fieldsli=SCANPATETFIELD)) <= endtime,
                    sp_l
    ))
    spst_l = list(map(DIRPARSEFN(fieldsli=SCANPATSTFIELD), sp_l))
    spet_l = list(map(DIRPARSEFN(fieldsli=SCANPATETFIELD), sp_l))
    spst_l = list(map(pd.Timestamp, spst_l))
    spet_l = list(map(pd.Timestamp, spet_l))

    # comparing each indivdual scan pattern with the scan angles
    for i, sp in enumerate(sp_l):

        # reading files
        spdir_l = np.loadtxt(sp, delimiter=', ').tolist()
        spdir_l = [tuple(spdir) for spdir in spdir_l]
        mpl_d = smmpl_reader(lidarname, starttime=spst_l[i], endtime=spet_l[i]
                             , verbboo=False)
        mpldir_a = np.stack(
            [mpl_d['Azimuth Angle'], mpl_d['Elevation Angle']],
            axis=1
        ).astype(np.float64)    # need to have same precision as python float
                                # for hashing
        mpldir_l = [tuple(np.round(mpldir, 2)) for mpldir in mpldir_a]

        # enumerating scanpat points
        spdir_d = {spdir: i for i, spdir in enumerate(spdir_l)}

        # matching measured angles
        mplind_l = list(map(lambda x: spdir_d[x], mpldir_l))

        # plotting resutls
        print(len(spdir_d.values()))
        plt.plot(list(spdir_d.values()))

        print(len(mplind_l))
        plt.plot(mplind_l)
        break
    plt.show()



if __name__ == '__main__':
    starttime = pd.Timestamp('202007312330')
    endtime = starttime + pd.Timedelta(30, 'm')

    main(
        'smmpl_E2',
        starttime, endtime
    )
