# imports
import json
import geopandas as gpd
import os
import os.path as osp
import shapely as sh

from ...global_imports.solaris_opcodes import *


# params
_sla_file = 'sla-cadastral-land-parcel-geojson.geojson.gz'


# main func
def main(
        save_file,
        lat_low, lat_high,
        lg_low, lg_high,
):
    '''
    trims the sla-casdastral-land-parcel geojson file

    Parameters
        save_file (str): filename of the trimmed geojsonfile, note that it will save
                         the trimmed file in this directory
        lat/lg_low/high (float): bounding limits of rectangular AOI
    '''

    # directories
    wd = osp.dirname(osp.abspath(__file__))
    sla_file = DIRCONFN(wd, _sla_file)
    save_file = DIRCONFN(wd, save_file)

    # unzipping geojson file
    os.system(f'gzip -d {sla_file}')

    # trimming dataframe
    aoi_lst = [
        [lg_low, lat_low], [lg_low, lat_high],
        [lg_high, lat_high], [lg_high, lat_low]
    ]
    aoi_poly = sh.geometry.Polygon(aoi_lst)

    sla_df = gpd.read_file(sla_file[:-3])
    sla_boo = sla_df['geometry'].apply(aoi_poly.contains)

    trim_df = sla_df[sla_boo]

    # writing trimmed geojson
    trim_gj = {
        'type': 'FeatureCollection',
        "crs": {
            "type": "name",
            "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}
        },
        'features': [{
            'type': 'Feature',
            'properties': {
                'Name': row['Name'],
                'Description':row['Description']
            },
            'geometry': {
                'type': 'Polygon',
                'coordinates': [list(row['geometry'].exterior.coords)]
            }
        } for _, row in trim_df.iterrows()
        ]
    }

    # writing to file
    with open(save_file, 'w') as save_file:
        json.dump(trim_gj, save_file, indent=2)

    # rezipping geojson file
    os.system(f'gzip {sla_file[:-3]}')


if __name__ == '__main__':

    main(
        'testcadastral_AOI.geojson',
        1.298, 1.308,
        103.771080, 103.807,
    )
