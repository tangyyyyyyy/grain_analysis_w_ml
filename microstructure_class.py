# -*- coding: utf-8 -*-
"""
Created on Fri May  5 14:33:28 2023

@author: Kashyap
"""

import numpy as np
from dataclasses import dataclass, field
from abstract_microstructure import abstract_microstructure
from constants import e_square, k, min_grain_dist_l, rand_seed
from poisson_sampler import poisson_disk_sampler, visualize_grains, extract_coords

from scipy.spatial import Voronoi, voronoi_plot_2d
import matplotlib.pyplot as plt

import random as rand

"""
---------------------------------
CLASSES/METHODS
---------------------------------
"""

@dataclass()
class microstructure(abstract_microstructure):
    cell_edge: int
    grain_center_min_distance: float
    grain_list: np.ndarray = field(init=False, repr=False)
    
    def __post_init__(self):
        #initial grain positions
        self.grain_list = poisson_disk_sampler(e_square, min_grain_dist_l,  k)

    def grow_grain(self):
        #self.grain_map = grain_growth_alg(self.grain_map)
        coords = extract_coords(self.grain_list)
        grain_map = Voronoi(coords)
        fig = voronoi_plot_2d(grain_map)
        plt.show()

    def image_cell(self) -> None:
        #visual for sanity
        fig = visualize_grains(self.grain_list)
        plt.xlim([0, e_square])
        plt.ylim([0, e_square])
        plt.xlabel("x")
        plt.ylabel("y")
        plt.title("Initial Grain Position")
        plt.show()
    

##testing
rand.seed(rand_seed)
ms = microstructure(e_square, min_grain_dist_l)
ms.image_cell()
ms.grow_grain()
