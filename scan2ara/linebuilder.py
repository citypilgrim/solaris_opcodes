import numpy as np

from .ncreader import main as ncreader


def arasegextract_func(keyword, araseg):
    '''
    Parameters:
        keyword (str): nc file variable
        araseg (ara): 2d array of data dictionaries
                      0-axis -> scan pattern
                      1-axis -> angular position
    Returns:
        keyaraseg (ara): 2d array of variable value
    '''
    


def main(data_dictara, scanpattern_dir):
    '''
    Extracts the data required from data.json, which is read/written by ncreader

    Parameters:
        data_dictara (ara): array of dictionaries containing data
        scanpattern_dir (str): directory of scanpattern

    Returns:
        built_araara (ara): array of 3d numpy array. 
                          Each 3d array is a single scan sweep
    '''

    
    azi_ara = [dic['azimuth_angle'] for dic in data_dictara]
    ele_ara = [dic['elevation_angle'] for dic in data_dictara]
    ang_ara = np.stack([azi_ara, ele_ara], axis=1)

    # getting azimuth readings from scanpattern
    with open(scanpattern_dir, 'r') as scanpat_file:
        scanpat_ara = np.array(scanpat_file.read().splitlines())
    scanpat_ara = np.char.split(scanpat_ara[::2], sep=',')
    scanpatend_ara = np.array(scanpat_ara[-1]).astype(np.float) # [azi, ele]
    '''
    for now this doesnt work because netcdf averages the azimuth angles, 
    as such the scan pattern endpoint is set manually
    '''
    scanpatend_ara = np.array([-48.07, 0.0])
    
    # segment array
    cutinds_ara = np.argwhere(np.all(ang_ara == scanpatend_ara, axis=1))\
                    .flatten()
    cutinds_ara = np.concatenate(
        (np.array([0]), cutinds_ara, np.array([len(ang_ara)]))
    )
    data_araseg = [data_dictara[cutinds_ara[i]:cutinds_ara[i+1]]\
                   for i in range(len(cutinds_ara)-1)]
    
    # read relevant data
    rangenrb_araseg = arasegextract_func('range_nrb', data_araseg)
    copolnrb_araseg = arasegextract_func('copol_nrb', data_araseg)
    crosspolnrb_araseg = arasegextract_func('crosspol_nrb', data_araseg)


    
    
    
    return None


if __name__ == '__main__':

    import os.path as osp

    datadate = '20200221'
    data_dir = osp.dirname(osp.dirname(osp.dirname(osp.abspath(__file__))))\
        + '/data/{}/'.format(datadate)

    data_dictara = ncreader(data_dir, refreshjson_boo=False)
    scanpattern_dir = data_dir + 'scanpattern_{}.txt'.format(datadate)

    built_araara = main(data_dictara, scanpattern_dir)
    
