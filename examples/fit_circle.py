#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from spatial_calib_xray.model import OptimizeCircleModel
from spatial_calib_xray.display import Display


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

# Display an image...
disp_manager = Display(img, crds_init, crds, figsize = (10, 8))
disp_manager.show(is_save = False)
