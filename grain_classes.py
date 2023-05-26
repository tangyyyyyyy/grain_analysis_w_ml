# -*- coding: utf-8 -*-
"""
Created on Sun May 21 10:22:58 2023

@author: Kashyap
"""

import numpy as np
from dataclasses import dataclass, field
        
@dataclass()
class grain():
    x: float
    y: float
    def coords(self) -> np.ndarray:
        return np.asarray([self.x, self.y])

@dataclass()
class grain_grid():
    edge_len: float
    r: float
    
    cell_size: float = field(init = False)
    cell_width: int = field(init = False)
    cell_height: int = field(init = False)
    cell_size: float = field(init = False)
    grid: np.ndarray = field(init = False)
    
    def __post_init__(self):
        self.cell_size = self.r/np.sqrt(2)
        self.cell_width = int(np.ceil(self.edge_len/self.cell_size) + 1)
        self.cell_height = self.cell_width
        self.grid = np.empty(shape=(self.cell_width, self.cell_height, 1), dtype=grain)
        self.cell_size = self.r/np.sqrt(2)
    
    def add_grain(self, new_grain):
        xindex = int(np.floor(new_grain.x/self.cell_size))
        yindex = int(np.floor(new_grain.y/self.cell_size))
        if self.grid[xindex][yindex] == None:
            self.grid[xindex][yindex] = new_grain
        else:
            print("Grain already exists at this position!")