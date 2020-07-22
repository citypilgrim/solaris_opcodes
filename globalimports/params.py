# data
'''
directories seen by python C:/Program Files (x86)/...;  '/' or '\\' is allowed
directories seen by gitbash, i.e. os.system C:/Program\ Files\ \(x86\)/...
                                         or 'C:/Program Files (x86)/...'
directories seen by rsync in os.system /c/Program\ Files\ \(x86\)/...
'''
## on solaris server
SOLARISIP = '137.132.39.187'
SOLARISUSER = 'tianli'
SOLARISHOMEDIR = '/home/tianli/SOLAR_EMA_project'

SOLARISCODESDIR = SOLARISHOMEDIR + '/codes/solaris_opcodes'

SOLARISDATADIR = SOLARISHOMEDIR + '/data'
SOLARISMPLDIR = SOLARISDATADIR + '/{}'  # lidarname
SOLARISMPLCALIDIR = SOLARISMPLDIR + '/calibration'
SOLARISRAZONDATADIR = SOLARISDATADIR + '/razon_E2'

## data nomenclature; indices to change manually when fmts are adjusted
DATEFMT, TIMEFMT = '{:%Y%m%d}', '{:%Y%m%d%H%M}'  # must be compatible for pandas
SCANPATFILE = TIMEFMT + '_' + TIMEFMT + '_scanpat.txt'
MPLTIMEFIELD = 0
MPLFILE = TIMEFMT + '.mpl'
MPLEOMTIMEFIELD = 0
MPLEOMFILE = TIMEFMT + '_eom.flag'  # indicates end of measurement
MPLLOGFILE = TIMEFMT + 'MPLLog.txt'
MPLLOGCURFILE = 'mplLog.txt'
OVERLAPTIMEFIELD, OVERLAPBINTIMEFIELD = 0, 1
# OVERLAPFILE = TIMEFMT + '_{}_overlap.mpl' # bintime
OVERLAPFILE = TIMEFMT + '_{}_overlap.csv'  # bintime
AFTERPULSETIMEFIELD, AFTERPULSEBINTIMEFIELD = 0, 1
# AFTERPULSEFILE = TIMEFMT + '_{}_afterpulse.mpl'
AFTERPULSEFILE = TIMEFMT + '_{}_afterpulse.csv'
DEADCOUNTTIMEFIELD, DEADCOUNTBINTIMEFIELD = 0, 1
DEADCOUNTFILE = TIMEFMT + '_{}_deadcount.mpl'
DEADTIMESNFIELD = 0
DEADTIMEFILE = '{}_deadtime.txt'  # s/n of detector head

# scripting; __main__


# ara_calc
ANGOFFSET = 141                 # [deg]


# product_calc

## common constants nomenclature
BINTIMEFMT, BINNUMFMT = '{:.2e}', '{:.0f}'

## nrb_calc
NRBSTIMEFIELD, NRBETIMEFIELD = 0, 1
NRBDIR = TIMEFMT + '_' + TIMEFMT + '_{}_NRB.txt'  # start, end, array shape
BLINDRANGE = 0.3                # [km], lidar blind for starting distance
DELEOVERE = 0.01  # ~1% for averaging time <= 1 min,
                  # also in cali_profiles.afterpulse_gen

## cloud_calc.gcdm
NOISEALTITUDE = 2
KEMPIRICAL = 500                # good to find algorithm for this

## constant_profiles.rayleigh
CONSTPROFILESDIR = SOLARISCODESDIR + '/product_calc/constant_profiles'
RAYLEIGHPROFILEDIR = CONSTPROFILESDIR + '/rayleigh_gen/profiles'
RAYLEIGHCDLAMBDA = 523  # [nm]
RAYLEIGHCDFDIR = 'rayfil-{}_sing.cdf'  # wavelength
WAVELENGTH = 532  # [nm]
WEATHER = 'summer'  # either 'summer' or 'winter'
RAYWEATHERFIELD, RAYWAVELENGTHFIELD, RAYBINTIMEFIELD, RAYBINNUMFIELD = 0, 1, 2, 3
RAYLEIGHPROFILE = '{}_{}_'+BINTIMEFMT+'_'+BINNUMFMT+'_rayleigh.txt'  # weather,
                                                                     # wavelength

## cali_profiles
CALIPROFILESDIR = SOLARISCODESDIR + '/product_calc/cali_profiles/profiles'
CALIWRITESIGFIG = 7
AFTPROTIMEFIELD, AFTPROBINTIMEFIELD, AFTPROBINNUMFIELD = 0, 1, 2
AFTERPULSEPROFILE = '_'.join([TIMEFMT, BINTIMEFMT, BINNUMFMT]) \
    + '_{}_afterpulse.txt'       # lidarname
OVERPROTIMEFIELD, OVERPROBINTIMEFIELD, OVERPROBINNUMFIELD = 0, 1, 2
OVERLAPPROFILE = '_'.join([TIMEFMT, BINTIMEFMT, BINNUMFMT]) \
    + '_{}_overlap.txt'          # lidarname
DTSNFIELD, DTLIDARNAMEFIELD = 0, 1
DEADTIMEPROFILE = '{}_{}_deadtime.txt'  # s/n of detector head, lidarname
SPEEDOFLIGHT = 299792.45737195015  # [km s^-1]

### cali_profiles.afterpulse_*gen
SAVGOLWINDOWLEN = 151  # has to be odd number
SAVGOLPOLYORDER = 2
SAVGOLRANGETHRES = 4  # [km]
SAVGOLDIFFTHRES = 10e-8         # might be a bit too liberal
AFTERPULSEPROFSTART = 0
AFTERPULSEPROFEND = None

AFTERPULSEUNCERTSCALE = 1.5e-1
AFTERPULSECSVHEADER = 1

### cali_profiles.overlap_*gen
OVERLAPSTARTTHRES = 2.548  # [km]
OVERLAPENDTHRES = 5.5  # [km]
OVERLAPPROFSTART = 0
OVERLAPPROFEND = None
OVERLAPSMALLVALUE = 1e-50

OVERLAPUNCERTSCALE = 6e-2       # 6e-1
OVERLAPCSVHEADER = 0

### cali_profiles.darkcount_*gen
DARKCOUNTPROFSTART = 0
DARKCOUNTPROFEND = None
