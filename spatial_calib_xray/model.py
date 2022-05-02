#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from scipy.ndimage import map_coordinates
import lmfit

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
