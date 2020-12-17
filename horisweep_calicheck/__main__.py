# imports
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
from pymap3d import ned2geodetic, geodetic2ned


# params
_D = 3000
_delr = 15
_nrbthres = 5

_psinum = 10                  # number of points for uncertainty in azimuth plot


# main func
def main(
        lidar_lat, lidar_lg, lidar_h,
        delphib,
        cadastraldir,
        *nrbds
):
    '''
    Follow these steps to perform azimuthal calibration of the lidar
    1. Use .geojson_trimmer to create a suitable sized geojson file for plotting
    2. specify the data set used for calibration check

    Plots out the horizontal sweep of the nrb against the cadastral map
    the geojson can be created and trimmed in /.cadastral_trimmer.

    Note that the coordinates provided by nrb_calc are in spherical coordinates,
    which map x->N, y->W.
    But here we plot on a 2D-plane, which maps y->N(latitude), x->E(longitude).
    This is taken care in the coordinate transform of the azimuthal array from
    nrb_calc. which converts phi to psi, which is the angle starting from the E axis,
    aka the longitude axis

    Parameters
        lidar_lat (float): [deg] lidar latitude
        lidar_lg (float): [deg] lidar longitude
        lidar_h (float): [m] lidar heigh above geodetic ellipsoid
        delphib (float): [rad] uncert of phib
        cadastraldir (str): directory of cadastral geojson
        nrbds (list): list of output from product_calc.nrb_calc
    '''
    # reading files
    sg_df = gpd.read_file(cadastraldir)

    # plot creation
    fig, ax = plt.subplots()

    ## plotting map
    sg_df.plot(ax=ax)

    # computing coordinates
    for i, nrbd in enumerate(nrbds):
        color = f'C{i+1}'
        if i == 0:
            markeralpha = 1  # darker color for reference marker
            markercolor = 'k'
        else:
            markeralpha = 0.3
            markercolor = color

        NRB_tra = nrbd['NRB_tra']
        r_tra = nrbd['r_tra'] * 1000
        r_trm = nrbd['r_trm']
        phi_ta = nrbd['phi_ta']
        psi_ta = nrbd['phi_ta'] + np.pi/2       # psi is the angle inthe 2D projection
                                                # anti clockwise from E(longitude) axis

        # scan lines; coverting local NE to lat long, referenced from the lidar
        # coordinates
        print('computing lidar point')
        point1lat_ta = lidar_lat*np.ones_like(psi_ta)
        point1lg_ta = lidar_lg*np.ones_like(psi_ta)
        point1n_ta, point1e_ta, point1d_ta = geodetic2ned(
            point1lat_ta, point1lg_ta, lidar_h,
            lidar_lat, lidar_lg, lidar_h
        )

        print('computing scan points')
        point2n_ta = point1n_ta + _D*np.sin(psi_ta)
        point2e_ta = point1e_ta + _D*np.cos(psi_ta)
        point2lat_ta, point2lg_ta, _ = ned2geodetic(
            point2n_ta, point2e_ta, point1d_ta,
            lidar_lat, lidar_lg, lidar_h,
        )

        # threshold for nrb
        r_trm *= NRB_tra > _nrbthres

        # range (time, bins)
        print('computing range points')
        rn_tra = point1n_ta[:, None] + r_tra * np.sin(psi_ta)[:, None]
        re_tra = point1e_ta[:, None] + r_tra * np.cos(psi_ta)[:, None]
        rlat_tra, rlg_tra, _ = ned2geodetic(
            rn_tra, re_tra, point1d_ta[:, None],
            lidar_lat, lidar_lg, lidar_h,
        )

        # error bars

        ## errorbar for range; (time, bins, 2(lower limit, upper limit))
        print('computing range error bar')
        deln_ta = _delr/2 * np.sin(psi_ta)
        dele_ta = _delr/2 * np.cos(psi_ta)
        delrn_tr2a = np.stack([
            rn_tra - deln_ta[:, None], rn_tra + deln_ta[:, None]
        ], axis=2)
        delre_tr2a = np.stack([
            re_tra - dele_ta[:, None], re_tra + dele_ta[:, None]
        ], axis=2)
        delrlat_tr2a, delrlg_tr2a, _ = ned2geodetic(
            delrn_tr2a, delre_tr2a, point1d_ta[:, None, None],
            lidar_lat, lidar_lg, lidar_h,
        )

        ## error bar for azimuth; (time, bins, _psinum), 'n' represents _psinum
        print('computing azimuthal error bar')
        delpsi_na = np.linspace(-delphib, delphib, _psinum)
        delpsi_tna = psi_ta[:, None] + delpsi_na
        delpsin_trna = point1n_ta[:, None, None] + r_tra[:, :, None] * \
            np.sin(delpsi_tna)[:, None, :]
        delpsie_trna = point1e_ta[:, None, None] + r_tra[:, :, None] * \
            np.sin(delpsi_tna)[:, None, :]
        delpsilat_trna, delpsilg_trna, _ = ned2geodetic(
            delpsin_trna, delpsie_trna, point1d_ta[:, None, None],
            lidar_lat, lidar_lg, lidar_h
        )

        # plotting

        ## lidar
        ax.plot(lidar_lg, lidar_lat, 'ko')

        ## plotting threshold nrb
        for j in range(len(phi_ta)):  # indexing time

            # scan lines
            ax.plot(
                [point1lg_ta[j], point2lg_ta[j]],
                [point1lat_ta[j], point2lat_ta[j]],
                '-', alpha=0.3, color=color
            )

            # nrb threshold points
            r_rm = r_trm[j]             # (bins)
            ax.plot(
                rlg_tra[j][r_rm], rlat_tra[j][r_rm],
                'o', color=markercolor, alpha=markeralpha
            )

            # plotting error bars
            for k in range(np.sum(r_rm)):

                # plotting range error bars
                delr_r2m = np.stack([r_rm]*2, axis=1)
                ax.plot(
                    delrlg_tr2a[j][delr_r2m][k],
                    delrlat_tr2a[j][delr_r2m][k],
                    '-', color='k'
                )

                # plotting azimuth error bars
                delpsi_r2m = np.stack([r_rm]*_psinum, axis=1)
                ax.plot(
                    delpsilg_trna[j][delpsi_r2m][k],
                    delpsilat_trna[j][delpsi_r2m][k],
                    '-', color='k'
                )

    # showing
    plt.xlabel('Long [deg]')
    plt.ylabel('Lat [deg]')
    plt.show()


