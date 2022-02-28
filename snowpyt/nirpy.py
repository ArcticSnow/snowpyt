'''
See the paper by Matzl and Schneebeli 2016 for more info

A calibration profile was derived from the camera with Micmac. This calibration profile is for correcting vigneting.
correct image for vignetting (calib profile is of the size of Raw images. Crop from center to use with jpegs
detrend if needed the luminosity, as it can vary linearly from top to bottom of the snowpit
sample targets for absolute reflectance calibration (white= 99%, and grey=50%). Fit a linear model
Convert reflectance image to SSA with the conversion equation  𝑆𝑆𝐴=𝐴𝑒𝑟/𝑡

Finally, use the ruler (or other object of know size) in image to scale image dimension to metric system.
TODO:

write functions for all steps
wrap all in a python package/class
write function to extract profiles, and maybe later identify layers using reflectance/SSA, and contrast enhanced image
write function to extract SSA profile to import in niviz.org
include class to compute
Raw images are in 12 bit. Find a way to convert to BW from original while maintaining the 12bit resolution. Rawpy might be useful. Then make sure the processing pipeline can accept 12bit data (i.e. all skimage functions)
wrap micmac function to extract profile 'mm3d vodka'. At least provide the method on how to do it.

'''

from skimage import io, color
import matplotlib.pyplot as plt
from mpl_point_clicker import clicker
import numpy as np

class micmac_nir():
    '''
    Class to correct images via micmac. with mm3d vodka
    '''



class nir(object):
    def __init__(self, fname_nir, fname_calib):
        self.fname_nir = fname_nir
        self.fname_calib = fname_calib
        self.img_rgb = None
        self.img_v = None
        self.img_calib = None
        self.calib_profile = None
        self.targets = []
        self.img_reflectance = None

        self.load_nir()
        if fname_calib is not None:
            self.load_calib()
            self.apply_calib()
        else:
            print("---> WARNING: No calbration profile provided.")


    def pick_targets(self, reflectances=[99, 50]):

        def pick_target(image_calib, target_reflectance=99):
            """
            Function to pick values of targets of a given reflectance
            Args:
                image_calib (array):
                target_reflectance (int): absolute reflectance of target type

            Returns:
                dict: data for one type of targets
            """
            fig, ax = plt.subplots(constrained_layout=True)
            ax.imshow(image_calib, cmap=plt.cm.gray)
            klicker = clicker(ax, ["event"], markers=["x"])
            plt.show()

            coords = klicker.get_positions().get('event').astype(int)
            vals = image_calib[coords[:,1], coords[:,0]]
            val_mean = np.mean(vals)

            target = {'coords': coords,
                         'values':vals,
                         'mean_values':val_mean,
                         'reflectance': target_reflectance}
            return target

        self.targets = []
        for refl in reflectances:
            print("---> Pick {}% reflectance targets".format(refl))
            self.targets.append(pick_target(self.img_calib, target_reflectance=refl))
        print('DONE: Reflectance targets picked.')

    def convert_to_reflectance(self):
        values = []
        reflectances = []

        for ref in self.targets:
            values.append(ref.get('values'))
            reflectances.append(ref.get('values') * 0 + ref.get('reflectance'))
        values = np.array(values).flatten()
        reflectances = np.array(reflectances).flatten()

        A = np.vstack([values, np.ones(len(values))]).T
        m, c = np.linalg.lstsq(A, reflectances, rcond=None)[0]

        self.img_reflectance = self.img_calib * m + c

    def convert_to_SSA(self):
        self.img_ssa = 0.017 * np.exp(self.img_reflectance/12.222)

    def convert_to_doptic(self):
        self.img_doptic = 6/self.img_ssa

    def load_calib(self):
        self.calib_profile = io.imread(self.fname_calib).T

    def apply_calib(self,  crop_calib=False):
        if (self.calib_profile.shape != self.img_v) or (crop_calib):
        # Crop calib profile, using center of matrix as cropping reference
            def crop_center(img,crop_shape):
                y,x = img.shape
                startx = x//2 - crop_shape[1]//2
                starty = y//2 - crop_shape[0]//2
                return img[starty:starty+crop_shape[0], startx:startx+crop_shape[1]]
            self.calib_profile = crop_center(self.calib_profile, self.img_v.shape)

        means = np.mean(self.img_v * self.calib_profile, axis=1)
        trend = np.polyfit(np.arange(0,means.shape[0]),means,1)
        trendpoly = np.poly1d(trend)
        self.img_calib = self.img_v * self.calib_profile - np.repeat(trendpoly(np.arange(0,means.shape[0])),
                                                                     self.img_v.shape[1], axis=0).reshape(self.img_v.shape)


    def load_nir(self):
        '''
        function to load jpeg NIR images, and convert them to BW
        '''
        self.img_rgb = io.imread(self.fname_nir)
        self.img_v = color.rgb2hsv(self.img_rgb)[:,:,2]


    def load_array(self):
        '''
        Function to data if saved in a 2D array format.
        '''
        return

    def read_exif(self):
        '''
        function to read image exif
        :return:
        '''
        return

    def apply_vignetting(self):
        '''
        Apply via Python the
        :return:
        '''

    def detrend_limunosity_gradient(self):
        '''
        Function to detrend the luminosity gradient (vertical and/or horizontal)
        :return:
        '''

    def extract_profile(self):
        '''function to extract profile
        1. one single pixel profile
        2. multiple profile, and return aggregate profile (mean, median, min, max, std)
        '''
        return

    def calibrate_targets(self):
        '''
        Function to derive reflectance calibration value from targets (50% and 90%)
        :return:
        '''
        return

    def apply_calibration(self):
        '''
        apply reflectance calibration from targets
        :return:
        '''
        return

    def ref2ssa(self):
        '''
        function to compute SSA from reflectance value
        :return:
        '''
        return

    def ssa2d(self):
        '''
        function to derive optical diameter of grain from SSA values
        :return:
        '''
        return

        def plot_compare(self, im1, im2, cm=plt.cm.gray):
        """
        Function to compare two images
        :param im1:
        :param im2:
        :param cm:
        :return:
        """