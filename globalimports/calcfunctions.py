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


def LOCTIMEFN(tsinput=None, utcinfo=None):
    '''
    converts tsinput into a timezone aware datetime like object
    preserving the datetime object type which was used for the input

    utcinfo is abstracted to allow for future changes
    '''
    tstype = type(tsinput)
    if tstype in [list, np.ndarray]:
        return np.vectorize(LOCTIMEFN(utcinfo=utcinfo))(tsinput)

    elif isinstance(tsinput, type(None)):
        return lambda x: LOCTIMEFN(x, utcinfo)

    else:
        tz = dt.timezone(dt.timedelta(hours=utcinfo))

        if tstype in [pd.Timestamp, pd.DatetimeIndex]:
            try:
                return tsinput.tz_localize(tz)
            except TypeError:   # setting the UTC of already tz aware timestamps
                return tsinput.tz_convert(tz)
        elif tstype == dt.datetime:
            return tsinput.replace(tzinfo=tz)
        elif tstype == np.datetime64:
            return LOCTIMEFN(tsinput.astype(dt.datetime), utcinfo)

        else:
            raise TypeError('tsinput is not a specified type')
