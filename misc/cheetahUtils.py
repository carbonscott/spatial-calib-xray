# Cheetah-related data and methods
import sys
import h5py
import numpy as np
from dataclasses import dataclass
from abc import ABC, abstractmethod
from collections import namedtuple

class DetectorNotSupportedError(Exception):
    """Base class for other exceptions"""
    pass

@dataclass
class SupportedDetectors:
    supported = {'cspad','rayonix','jungfrau4m','epix10k2m'} # TODO: add pnccd for SPI

    @classmethod
    def parseDetectorName(cls, detName: str) -> str:
        """simplify detector name into psocake name and return lower case"""
        for det in cls.supported:
            if 'epix10k' in detName.lower() and '2m' in detName.lower():
                return 'epix10k2m'
            elif 'cxids' in detName.lower() and 'jungfrau' in detName.lower():
                return 'jungfrau4m' 
            elif det in detName.lower():
                return det
        raise DetectorNotSupportedError("{} is not supported in psocake".format(detName))


class DetectorDescriptor(ABC):

    @property
    @abstractmethod
    def psanaDim(self):
        """(seg, row, col)"""
        raise NotImplementedError

    @property
    @abstractmethod
    def quads(self):
        """"(numQuad, numAsicsPerQuad)"""
        raise NotImplementedError

    @property
    def tileDim(self):
        """"(dim0, dim1)"""
        ChDim = namedtuple('ChDim', ['dim0', 'dim1'])
        return ChDim(self.quads.numAsicsPerQuad * self.psanaDim.rows, self.quads.numQuad * self.psanaDim.cols)

    @abstractmethod
    def convert_peaks_to_cheetah(s, r, c):
        """convert psana peak positions to cheetah tile positions"""

    @abstractmethod
    def convert_peaks_to_psana(row2d, col2d):
        """convert cheetah tile peak positions to psana positions"""

    def pct(self, unassembled):
        """psana cheetah transform: convert psana unassembled detector to cheetah tile shape"""
        counter = 0
        img = np.zeros(self.tileDim)
        for quad in range(self.quads.numQuad):
            for seg in range(self.quads.numAsicsPerQuad):
                img[seg * self.psanaDim.rows:(seg + 1) * self.psanaDim.rows,
                    quad * self.psanaDim.cols:(quad + 1) * self.psanaDim.cols] = unassembled[counter, :, :]
                counter += 1

        return img

    def ipct(self, tile):
        """inverse psana cheetah transform: convert cheetah tile to psana unassembled detector shape"""
        calib = np.zeros((self.quads.numQuad * self.quads.numAsicsPerQuad, self.psanaDim.rows, self.psanaDim.cols))
        counter = 0
        for quad in range(self.quads.numQuad):
            for seg in range(self.quads.numAsicsPerQuad):
                calib[counter, :, :] = \
                    tile[seg * self.psanaDim.rows:(seg + 1) * self.psanaDim.rows,
                         quad * self.psanaDim.cols:(quad + 1) * self.psanaDim.cols]
                counter += 1
        return calib


class DetectorDescriptor(ABC):

    @property
    @abstractmethod
    def psanaDim(self):
        """(seg, row, col)"""
        raise NotImplementedError

    @property
    @abstractmethod
    def quads(self):
        """"(numQuad, numAsicsPerQuad)"""
        raise NotImplementedError

    @property
    def tileDim(self):
        """"(dim0, dim1)"""
        ChDim = namedtuple('ChDim', ['dim0', 'dim1'])
        return ChDim(self.quads.numAsicsPerQuad * self.psanaDim.rows, self.quads.numQuad * self.psanaDim.cols)

    @abstractmethod
    def convert_peaks_to_cheetah(s, r, c):
        """convert psana peak positions to cheetah tile positions"""

    @abstractmethod
    def convert_peaks_to_psana(row2d, col2d):
        """convert cheetah tile peak positions to psana positions"""

    def pct(self, unassembled):
        """psana cheetah transform: convert psana unassembled detector to cheetah tile shape"""
        counter = 0
        img = np.zeros(self.tileDim)
        for quad in range(self.quads.numQuad):
            for seg in range(self.quads.numAsicsPerQuad):
                img[seg * self.psanaDim.rows:(seg + 1) * self.psanaDim.rows,
                    quad * self.psanaDim.cols:(quad + 1) * self.psanaDim.cols] = unassembled[counter, :, :]
                counter += 1

        return img

    def ipct(self, tile):
        """inverse psana cheetah transform: convert cheetah tile to psana unassembled detector shape"""
        calib = np.zeros((self.quads.numQuad * self.quads.numAsicsPerQuad, self.psanaDim.rows, self.psanaDim.cols))
        counter = 0
        for quad in range(self.quads.numQuad):
            for seg in range(self.quads.numAsicsPerQuad):
                calib[counter, :, :] = \
                    tile[seg * self.psanaDim.rows:(seg + 1) * self.psanaDim.rows,
                         quad * self.psanaDim.cols:(quad + 1) * self.psanaDim.cols]
                counter += 1
        return calib
