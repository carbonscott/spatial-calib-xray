#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import os
import matplotlib              as mpl
import matplotlib.pyplot       as plt
import matplotlib.colors       as mcolors
import matplotlib.patches      as mpatches
import matplotlib.transforms   as mtransforms
import matplotlib.font_manager as font_manager


class Display():
    def __init__(self, img, figsize, **kwargs):
        self.img = img
        self.figsize = figsize
        self.crds_mouse = []
        for k, v in kwargs.items(): setattr(self, k, v)

        ## self.config_fonts()
        self.config_colorbar()


    def config_fonts(self):
        # Where to load external font...
        drc_py    = os.getcwd()
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


    def save_mouse_crds(self, event):
        print( f"{event.xdata}, {event.ydata}" )
        self.crds_mouse.append( (event.xdata, event.ydata) )

        if len(self.crds_mouse) > 2: 
            ## self.fig.canvas.mpl_disconnect(self.cid)
            plt.close()


    def select_circle(self, title = '', is_save = False): 
        self.fig, (self.ax_img, self.ax_bar_img, ) = self.create_panels()

        self.plot_img()

        self.crds_mouse = []
        self.cid = self.fig.canvas.mpl_connect('button_press_event', self.save_mouse_crds)

        plt.show()


    def show(self, crds_init, crds, title = '', is_save = False): 
        self.fig, (self.ax_img, self.ax_bar_img, ) = self.create_panels()

        self.plot_img()
        self.plot_circle(crds_init, color = 'blue', zorder = 2, label = 'init')
        self.plot_circle(crds     , color = 'red', zorder = 3, label = 'final')
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




class DisplayConcentricCircles():
    def __init__(self, img, figsize, **kwargs):
        self.img = img
        self.figsize = figsize
        self.crds_mouse = []
        for k, v in kwargs.items(): setattr(self, k, v)

        self.config_fonts()
        self.config_colorbar()


    def config_fonts(self):
        # Where to load external font...
        drc_py    = os.getcwd()
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


    def save_mouse_crds(self, event):
        print( f"{event.xdata}, {event.ydata}" )
        self.crds_mouse.append( (event.xdata, event.ydata) )

        if len(self.crds_mouse) > 2: 
            ## self.fig.canvas.mpl_disconnect(self.cid)
            plt.close()


    def select_circle(self, title = '', is_save = False): 
        self.fig, (self.ax_img, self.ax_bar_img, ) = self.create_panels()

        self.plot_img()

        self.crds_mouse = []
        self.cid = self.fig.canvas.mpl_connect('button_press_event', self.save_mouse_crds)

        plt.show()


    def show(self, crds_init, crds, title = '', is_save = False): 
        self.fig, (self.ax_img, self.ax_bar_img, ) = self.create_panels()

        self.plot_img()
        for i in range(crds_init.shape[1]):
            label = 'init' if i < 1 else None
            self.plot_circle(crds_init[:, i, :], color = 'blue', zorder = 2, label = label)

            label = 'final' if i < 1 else None
            self.plot_circle(crds[:, i, :]     , color = 'red' , zorder = 3, label = label)
            #                     ^  ^  ^
            # (x, y) _____________|  :  |
            #                        :  |
            # num of circles ........:  |
            #                           |
            # num of sample points _____|

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
