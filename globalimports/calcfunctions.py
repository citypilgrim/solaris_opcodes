# imports
import datetime as dt

import numpy as np
import pandas as pd


# functions

def SPHERE2LIDARFN(theta_ara, phi_ara, angoffset):
    '''
    Converts spherical coordinates to lidar coordinates (bearing convention)

    Parameters
        theta_ara (np.array or float): [rad]
        phi_ara (np.array or float): [rad]
        angoffset (float): [rad]

    Return
        ret (np.array): [rad] lidar init points with offset
                        (N x N x np.prod(...) x no. grids, 2(phi, ele))
    '''
    if theta_ara.shape == ():   # convert scalar to array
        theta_ara = np.array([theta_ara])
        phi_ara = np.array([phi_ara])
    else:
        theta_ara = np.array(theta_ara)
        phi_ara = np.array(phi_ara)

    # converting right hand coord convention to bearing convention
    phil_ara = -phi_ara

    # applying angular offset
    phil_ara -= angoffset  # [-pi, pi] -> [-2pi, 0] or [0, 2pi]
    ## shifting phil_ara back to [-pi, pi] for compatibiility with lidar
    phil_ara[phil_ara < -np.pi] += 2*np.pi
    phil_ara[phil_ara > np.pi] -= 2*np.pi

    # convert lidar zenith angle to elevation
    ele_ara = np.pi/2 - theta_ara

    ret = np.stack((phil_ara, ele_ara), axis=1)

    return ret


def LIDAR2SPHEREFN(dir_ara, angoffset):
    '''
    Converts lidar coordinates(bearing convention) to spherical coordinates,
    removing the angular offset

    Parameters
        dir_ara (np.array): [deg, 2dp] lidar init points with offset
                            (N x N x np.prod(...) x no. grids, 2(phi, ele))
        angoffset (float): [rad] angular offset of lidar from north in bearing
                           convention
    Return
        theta_ara (np.array): [rad]
        phi_ara (np.array): [rad]
    '''
    dir_ara = np.deg2rad(dir_ara)
    phil_ara, ele_ara = dir_ara[:, 0], dir_ara[:, 1]

    theta_ara = np.pi/2 - ele_ara

    philpb_ara = phil_ara + angoffset
    phi_ara = -philpb_ara
    phi_ara[phi_ara < -np.pi] += 2*np.pi
    phi_ara[phi_ara > np.pi] -= 2*np.pi

    return theta_ara, phi_ara


def LOCTIMEFN(pdtimestampinput, utcinfo):
    '''
    converts pdtimestampinput into a timezone aware pd.Timestamp object
    will take in whatever input which pd.Timestamp also accepts

    utcinfo is abstracted to allow for future changes
    '''
    ts = pd.Timestamp(pdtimestampinput).tz_localize(
        dt.timezone(dt.timedelta(hours=utcinfo))
    )

    return ts
