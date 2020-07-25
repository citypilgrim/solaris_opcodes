# import
import datetime as dt

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from ..globalimports import *
from ...smmpl_opcodes.scanpat_calc.sunforecaster import sunforecaster

# main func
def main(mpld):

    # figure setup
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()           # for plotting angles

    # plotting noise
    mplts_a = mpld['Timestamp'].astype(pd.Timestamp)
    ax1.errorbar(
        mplts_a, mpld['Background Average'],
        yerr=mpld['Background Std Dev'],
        color='C0', marker='o'
    )

    # plotting angles
    sf = sunforecaster(LATITUDE, LONGITUDE, ELEVATION)
    ts_a = pd.date_range(start=mplts_a[0], end=mplts_a[-1], freq='T')
    ts_a = list(map(lambda x: LOCTIMEFN(x, UTCINFO), ts_a))
    thetas_a, phis_a = sf.get_anglesvec(ts_a)
    dir_a = np.stack([
        mpld['Azimuth Angle'], mpld['Elevation Angle']
    ], axis=1)
    mpltheta_a, mplphi_a = LIDAR2SPHEREFN(dir_a, np.deg2rad(ANGOFFSET))
    mpltheta_a, mplphi_a = np.rad2deg(mpltheta_a), np.rad2deg(mplphi_a)
    thetas_a, phis_a = np.rad2deg(thetas_a), np.rad2deg(phis_a)
    phis_a[phis_a>180] -= 360
    phis_a[phis_a<-180] += 360
    ax2.plot(ts_a, thetas_a, color='C1')
    ax2.plot(mplts_a, mpltheta_a, marker='x', linestyle='', color='C1')
    ax2.plot(ts_a, phis_a, color='C2')
    ax2.plot(mplts_a, mplphi_a, marker='x', linestyle='', color='C2')


    plt.show()


# running
if __name__ == '__main__':
    import datetime as dt
    import pandas as pd
    from ..file_readwrite.mpl_reader import smmpl_reader

    starttime = pd.Timestamp('202007210000')
    endtime = pd.Timestamp(dt.datetime.now())

    mpl_d = smmpl_reader(
        'smmpl_E2',
        starttime=starttime,
        endtime=endtime,
    )
    main(mpl_d)
