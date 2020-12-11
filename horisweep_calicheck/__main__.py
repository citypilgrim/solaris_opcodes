# imports
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pymap3d import ned2geodetic, geodetic2ned

from .latlg2ne import svy21
from . import scan2ara as s2a
from . import scan_event as se


# params
_D = 3000
_delr = 15
_nrbthres = 5

_phibanum = 10                  # number of points for phib plot


# sup func
def _rangetup_func(lidarNEa, rtra, phita, survey21):
    rangen_ara = lidarNEa[0] + np.cos(phita)[..., None] * rtra # (phi, bins)
    rangee_ara = lidarNEa[1] + np.sin(phita)[..., None] * rtra
    rangeltlg_tup = survey21.computeLatLon(rangen_ara, rangee_ara)
    return rangeltlg_tup


# main func
def main(
        lidarNEa, phib, delphib,
        cadastraldir,
        *nrbds
):
    '''
    Follow these steps to perform azimuthal calibration of the lidar
    1. Use .geojson_trimmer to create a suitable sized geojson file for plotting
    2. specify the data set used for calibration check

    Plots out the horizontal sweep of the nrb against the cadastral map
    the geojson can be created and trimmed in /.cadastral_trimmer

    Parameters
        lidarNEa (array like): Northing and easting of lidar
        phib (float): [rad] bearing offset of lidar
        delphib (float): [rad] uncert of phib
        cadastraldir (str): directory of cadastral geojson
        nrbds (list): list of output from product_calc.nrb_calc
    '''
    # init NE to latlong converter
    survey21 = svy21.SVY21()        # converts NE to lat long
    lidarltlg_a = survey21.computeLatLon(*lidarNEa)

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
        phi_ta = -nrbd['phi_ta'] - phib  # inversion of coordinates from nrb_calc

        # scan lines
        point1ne_lst = [lidarNE_a[0]*np.ones_like(phi_ta), # (phi, 2)
                        lidarNE_a[1]*np.ones_like(phi_ta)]
        _D = 4000
        point2ne_lst = [point1ne_lst[0] + _D*np.cos(phi_ta),
                        point1ne_lst[1] + _D*np.sin(phi_ta)]
        pointn_ara = np.stack([point1ne_lst[0], point2ne_lst[0]], axis=1) # (phi, 2)
        pointe_ara = np.stack([point1ne_lst[1], point2ne_lst[1]], axis=1)
        pointltlg_tup = survey21.computeLatLon(pointn_ara, pointe_ara) # (lt_ta, lg_ta)

        # thresholding nrb
        r_trm *= NRB_tra > _nrbthres
        rangen_ara = lidarNE_a[0] + np.cos(phi_ta)[..., None] * r_tra # (phi, bins)
        rangee_ara = lidarNE_a[1] + np.sin(phi_ta)[..., None] * r_tra
        rangeltlg_tup = survey21.computeLatLon(rangen_ara, rangee_ara)

        # errorbar for range
        deln = _delr/2 * np.cos(phi_ta)[..., None] # (phi, 1)
        dele = _delr/2 * np.sin(phi_ta)[..., None]
        errrangen_ara = np.stack([rangen_ara-deln, rangen_ara+deln], axis=2) # (phi, bins, 2)
        errrangee_ara = np.stack([rangee_ara-dele, rangee_ara+dele], axis=2)
        errrangeltlg_tup = survey21.computeLatLon(errrangen_ara, errrangee_ara)

        # error bar for azimuth
        errphirangeltlg_l = [
        _rangetup_func(lidarNE_a, r_tra, phi_ta + dphib, survey21)
        for dphib in np.linspace(-delphib, delphib, _phibanum)
        ]
        errphilt_tr1l = [x[0][..., None] for x in errphirangeltlg_l]
        errphilg_tr1l = [x[1][..., None] for x in errphirangeltlg_l]
        errphilt_trna = np.concatenate(errphilt_tr1l, axis=-1)
        errphilg_trna = np.concatenate(errphilg_tr1l, axis=-1)

        # plotting

        ## lidar
        ax.plot(*lidarltlg_a[::-1], 'ko')

        ## plotting threshold nrb
        for j in range(len(phi_ta)):

            # scan lines
            ax.plot(pointltlg_tup[1][j],  # (2)
                    pointltlg_tup[0][j],
                    '-', alpha=0.3, color=color)

            # nrb threshold points
            r_rm = r_trm[j]             # (bins)
            ax.plot(rangeltlg_tup[1][j][r_rm], # (bins)
                    rangeltlg_tup[0][j][r_rm],
                    'o', color=markercolor, alpha=markeralpha)

            # # azimuth error bars
            # pointnum = np.sum(r_rm)
            # rmind_a = np.where(r_rm)[0]
            # for k in range(pointnum):
            #     ax.plot(
            #         errphilg_trna[k, rmind_a[j], :],
            #         errphilt_trna[k, rmind_a[j], :],
            #         '-', color='k'
            #     )

            # # range error bars
            # copolrangeerr_mask = np.stack([r_rm]*2, axis=1) # (bins, 2)
            # lgerr_tra = errrangeltlg_tup[1][j][copolrangeerr_mask] # (bins>thres * 2)
            # lterr_tra = errrangeltlg_tup[0][j][copolrangeerr_mask]
            # for k in range(0, len(lgerr_tra), 2):
            #     ax.plot(lgerr_tra[k:k+2], lterr_tra[k:k+2],
            #              '-', color='k')


    plt.xlabel('Long [deg]')
    plt.ylabel('Lat [deg]')


    # showing
    plt.show()

# running
if __name__ == '__main__':
    # imports
    import pandas as pd
    from ..file_readwrite import smmpl_reader
    from ..product_calc.nrb_calc import nrb_calc
    from ..global_imports.smmpl_opcodes import *

    nrbd_l = []
    # nrbd_l.append(nrb_calc(
    #     'smmpl_E2', smmpl_reader,
    #     date=pd.Timestamp('20200304'),
    #     starttime=LOCTIMEFN('202003040341', UTCINFO),
    #     endtime=LOCTIMEFN('202003040900', UTCINFO),
    #     genboo=True,
    # ))
    nrbd_l.append(nrb_calc(
        'smmpl_E2', smmpl_reader,
        starttime=LOCTIMEFN('202008280250', UTCINFO),
        endtime=LOCTIMEFN('202008280350', UTCINFO),
        genboo=True,
    ))
    nrbd_l.append(nrb_calc(
        'smmpl_E2', smmpl_reader,
        starttime=LOCTIMEFN('202009132007', UTCINFO),
        endtime=LOCTIMEFN('202009132113', UTCINFO),
        genboo=True,
    ))

    phi_ta = nrbd_l[0]['phi_ta'] + np.deg2rad(ANGOFFSET)
    print(np.rad2deg(phi_ta[0]), np.rad2deg(phi_ta[-1]))
    phi_ta = nrbd_l[1]['phi_ta'] + np.deg2rad(ANGOFFSET)
    print(np.rad2deg(phi_ta[0]), np.rad2deg(phi_ta[-1]))

    lidarNE_a = [31272.71725, 21106.03025]  # at E2
    phib = np.deg2rad(0)
    delphib = np.deg2rad(0.4)
    cadastral_dir = '/home/tianli/SOLAR_EMA_project/codes/smmpl_codes/horisweep_plot/cadastral_trimmer/cadastral_AOI.geojson'

    main(
        lidarNE_a,
        phib, delphib,
        cadastral_dir,
        *nrbd_l
    )
