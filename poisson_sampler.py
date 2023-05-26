# -*- coding: utf-8 -*-
"""
Created on Fri May  5 14:41:02 2023

@author: Kashyap
"""

import numpy as np
import random as rand
from constants import min_grain_dist_l, e_square, rand_seed, k
from grain_classes import grain, grain_grid

import matplotlib.pyplot as plt
#from matplotlib.animation import ArtistAnimation

def poisson_disk_sampler(edge_len:float, min_dist:float, k:int) -> np.ndarray:

    ####################
    ###INITIALIZATION###
    ####################

    #initialize grain lists and grid
    grain_centers = []
    active_grains = []
    grid = grain_grid(edge_len, min_dist)

    #define initial random points within the microstructure
    g0 = make_random_grain(edge_len)
         

    #add g0 to initialized lists
    grid.add_grain(g0)
    grain_centers.append(g0)
    active_grains.append(g0)

    #######################
    ###POISSON ALGORITHM###
    #######################

    while len(active_grains) > 0:
        
        print('# found grains: ', len(grain_centers))
        #pick a random point within the active grains list
        random_index = int(np.floor(rand.random()*len(active_grains)))
        g_active = active_grains[random_index]

        #generate a new point 1-2 min distance away (will have same radius) from the selected active point
        for tries in range(0, k):
            g_new = make_test_grain(g_active, min_dist)

            #check if the point is valid,  if it is not, try a new point
            if pt_validity_check(grid, g_new, min_dist = min_dist):
                grain_centers.append(g_new)
                active_grains.append(g_new)
                grid.add_grain(g_new)
                break

            #check if we are on the last k, if no point was found after k attempts, stop trying to find a point near current active point
            elif tries >= (k-1):
                active_grains.pop(random_index)
                break
            else:
                continue
    return np.asarray(grain_centers)

def make_random_grain(edge_len) -> grain:
    #produce a grain placed randomly within the boundary square
    ran_grain = grain(x = rand.random()*edge_len, y = rand.random()*edge_len)
    return ran_grain

def make_test_grain(grain_init, min_dist) -> grain:
    #produce a test grain within 1-2 radii away from the initial grain
    theta = np.deg2rad(rand.randrange(360))
    distance = rand.uniform(1.0, 2.0)*min_dist
    x_new = grain_init.x + distance * np.cos(theta)
    y_new = grain_init.y + distance * np.sin(theta)
    test_grain = grain(x_new, y_new)
    return test_grain

def pt_validity_check(grid, g_new, min_dist) -> bool():
    #make sure point is on the screen
    if (g_new.x<0 or g_new.x>grid.edge_len or g_new.y<0 or g_new.y>grid.edge_len):
        return False

    #define box of 1 radius around p
    xindex = int(np.floor(g_new.x/grid.cell_size))
    yindex = int(np.floor(g_new.y/grid.cell_size))
    i0 = max(xindex - 1, 0)
    i1 = min(xindex + 1, grid.cell_width - 1)
    j0 = max(yindex - 1, 0)
    j1 = min(yindex + 1, grid.cell_height - 1)

    #min_dist = 

    #check distance between neighbor points
    for i in range(i0, i1):
        for j in range(j0, j1):
            if grid.grid[i][j][0] == None:
                continue
            if (np.linalg.norm(grid.grid[i][j][0].coords() - g_new.coords()) < (min_dist)):
                return False;
    #if no points are too close, return true
    return True
    
def visualize_grains(grain_list, fig = plt.figure()):
    
    #setup list of images
    # imgs = []
    # for grain in grain_list:
    #     pass  
    #animated_grains = animation.ArtistAnimation(fig, frame, interval=100)
    
    x_coords = [grain.x for grain in grain_list]
    y_coords = [grain.y for grain in grain_list]
    plt.scatter(x_coords, y_coords, s=2)
    return fig

def extract_coords(grain_list):
    x_coords = [grain.x for grain in grain_list]
    y_coords = [grain.y for grain in grain_list]
    return [(x_coords[i], y_coords[i]) for i in range(0, len(x_coords))]