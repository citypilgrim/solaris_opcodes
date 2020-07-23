# imports
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

from ..globalimports import *


# params
_scale = 1.3
_curlyl = 30

_colormap = 'viridis'

# main func
def main(datad, keyofint):
    '''
    Plots out data dictionary on a 3D axis.
    The dictionary has to have the following keys:
        - r_tra/trm
        - theta/phi_ta

    Parameters
        datad (dict): dictionary data
    '''
    # reading data
    key_tra = datad[keyofint]
    r_tra = datad['r_tra']
    r_trm = datad['r_trm']
    theta_ta = datad['theta_ta']
    phi_ta = datad['phi_ta']

    # normalising key_tra for color mapping
    key_tra -= key_tra.min()
    key_tra /= key_tra.max()
    # key_tra = [key_ra/key_ra.max() for key_ra in key_tra]
    key_tra /= 50
    # computing colors and alphas
    key_tra = np.stack([key_tra]*4, axis=-1)
    key_tra[..., 2] = 1
    key_tra[..., 0] = 0
    key_tra[..., 1] = 0

    # computing cartesian coords
    x_tra = r_tra * np.sin(theta_ta)[:, None] * np.cos(phi_ta)[:, None]
    y_tra = r_tra * np.sin(theta_ta)[:, None] * np.sin(phi_ta)[:, None]
    z_tra = r_tra * np.cos(theta_ta)[:, None]

    # figure creation
    fig3d = plt.figure(figsize=(10, 10), constrained_layout=True)
    ax3d = fig3d.add_subplot(111, projection='3d')
    ax3d.pbaspect = [_scale, _scale, _scale]
    ax3d.set_xlabel('South -- North')
    ax3d.set_ylabel('East -- West')
    ax3d.set_xlim([-_curlyl/2, _curlyl/2])
    ax3d.set_ylim([-_curlyl/2, _curlyl/2])
    ax3d.set_zlim([0, _curlyl])
    colormap = plt.get_cmap(_colormap)

    # plotting; iterating timestamps
    for i, r_rm in enumerate(r_trm):
        x_ra = x_tra[i][r_rm]
        y_ra = y_tra[i][r_rm]
        z_ra = z_tra[i][r_rm]
        key_ra = key_tra[i][r_rm]

        ax3d.scatter(
            x_ra, y_ra, z_ra, s=100,
            c=key_ra
        )

    plt.show()


# running
if __name__ == '__main__':
    import pandas as pd
    from ..product_calc.nrb_calc import nrb_calc
    from ..file_readwrite.mpl_reader import smmpl_reader

    nrb_d = nrb_calc(
        'smmpl_E2', smmpl_reader,
        starttime=pd.Timestamp('202007220000'),
        endtime=pd.Timestamp('202007220030'),
        genboo=True
    )
    main(nrb_d, 'NRB2_tra')
