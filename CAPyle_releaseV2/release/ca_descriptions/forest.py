# Name: Conway's game of life
# Dimensions: 2

# --- Set up executable path, do not edit ---
import sys
import inspect
this_file_loc = (inspect.stack()[0][1])
main_dir_loc = this_file_loc[:this_file_loc.index('ca_descriptions')]
sys.path.append(main_dir_loc)
sys.path.append(main_dir_loc + 'capyle')
sys.path.append(main_dir_loc + 'capyle/ca')
sys.path.append(main_dir_loc + 'capyle/guicomponents')
# ---

from capyle.ca import Grid2D, Neighbourhood, CAConfig, randomise2d
import capyle.utils as utils
import numpy as np


def transition_func(grid, neighbourstates, neighbourcounts):
    
    # town == states == 0, water == states == 1, dense_forest == states == 2, canyon == states == 3,
    # chaparral == states == 4, powerplant == states == 5, incinerator == states == 6,burning_dense_forest == states == 7,
    # burning_canyon == states == 8, burning_chaparral == states == 9, burned_dense_forest == states == 10,
    # burned_canyon == states == 11, burned_chaparral == states == 12, burned_town == states == 13
    
    # Town - 0,0,0
    # Water - 0,0,1
    # Dense forest - 0.5,0.5,0
    # Canyon - 1,1,0
    # Chaparral - 0,1,0
    # Power plant - 0,0.5,0.5
    # Incinerator - 0.5,0.5,0.5
    # Burning dense forest - 1,0.5,0
    # Burning canyon - 1,0.5,0
    # Burning chaparral - 0.75, 0.5,0
    # Burned dense forest - 0.25,0.25,0.25
    # Burned canyon - 0.25, 0.25, 0.25
    # Burned chaparral - 0.75,0.75,0.75
    # Burned town - 1,0,0


    # unpack state counts for clarity
    burning_dense_forest, burning_canyon, burning_chaparral = neighbourcounts
    
   
    # Set all cells to 0 (dead)
    grid[:, :] = 0
    
    # Set cells to 0 where sick cells die of isolation or sickness
    grid[isolation_death | sickness_death] = 0

    
    return grid


def setup(args):
    config_path = args[0]
    config = utils.load(config_path)
    # ---THE CA MUST BE RELOADED IN THE GUI IF ANY OF THE BELOW ARE CHANGED---
    config.title = "Forest fire"
    config.dimensions = 2
    config.states = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13)
    # ------------------------------------------------------------------------

    # ---- Override the defaults below (these may be changed at anytime) ----

    config.state_colors = [(0,0,0), (0,0,1), (0.5,0.5,0), (1,1,0), (0,1,0),
                           (0,0.5,0.5), (0.5,0.5,0.5), (1,0.5,0), (1,0.5,0), (0.75, 0.5,0), 
                           (0.25,0.25,0.25), (0.25, 0.25, 0.25), (0.75,0.75,0.75), (1,0,0)]
    # config.num_generations = 150
    config.grid_dims = (40,40)

    # ----------------------------------------------------------------------

    if len(args) == 2:
        config.save()
        sys.exit()

    return config


def main():
    # Open the config object
    config = setup(sys.argv[1:])

    # Create grid object
    grid = Grid2D(config, transition_func)

    # Run the CA, save grid state every generation to timeline
    timeline = grid.run()

    # save updated config to file
    config.save()
    # save timeline to file
    utils.save(timeline, config.timeline_path)


if __name__ == "__main__":
    main()
