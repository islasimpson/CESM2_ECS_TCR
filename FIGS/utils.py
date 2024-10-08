import numpy as np
from scipy.fft import fft, ifft
import xarray as xr
import sys
import logging
logging.basicConfig(level=logging.INFO)

def runningmean(dat, nysm, timeaxis='time', dropna=False):
    """dat = your data with a time axis with name equal to whatever you set "timeaxis" to
       nysm = the number of time values in your running mean
       dropna = False if you don't want to drop the NaN's at the edges
    """

    window_kwargs = {timeaxis:nysm}
    if (dropna):
        datm = dat.rolling(center=True, min_periods=nysm, **window_kwargs).mean(timeaxis).dropna(timeaxis)
    else:
        datm = dat.rolling(center=True, min_periods=nysm, **window_kwargs).mean(timeaxis)
    return datm

def cosweightlonlat(darray,lon1,lon2,lat1,lat2, fliplon=True):
    """Calculate the weighted average for an [:,lat,lon] array over the region
    lon1 to lon2, and lat1 to lat2
    """
    # flip latitudes if they are decreasing
    if (darray.lat[0] > darray.lat[darray.lat.size -1]):
        print("flipping latitudes")
        darray = darray.sortby('lat')

    # flip longitudes if they start at -180
    if (fliplon):
        if (darray.lon[0] < 0):
            print("flipping longitudes")
            darray.coords['lon'] = (darray.coords['lon'] + 360) % 360
            darray = darray.sortby(darray.lon)


    region=darray.sel(lon=slice(lon1,lon2),lat=slice(lat1,lat2))
    weights = np.cos(np.deg2rad(region.lat))
    regionw = region.weighted(weights)
    regionm = regionw.mean(("lon","lat"))

    return regionm

