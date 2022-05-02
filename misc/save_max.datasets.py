#!/usr/bin/env python
# -*- coding: utf-8 -*-

import psana
import numpy as np
import os
from mpi4py import MPI

mpi_comm = MPI.COMM_WORLD
mpi_rank = mpi_comm.Get_rank()
mpi_size = mpi_comm.Get_size()

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
        self.datasource_id   = f"exp={exp}:run={run}:{mode}"
        self.datasource      = psana.DataSource( self.datasource_id )
        self.run_current     = next(self.datasource.runs())
        self.timestamps      = self.run_current.times()
        self.event_num_total = len(self.timestamps)

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




# Specify the dataset and detector...
exp, run, mode, detector_name = 'mfxlv4920', '42', 'idx', 'epix10k2M'

# Initialize an image reader...
img_reader = PsanaImg(exp, run, mode, detector_name)

# Max pool all images...
img_sample = img_reader.get(0, mode = "image")
imgs = np.zeros((img_reader.event_num_total, *img_sample.shape))
for event_num in range(img_reader.event_num_total):
    imgs[event_num] = img_reader.get(event_num, mode = "image")

mpi_comm.Reduce(imgs)

imgs_max = np.amax(imgs, axis = 0)
fl_output = f"{exp}.{run}.{detector_name}.max.npy"
path_output = os.path.join(os.getcwd(), fl_output)
np.save(path_output, imgs_max)

MPI.Finalize()
