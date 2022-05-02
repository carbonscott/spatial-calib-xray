#!/usr/bin/env python
# -*- coding: utf-8 -*-

import psana

import matplotlib              as mpl
import matplotlib.pyplot       as plt
import matplotlib.colors       as mcolors
import matplotlib.patches      as mpatches
import matplotlib.transforms   as mtransforms
import matplotlib.font_manager as font_manager
import numpy as np
import os

class PsanaImg:
    """
    For online data, set up environment variable correctly.  

    ```
    export SIT_PSDM_DATA=/cds/data/drpsrcf
    ```

    It serves as an image accessing layer based on the data management system
    psana in LCLS.  
    """

    def __init__(self, exp, run, mode, detector_name):
        # Biolerplate code to access an image
        # Set up data source
        self.datasource_id = f"exp={exp}:run={run}:{mode}"
        self.datasource    = psana.DataSource( self.datasource_id )
        self.run_current   = next(self.datasource.runs())
        self.timestamps    = self.run_current.times()

        # Set up detector
        self.detector = psana.Detector(detector_name)


    def get(self, event_num, mode = "image"):
        # Fetch the timestamp according to event number...
        timestamp = self.timestamps[int(event_num)]

        # Access each event based on timestamp...
        event = self.run_current.event(timestamp)

        # Only three modes are supported...
        assert mode in ("raw", "image", "calib"), f"Mode {mode} is not allowed!!!  Only 'raw' or 'image' are supported."

        # Fetch image data based on timestamp from detector...
        read = { "image" : self.detector.image, }
        img = read[mode](event)

        return img




class DisplaySPIImg():

    def __init__(self, img, figsize, **kwargs):
        self.img = img
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
        im = self.ax_img.imshow(img, norm = self.divnorm)
        im.set_cmap('seismic')
        plt.colorbar(im, cax = self.ax_bar_img, orientation="horizontal", pad = 0.05)


    def config_colorbar(self, vmin = -1, vcenter = 0, vmax = 1):
        # Plot image...
        self.divnorm = mcolors.TwoSlopeNorm(vcenter = vcenter, vmin = vmin, vmax = vmax)


    def show(self, center = None, angle = None, title = '', is_save = False): 
        self.fig, (self.ax_img, self.ax_bar_img, ) = self.create_panels()

        self.plot_img()

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




# Specify the dataset and detector...
exp, run, mode, detector_name = 'mfxlv4920', '42', 'idx', 'epix10k2M'

# Initialize an image reader...
img_reader = PsanaImg(exp, run, mode, detector_name)

# Access an image (e.g. event 796)...
event_num = 7
img = img_reader.get(event_num, mode = "image")

# Normalize image...
img = (img - np.mean(img)) / np.std(img)

# Dispaly an image...
title = f''
disp_manager = DisplaySPIImg(img, figsize = (10, 8))
disp_manager.show(title = title, is_save = False)
