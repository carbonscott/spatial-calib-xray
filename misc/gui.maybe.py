#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui

# Main event loop
app = QtGui.QApplication([])

image = np.random.normal(size=(500, 400))
plt1 = pg.PlotWidget()
plt1_imageitem = pg.ImageItem(image)
plt1.addItem(plt1_imageitem)
roi_circle = pg.CircleROI([250, 250], [120, 120], pen=pg.mkPen('r',width=2))
## roi_circle.sigRegionChanged.connect(circle_update)
plt1.addItem(roi_circle)
plt1.show()

sys.exit(app.exec_())
