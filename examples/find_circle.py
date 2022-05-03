#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from spatial_calib_xray.model   import OptimizeCircleModel, InitCircle
from spatial_calib_xray.display import Display

# Constant...
num = 1000

# Read the max pooled image...
fl_img_max = "mfxlv4920.42.epix10k2M.max.npy"
img = np.load(fl_img_max)

# Normalize image...
img = (img - np.mean(img)) / np.std(img)

# Display an image...
disp_manager = Display(img, figsize = (12, 12))

circle_list = []
for _ in range(1):
    disp_manager.select_circle(is_save = False)

    # Form init circle...
    crds_pt1, crds_pt2, crds_pt3 = disp_manager.crds_mouse
    cx, cy, r = InitCircle(crds_pt1, crds_pt2, crds_pt3).solve()

    # Create a circle model...
    model = OptimizeCircleModel(cx = cx, cy = cy, r = r, num = num)
    model.generate_crds()
    crds_init = model.crds.copy()

    # Fitting...
    res = model.fit(img)
    model.report_fit(res)
    crds = model.crds
    disp_manager.show(crds_init, crds, is_save = False)
    circle_list.append(res.params)

## r1 = circle_list[0][-1]
## r2 = circle_list[1][-1]
## 
## r2 - r1
