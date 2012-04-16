import warnings
import os
import numpy as np
import exceptions

import unittest

import healpy as hp

DATAPATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data')

WMAP_MAP_URL = 'http://lambda.gsfc.nasa.gov/data/map/dr4/skymaps/7yr/raw/wmap_band_imap_r9_7yr_W_v4.fits'
WMAP_MASK_URL = 'http://lambda.gsfc.nasa.gov/data/map/dr4/ancillary/masks/wmap_temperature_analysis_mask_r9_7yr_v4.fits'

WMAP_MAP_FILENAME = os.path.join(DATAPATH, os.path.basename(WMAP_MAP_URL))
WMAP_MASK_FILENAME = os.path.join(DATAPATH, os.path.basename(WMAP_MASK_URL))


def download_wmap_maps():
    import urllib
    if not os.path.isfile(WMAP_MAP_FILENAME):
        print 'Downloading %s to %s' % (WMAP_MAP_URL, WMAP_MAP_FILENAME)
        urllib.urlretrieve(WMAP_MAP_URL, filename = WMAP_MAP_FILENAME)
    if not os.path.isfile(WMAP_MASK_FILENAME):
        print 'Downloading %s to %s' % (WMAP_MASK_URL, WMAP_MASK_FILENAME)
        urllib.urlretrieve(WMAP_MASK_URL, filename = WMAP_MASK_FILENAME)
    

class TestSphtFunc(unittest.TestCase):

    def setUp(self):
        try:
            download_wmap_maps()
            self.map = hp.ma(hp.read_map(WMAP_MAP_FILENAME))
            self.mask = hp.read_map(WMAP_MASK_FILENAME).astype(np.bool)
        except exceptions.IOError:
            warnings.warn("""Missing Wmap test maps from the data folder, please download them from Lambda and copy them in the test/data folder:
            http://lambda.gsfc.nasa.gov/data/map/dr4/skymaps/7yr/raw/wmap_band_imap_r9_7yr_W_v4.fits
            http://lambda.gsfc.nasa.gov/data/map/dr4/ancillary/masks/wmap_temperature_analysis_mask_r9_7yr_v4.fits
            on Mac or Linux you can run the bash script get_wmap_maps.sh from the same folder
            """)
            raise
        self.map.mask = np.logical_not(self.mask)
        self.cla = hp.read_cl(os.path.join(DATAPATH, 'cl_wmap_fortran.fits'))
    
    def test_anafast(self):
        cl = hp.anafast(self.map.filled(), lmax = 1024)
        self.assertEqual(len(cl), 1025)
        np.testing.assert_array_almost_equal(cl, self.cla, decimal=8)

    def test_synfast(self):
        m = hp.synfast(self.cla, 1024)

if __name__ == '__main__':
    unittest.main()