# running
if __name__ == '__main__':
    # imports
    from ..file_readwrite import smmpl_reader
    from ..product_calc.nrb_calc import main as nrb_calc
    from ..global_imports.solaris_opcodes import *

    phib = 141.6

    nrbd_l = []
    # nrbd_l.append(nrb_calc(
    #     'smmpl_E2', smmpl_reader,
    #     starttime=LOCTIMEFN('202003040341', 0),
    #     endtime=LOCTIMEFN('202003040900', 0),
    #     angularoffset=phib
    # ))
    # nrbd_l.append(nrb_calc(
    #     'smmpl_E2', smmpl_reader,
    #     starttime=LOCTIMEFN('202008280250', 0),
    #     endtime=LOCTIMEFN('202008280350', 0),
    #     angularoffset=phib
    # ))
    nrbd_l.append(nrb_calc(
        'smmpl_E2', smmpl_reader,
        starttime=LOCTIMEFN('202009132007', 0),
        endtime=LOCTIMEFN('202009132113', 0),
        angularoffset=phib
    ))

    lidar_lat, lidar_lg = 1.299119, 103.771232  # [deg], at E2
    lidar_h = 70
    delphib = np.deg2rad(0.4)
    cadastral_dir = '/home/tianli/SOLAR_EMA_project/codes/smmpl_codes/horisweep_plot/cadastral_trimmer/cadastral_AOI.geojson'

    main(
        lidar_lat, lidar_lg, lidar_h,
        delphib,
        cadastral_dir,
        *nrbd_l
    )
