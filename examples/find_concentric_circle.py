#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from spatial_calib_xray.model   import OptimizeConcentricCircles, InitCircle
from spatial_calib_xray.display import Display, DisplayConcentricCircles

# Constant...
num = 1000

# Read the max pooled image...
fl_img_max = "mfxlv4920.42.epix10k2M.max.npy"
img = np.load(fl_img_max)

# Normalize image...
img = (img - np.mean(img)) / np.std(img)

params_list   = []
for _ in range(3):
    disp_manager = Display(img, figsize = (12, 12))
    disp_manager.select_circle(is_save = False)

    # Form init circle...
    crds_pt1, crds_pt2, crds_pt3 = disp_manager.crds_mouse
    cx, cy, r = InitCircle(crds_pt1, crds_pt2, crds_pt3).solve()

    params_list.append((cx, cy, r))

# Consolidat init params...
params_list = np.array(params_list)
cx = np.mean(params_list[:, 0])
cy = np.mean(params_list[:, 1])
r  = params_list[:, 2]

# Create a concentric circle model...
model = OptimizeConcentricCircles(cx = cx, cy = cy, r = r, num = num)
model.generate_crds()
crds_init = model.crds.copy()

crds_init = crds_init.reshape(2, -1, num)

# Fitting...
res = model.fit(img)
model.report_fit(res)
crds = model.crds
crds = crds.reshape(2, -1, num)

disp_manager = DisplayConcentricCircles(img, figsize = (12, 12))
disp_manager.show(crds_init, crds, is_save = False)
