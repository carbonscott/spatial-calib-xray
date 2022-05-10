#!/usr/bin/env python
# -*- coding: utf-8 -*-

from math import sqrt
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


    def update_crds_with_noise(self):
        dx = np.random.normal(loc = 1.0, scale = 0.2, size = self.num)
        dy = np.random.normal(loc = 1.0, scale = 0.2, size = self.num)

        self.crds[1] += dx
        self.crds[0] += dy

        return None


    def generate_crds(self):
        theta = np.linspace(0.0, 2 * np.pi, self.num)

        cx = self.cx
        cy = self.cy
        r  = self.r

        # Convert input to numpy array with shape (N,)...
        if not isinstance(theta, np.ndarray): theta = np.array([theta]).reshape(-1)

        len_theta = len(theta)

        self.crds[1] = r * np.cos(theta) + cx   # In image, horizontal axis is axis=1 in matrix
        self.crds[0] = r * np.sin(theta) + cy

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
        print(f"___/ Fitting \___")
        res = lmfit.minimize( self.residual_model,
                              self.params,
                              method     = 'leastsq',
                              nan_policy = 'omit',
                              args       = (img, ),
                              **kwargs )

        return res


    def report_fit(self, res):
        lmfit.report_fit(res)




class ConcentricCircles:

    def __init__(self, cx, cy, r, num = 100):
        super().__init__()

        self.cx  = cx                                # Beam center position in pixels along x-axis (axis = 1 in numpy format)
        self.cy  = cy                                # Beam center position in pixels along y-axis
        self.r   = np.array([r]).reshape(-1)         # List of radii for all concentric circles in pixels
        self.num = num                               # Number of pixels sampled from a circle
        self.crds = np.zeros((2, num * len(self.r))) # Coordinates where pixels are sampled from all circles.  Unit is pixel.  2 is the size of (x, y)


    def generate_crds(self):
        """
        Generate coordinates of sample points along each concentric circle
        """
        # Fetching initial values that define concentric circles...
        cx = self.cx
        cy = self.cy
        r  = np.array([self.r]).reshape(-1, 1) # Facilitate broadcasting in calculting crds_x and crds_y

        # Find all theta values for generating coordinates of sample points...
        theta = np.linspace(0.0, 2 * np.pi, self.num)
        if not isinstance(theta, np.ndarray): theta = np.array([theta]).reshape(-1)

        # Generate coordinates...
        crds_x = r * np.cos(theta) + cx
        crds_y = r * np.sin(theta) + cy

        # Reshape crds into one flat array to facilitate optimization routine...
        self.crds[1] = crds_x.reshape(-1)
        self.crds[0] = crds_y.reshape(-1)

        return None


    def get_pixel_values(self, img):
        """
        Get pixel values from all sample points.  If a sample point has 
        subpixel coordinates, interpolation will take place.  
        """
        pvals = map_coordinates(img, self.crds)

        return pvals




class OptimizeConcentricCircles(ConcentricCircles):

    def __init__(self, cx, cy, r, num):
        super().__init__(cx, cy, r, num)

        # Provide parameters for optimization...
        self.params = self.init_params()
        self.params.add("cx", value = cx)
        self.params.add("cy", value = cy)

        # Set up radius parameter based on number of circles...
        for i in range(len(r)): self.params.add(f"r{i:d}" , value = r[i] )


    def init_params(self): 
        """
        Initialize parameters for optimization.
        """
        return lmfit.Parameters()


    def unpack_params(self, params): 
        """
        Unpack all parameters from dictionary.
        """
        return [ v.value  for _, v in params.items() ]


    def residual_model(self, params, img, **kwargs):
        """
        Calculate the residual for least square optimization.
        """
        parvals = self.unpack_params(params)
        self.cx, self.cy = parvals[:2]
        self.r = parvals[2:]

        self.generate_crds()

        pvals = self.get_pixel_values(img)

        pvals -= img.max()    # Measure the distance from the peak value

        return pvals


    def fit(self, img, **kwargs):
        """
        Fit the residual model.
        """
        print(f"___/ Fitting \___")
        res = lmfit.minimize( self.residual_model,
                              self.params,
                              method     = 'leastsq',
                              nan_policy = 'omit',
                              args       = (img, ),
                              **kwargs )

        return res


    def report_fit(self, res):
        """
        Report details of the optimization.  
        """
        lmfit.report_fit(res)




class InitCircle:
    ''' Refer to http://paulbourke.net/geometry/circlesphere/
    '''

    def __init__(self, crds_pt1, crds_pt2, crds_pt3):
        self.x1, self.y1 = crds_pt1
        self.x2, self.y2 = crds_pt2
        self.x3, self.y3 = crds_pt3


    def solve(self):
        x1, y1 = self.x1, self.y1
        x2, y2 = self.x2, self.y2
        x3, y3 = self.x3, self.y3

        ma = (y2 - y1) / (x2 - x1)
        mb = (y3 - y2) / (x3 - x2)

        cx = ma * mb * (y1 - y3) + mb * (x1 + x2) - ma * (x2 + x3)
        cx /= 2 * (mb - ma)

        cy  = cx - (x2 + x3) / 2
        cy *= -1 / mb
        cy += (y2 + y3) / 2

        r = sqrt( (x1 - cx)**2 + (y1 - cy)**2 )

        return cx, cy, r
