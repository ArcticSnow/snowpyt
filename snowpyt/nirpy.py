"""
Collection of NIR processing tools
S. Filhol, March 2022


Inpired by the paper by Matzl and Schneebeli 2016 for more info

A calibration profile was derived from the camera with Micmac. This calibration profile is for correcting vigneting.
correct image for vignetting (calib profile is of the size of Raw images. Crop from center to use with jpegs
detrend if needed the luminosity, as it can vary linearly from top to bottom of the snowpit
sample targets for absolute reflectance calibration (white= 99%, and grey=50%). Fit a linear model
Convert reflectance image to SSA with the conversion equation  𝑆𝑆𝐴=𝐴𝑒𝑟/𝑡

Finally, use the ruler (or other object of know size) in image to scale image dimension to metric system.

TODO:
- write function to extract SSA profile to import in niviz.org
- Raw images are in 12 bit. Find a way to convert to BW from original while maintaining the 12bit resolution. Rawpy might be useful. Then make sure the processing pipeline can accept 12bit data (i.e. all skimage functions)
- wrap micmac function to extract profile 'mm3d vodka'. At least provide the method on how to do it.

"""

from skimage import io, measure, color
import matplotlib.pyplot as plt
from mpl_point_clicker import clicker
import numpy as np
import cv2, scipy
import pandas as pd


def kernel_square(nPix):
    """
    Function to defin a square kernel of equal value for performing averaging
    Args:
        nPix (int): size of the kernel in pixel

    Returns:
        array: kernel matrix

    """
    print("... Averaging kernel of " + str(nPix) + " by " + str(nPix))
    kernel = np.empty([nPix, nPix])
    kernel.fill(1)
    kernel /= kernel.sum()   # kernel should sum to 1!  :)
    return kernel


def smooth(mat, kernel):
    """
    Function that produce a smoothed version of the 2D array
    Args:
        mat: 2D Array to smooth
        kernel: kernel array (output) from the function kernel_square()

    Returns:
        2D array: smoothed array
    """
    r = cv2.filter2D(mat, -1, kernel)
    print("... Smoothing done ...")
    return r


def micmac_radiometric():
    """
    List of commands to run for deriving a radiometric calibratino profile for the camera
    """

    cmd1 = "mm3d Tapioca All .*JPG 2500"
    cmd2 = "mm3d Vodka .*JPG"


