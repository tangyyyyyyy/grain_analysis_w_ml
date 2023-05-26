# -*- coding: utf-8 -*-
"""
---------------------------------
ML FOR MICROSTRUCTURE PREDICTION
---------------------------------

This script is for producing artifical microstructures.

STEPS:
    1. produce a cell with n grain centers distributed randomly at least a distance
    l apart in a square cell with edge of length e_square
    2. simulate grain growth
    3. save an image of completed grain*
    3*. as we get more complex, also save particular "processing" labels
    in a text document (i.e. temperature, treatment, material, etc) for training

NEEDS:
    1. simple grain growth algorithm with walls (for now, constant growth,
    stops when makes contact with another grain/wall)

Created on Wed Oct 20 15:31:11 2021

@author: Kashyap
"""

"""
---------------------------------
ABSTRACT CLASSES/METHODS
---------------------------------
"""

import numpy as np
from abc import abstractmethod, ABC
from dataclasses import dataclass, field

@dataclass()
class abstract_microstructure(ABC):
    cell_edge: int
    grain_center_min_distance: float
    grain_map: np.ndarray = field(init=False, repr=False)

    @abstractmethod
    def __post_init__(self):
        """
        After initializing cell, run init_grain_placement
        """
        pass

    @abstractmethod
    def grow_grain(self) -> np.ndarray:
        """
        PURPOSE:
            Places grain centers following the restrictions in constants file,
            outputs a numpy array containing coordinate of each grain center

        ALGORITHM:
            Poisson-disk Sampling

        PARAMETERS:

        OUTPUT:
            np.ndarray = an array containing each grain center
        """
        pass

    @abstractmethod
    def image_cell(self) -> None:
        """
        PURPOSE:
            Convert grain array into image of microstructure, save to png, and
            produce a text file with training labels
        """
        pass
