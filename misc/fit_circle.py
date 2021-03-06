#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import os
from scipy.ndimage import map_coordinates
import lmfit

import matplotlib              as mpl
import matplotlib.pyplot       as plt
import matplotlib.colors       as mcolors
import matplotlib.patches      as mpatches
import matplotlib.transforms   as mtransforms
import matplotlib.font_manager as font_manager


class CircleModel:
    def __init__(self, cx, cy, r, num = 100):
        super().__init__()

        self.cx  = cx
        self.cy  = cy
        self.r   = r
        self.num = num
        self.crds = np.zeros((2, num))    # 2 is the size of (x, y)


    def set_seed(self, seed):
        np.random.seed(seed)


    def update_crds(self, theta):
        cx = self.cx
        cy = self.cy
        r  = self.r

        # Convert input to numpy array with shape (N,)...
        if not isinstance(theta, np.ndarray): theta = np.array([theta]).reshape(-1)

        len_theta = len(theta)

        self.crds[1] = r * np.cos(theta) + cx   # In image, horizontal axis is axis=1 in matrix
        self.crds[0] = r * np.sin(theta) + cy

        return None


    def update_crds_with_noise(self):
        dx = np.random.normal(loc = 1.0, scale = 0.2, size = self.num)
        dy = np.random.normal(loc = 1.0, scale = 0.2, size = self.num)

        self.crds[1] += dx
        self.crds[0] += dy

        return None


    def generate_crds(self):
        ## theta = np.random.uniform(low = 0.0, high = 2 * np.pi, size = (self.num, ))
        theta = np.linspace(0.0, 2 * np.pi, self.num)
        self.update_crds(theta)

        return None


    def get_pixel_values(self, img):
        ## pvals = map_coordinates(img, self.crds, order=1, mode='nearest')
        pvals = map_coordinates(img, self.crds)

        return pvals




class OptimizeCircleModel(CircleModel):
    def __init__(self, cx, cy, r, num):
        super().__init__(cx, cy, r, num)

        self.params = self.init_params()
        self.params.add("cx", value = cx)
        self.params.add("cy", value = cy)
        self.params.add("r" , value = r )


    def init_params(self): return lmfit.Parameters()


    def unpack_params(self, params): return [ v.value  for _, v in params.items() ]


    def residual_model(self, params, img, **kwargs):
        parvals = self.unpack_params(params)
        self.cx, self.cy, self.r = parvals

        self.generate_crds()

        pvals = self.get_pixel_values(img)

        pvals -= img.max()    # Measure the distance from the peak value

        return pvals


    def fit(self, img, **kwargs):
        res = lmfit.minimize( self.residual_model,
                              self.params,
                              method     = 'leastsq',
                              nan_policy = 'omit',
                              args       = (img, ),
                              **kwargs )

        return res


    def report_fit(self, res):
        lmfit.report_fit(res)




class Display():
    def __init__(self, img, crds_init, crds, figsize, **kwargs):
        self.img = img
        self.crds = crds
        self.crds_init = crds_init
        self.figsize = figsize
        for k, v in kwargs.items(): setattr(self, k, v)

        self.config_fonts()
        self.config_colorbar()

    def config_fonts(self):
        # Where to load external font...
        drc_py    = os.path.dirname(os.path.realpath(__file__))
        drc_font  = os.path.join("fonts", "Helvetica")
        fl_ttf    = f"Helvetica.ttf"
        path_font = os.path.join(drc_py, drc_font, fl_ttf)
        prop_font = font_manager.FontProperties( fname = path_font )

        # Add Font and configure font properties
        font_manager.fontManager.addfont(path_font)
        prop_font = font_manager.FontProperties(fname = path_font)
        self.prop_font = prop_font

        # Specify fonts for pyplot...
        plt.rcParams['font.family'] = prop_font.get_name()
        plt.rcParams['font.size']   = 18

        return None


    def create_panels(self):
        nrows, ncols = 2, 1
        fig = plt.figure(figsize = self.figsize)
        gspec =  fig.add_gridspec(nrows, ncols, height_ratios = [1, 1/20])
        ax_img  = fig.add_subplot(gspec[0,0], aspect = 1)
        ax_bar_img  = fig.add_subplot(gspec[1,0], aspect = 1/20)

        return fig, (ax_img, ax_bar_img, )


    def plot_img(self, title = ""): 
        img = self.img
        im = self.ax_img.imshow(img, norm = self.divnorm, zorder = 1)
        ## im.set_cmap('seismic')
        im.set_cmap('gray')
        plt.colorbar(im, cax = self.ax_bar_img, orientation="horizontal", pad = 0.05)


    def plot_circle(self, crds, color = 'yellow', zorder = 2, label = ''):
        x = crds[1]
        y = crds[0]
        self.ax_img.plot(x, y, zorder = zorder, c = color, alpha = 1, linewidth = 2, label = label)


    def config_colorbar(self, vmin = -1, vcenter = 0, vmax = 1):
        # Plot image...
        self.divnorm = mcolors.TwoSlopeNorm(vcenter = vcenter, vmin = vmin, vmax = vmax)


    def show(self, title = '', is_save = False): 
        self.fig, (self.ax_img, self.ax_bar_img, ) = self.create_panels()

        self.plot_img()
        self.plot_circle(self.crds_init, color = 'blue', zorder = 2, label = 'init')
        self.plot_circle(self.crds     , color = 'red', zorder = 3, label = 'final')
        self.ax_img.legend(loc=(1.04,0))

        if not is_save: 
            plt.show()
        else:
            # Set up drc...
            DRCPDF         = "pdfs"
            drc_cwd        = os.getcwd()
            prefixpath_pdf = os.path.join(drc_cwd, DRCPDF)
            if not os.path.exists(prefixpath_pdf): os.makedirs(prefixpath_pdf)

            # Specify file...
            fl_pdf = f"{title}.pdf"
            path_pdf = os.path.join(prefixpath_pdf, fl_pdf)

            # Export...
            ## plt.savefig(path_pdf, dpi = 100, bbox_inches='tight', pad_inches = 0)
            plt.savefig(path_pdf, dpi = 100, transparent=True)

        plt.close('all')




# Read the max pooled image...
fl_img_max = "mfxlv4920.42.epix10k2M.max.npy"
img = np.load(fl_img_max)

# Initial values...
cx, cy, r = 821, 831, 200
num = 1000

# Normalize image...
img = (img - np.mean(img)) / np.std(img)

# Create a circle model...
model = OptimizeCircleModel(cx = cx, cy = cy, r = r, num = num)
model.generate_crds()
crds_init = model.crds.copy()

# Fitting...
res = model.fit(img)
model.report_fit(res)
crds = model.crds

# Dispaly an image...
disp_manager = Display(img, crds_init, crds, figsize = (10, 8))
disp_manager.show(is_save = False)