class nir(object):
    """
    Class to process NIR snowpit photograph.
    """
    def __init__(self, fname_nir, fname_calib, highpass=True, kernel_size=2000, rotate_calib=False):
        """
        Class initialization
        Args:
            fname_nir (str): path to NIR image
            fname_calib (str): path to radiometric calibration image
            highpass (bool): perform high pass filtering to remove luminosity gradient across the pit
            kernel_size (int): size of the kernel for the highpass filter
        """

        self.fname_nir = fname_nir
        self.fname_calib = fname_calib
        self.rotate_calib = rotate_calib
        self.img_rgb = None
        self.img_bw = None
        self.img_calib = None
        self.calib_profile = None
        self.highpass = highpass
        self.kernel_size = kernel_size
        self.targets = []
        self.spatial_param = None
        self.img_reflectance = None
        self.img_ssa = None
        self.img_doptic = None
        self.profile = None

        self.load_nir()
        if fname_calib is not None:
            self.load_calib()
            self.apply_calib()
        else:
            self.apply_calib()
            print("---> WARNING: No calbration profile provided.")


    def pick_targets(self, reflectances=[99, 50]):
        """
        Function to pick reflectance targets
        Args:
            reflectances (list of int): List of reflectance targets to pick
        """

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
            ax.set_title('Pick targets')
            ax.imshow(image_calib, cmap=plt.cm.gray)
            klicker = clicker(ax, ["event"], markers=["x"], colors='r')
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
        """
        Function to convert image to reflectance using at minimum 2 sets of reflectance targets previously picked
        """
        print('---> convert to reflectance')
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
        """
        Function to convert reflectance to SSA
        """
        if self.img_reflectance is None:
            print('ERROR convert to Reflectance first')
        else:
            print('---> convert to SSA')
        self.img_ssa = 0.017 * np.exp(self.img_reflectance/12.222)

    def convert_to_doptic(self):
        """
        Function to convert SSA to optical diameter
        """
        if self.img_ssa is None:
            print('ERROR convert to SSA first')
        else:
            print('---> convert to optical diameter')
            self.img_doptic = 6/self.img_ssa

    def convert_all(self):
        """
        Function to convert pixel values to physical values using the targets
        """
        self.convert_to_reflectance()
        self.convert_to_SSA()
        self.convert_to_doptic()
        
    def load_calib(self):
        """
        Function to load radiometrci calibration file
        """
        self.calib_profile = io.imread(self.fname_calib)
        if self.rotate_calib:
            self.calib_profile = self.calib_profile.T

    def apply_calib(self,  crop_calib=False):
        """
        Function to apply calibration profile to the NIR image.
        Args:
            crop_calib (bool): if calibration and image are of slightly different size, crop calib and align the two with center.
        """
        # remove noise with median filter
        print('---> Apply median filter for noise reduction')
        self.img_bw = cv2.medianBlur(self.img_bw, 5)

        # apply radiometric calibration
        if self.fname_calib is not None:
            if (self.calib_profile.shape != self.img_bw) or (crop_calib):
                # Crop calib profile, using center of matrix as cropping reference
                def crop_center(img, crop_shape):
                    y,x = img.shape
                    startx = x//2 - crop_shape[1]//2
                    starty = y//2 - crop_shape[0]//2
                    return img[starty:starty+crop_shape[0], startx:startx+crop_shape[1]]
                self.calib_profile = crop_center(self.calib_profile, self.img_bw.shape)
            print('---> Apply radiometric calibration')
            self.img_calib = self.img_bw * self.calib_profile
        else:
            print("---> WARNING: No radiometric calibration applied")
            self.img_calib = self.img_bw

        # Apply a high pass filter
        if self.highpass:
            print('---> Apply high pass filter')
            lowpass = smooth(self.img_calib/255, kernel_square(self.kernel_size))
            self.img_calib = self.img_calib/255 - lowpass


    def load_nir(self):
        """
        Function to load jpeg NIR images, and convert them to BW
        """
        self.img_rgb = cv2.imread(self.fname_nir)
        self.img_bw = cv2.cvtColor(self.img_rgb, cv2.COLOR_BGR2HSV)[:,:,2]
        
    def scale_spatially(self):
        """
        Function to bring real spatial coordinate

        Method:
            1. click two points
            2. provide corresponding length
            3. option to provide geometrical correction
        """
        # Pick two points with a known distance
        print('---> Pick two points with known distance')
        fig, ax = plt.subplots(constrained_layout=True)
        ax.set_title('Pick 2 points with known distance [2 pts]')
        ax.imshow(self.img_calib, cmap=plt.cm.gray)
        klicker = clicker(ax, ["event"], markers=["x"], **{"linestyle": "--"}, colors='r')
        plt.show()
        coords = klicker.get_positions().get('event').astype(int)

        # provide corresponding distance
        dist = float(input('Enter distance in [cm]: '))
        scale = dist / np.linalg.norm(coords[0] - coords[1])

        # pick origin point for coordinate system
        print('---> Pick coordinate system origin)')
        fig, ax = plt.subplots(constrained_layout=True)
        ax.set_title('Pick coordinate system origin [1 pt]')
        ax.imshow(self.img_calib, cmap=plt.cm.gray)
        klicker = clicker(ax, ["event"], markers=["o"],  colors='r')
        plt.show()

        coord = klicker.get_positions().get('event').astype(int)
        extent = np.array([-coord[0][0], self.img_bw.shape[1] - coord[0][0],  coord[0][1] - self.img_bw.shape[0], coord[0][1]])
        self.spatial_param = {'scale': scale, 'extent': extent*scale}


    def extract_profile(self, imgs=['SSA', 'reflectance', 'd_optical'], param={'method': scipy, 'n_samples':1000}):
        """
        Function to extract profile of values for a list of images

        Args:
            imgs (list): images from which to sample profile
            param (dict):
                method (str): method to sample the profile. Avail: numpy, scipy, and skimage.
                n_sample (int, numpy and scipy method): number of samples along profile
                linewidth (int, skimage method): width of the profile
                reduce_func (func, skimage method): function to agglomerate the pixels perpendicular to the line
                spline_order (int, 0-5, skimage method): order of the spline applied to the sampled profile

                examples:
                    {'method': scipy, 'n_samples':1000},
                    {'method': numpy, 'n_samples':1000},
                    {'method': skimage, 'linewidth':5, 'reduce_func':np.median, 'spline_order':1}

        """
        img_dict = {'reflectance': self.img_reflectance,
                    'SSA': self.img_ssa,
                    'd_optical': self.img_doptic,
                    'value_ori': self.img_bw,
                    'value_calib': self.img_calib}

        print('---> Pick segement along which extracting profile')
        fig, ax = plt.subplots(constrained_layout=True)
        ax.set_title('Pick segement along which extracting profile [2 pts]')
        ax.imshow(self.img_reflectance, cmap=plt.cm.gray)
        klicker = clicker(ax, ["event"], markers=["x"], **{"linestyle": "--"}, colors='r')
        plt.show()

        coord = klicker.get_positions().get('event').astype(int)

        self.profile = pd.DataFrame()
        if param.get('method') == 'scipy':
            x, y = np.linspace(coord[0][0], coord[1][0], n_samples), np.linspace(coord[0][1], coord[1][1], n_samples)
            for img in imgs:
                print('... sampling from {}'.format(img))
                self.profile[img] = scipy.ndimage.map_coordinates(img_dict.get(img), np.vstack((y,x)))
            self.profile['x_pix'] = x
            self.profile['y_pix'] = y
            self.profile['dist_pix'] = np.sqrt((x[0] - x)**2 + (y[0] - y)**2)
            self.profile['dist'] = self.profile.dist_pix * self.spatial_param.get('scale')
            self.profile['x'] = self.profile.x_pix * self.spatial_param.get('scale') + self.spatial_param.get('extent')[0]
            self.profile['y'] = self.profile.y_pix * self.spatial_param.get('scale') + self.spatial_param.get('extent')[2]

        elif param.get('method') == 'numpy':
            x, y = np.linspace(coord[0][0], coord[1][0], n_samples), np.linspace(coord[0][1], coord[1][1], n_samples)
            for img in imgs:
                print('... sampling from {}'.format(img))
                self.profile[img] = img_dict.get(img)[y.astype(np.int), x.astype(np.int)]
            self.profile['x_pix'] = x
            self.profile['y_pix'] = y
            self.profile['dist_pix'] = np.sqrt((x[0] - x)**2 + (y[0] - y)**2)
            self.profile['dist'] = self.profile.dist_pix * self.spatial_param.get('scale')
            self.profile['x'] = self.profile.x_pix * self.spatial_param.get('scale') + self.spatial_param.get('extent')[0]
            self.profile['y'] = self.profile.y_pix * self.spatial_param.get('scale') + self.spatial_param.get('extent')[2]

        elif param.get('method') == 'skimage':
            co = np.flip(coord, axis=1)
            xs, ys = np.mgrid[0:self.img_bw.shape[1]:1, 0:self.img_bw.shape[0]:1]
            for img in imgs:
                print('... sampling from {}'.format(img))
                self.profile[img] = measure.profile_line(img_dict.get(img), co[0], co[1],
                                                    linewidth=param.get('linewidth'),
                                                    reduce_func=param.get('reduce_func'),
                                                    order=param.get('spline_order'))
                self.profile['x_pix'] = measure.profile_line(xs, co[0], co[1], order=0)
                self.profile['y_pix'] = measure.profile_line(ys, co[0], co[1], order=0)
            self.profile['dist_pix'] = np.arange(0, np.ceil(np.linalg.norm(co[1]-co[0]))+1)
            self.profile['dist'] = self.profile.dist_pix * self.spatial_param.get('scale')
            self.profile['x'] = self.profile.x_pix * self.spatial_param.get('scale') + self.spatial_param.get('extent')[0]
            self.profile['y'] = self.profile.y_pix * self.spatial_param.get('scale') + self.spatial_param.get('extent')[2]

        else:
            print('ERROR: sampling method not existing. Available: scipy, numpy, skimage')


if __name__ == '__main__':
    fnir = '/home/simonfi/Desktop/202202_finse_livox/NIR_cam/20220224_NIR/DSC01493.JPG'
    fcalib = '/home/simonfi/Downloads/Foc0200Diaph028-FlatField.tif'
    mo = nir(fname_nir=fnir, fname_calib=None, kernel_size=500)

    mo.pick_targets()
    mo.convert_all()
    mo.scale_spatially()
    mo.extract_profile(['SSA', 'd_optical', 'reflectance'], param={'method': skimage,
                                                                   'linewidth': 5,
                                                                   'reduce_func': np.median,
                                                                   'spline_order': 1})

    fig, ax = plt.subplots(1, 3, sharey=True)
    ax[0].plot(mo.profile.reflectance, mo.profile.dist)
    ax[0].grid(':')
    ax[0].set_xlabel('Reflectance [%]')

    ax[1].plot(mo.profile.SSA, mo.profile.dist)
    ax[1].grid(':')
    ax[1].set_xlabel('SSA [mm$^{-1}$]')

    ax[2].plot(mo.profile.d_optical, mo.profile.dist)
    ax[2].grid(':')
    ax[2].set_xlabel('d$_{optical}$ [mm]')
    plt.show()




    



    
    