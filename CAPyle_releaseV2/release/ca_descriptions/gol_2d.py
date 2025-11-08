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
    # dead == states == 0, live == states == 1, sick == states == 2
    
    # unpack state counts for clarity
    dead_neighbours, live_neighbours, sick_neighbours = neighbourcounts
    
    # create boolean arrays for the birth & survival rules
    # if 3 live or sick neighbours and is dead -> cell born
    birth = (live_neighbours + sick_neighbours == 3) & (grid == 0)
    
    # if 2 or 3 live neighbours and is alive -> survives
    survive = ((live_neighbours == 2) | (live_neighbours == 3)) & (grid == 1)
    
    # if 1 or more sick neighbours and is alive -> becomes sick
    catch_sick = (sick_neighbours > 2) & (grid == 1)
    
    # if 1 to 4 sick neighbours and is sick -> remain sick
    remain_sick = ((sick_neighbours + live_neighbours >= 1) & (sick_neighbours + live_neighbours <= 4)) & (grid == 2)
    
    # if 0 or 1 neighbours are alive and is sick -> dies
    isolation_death = (live_neighbours + sick_neighbours <= 1) & (grid == 2)
    
    # if 5 or more neighbours are sick and is sick -> dies
    sickness_death = (sick_neighbours >= 5) & (grid == 2)
    
    # if 0 sick neighbours and is sick -> recovers
    recovery = (sick_neighbours == 0) & (grid == 2)
    
    # Set all cells to 0 (dead)
    grid[:, :] = 0
    
    # Set cells to 0 where sick cells die of isolation or sickness
    grid[isolation_death | sickness_death] = 0
    
    # Set cells to 1 where cell is born or survives or recovers
    grid[birth | survive | recovery] = 1
    
    # Set cells to 2 where cell catches sickness or remains sick
    grid[catch_sick | remain_sick] = 2
    
    return grid


def setup(args):
    config_path = args[0]
    config = utils.load(config_path)
    # ---THE CA MUST BE RELOADED IN THE GUI IF ANY OF THE BELOW ARE CHANGED---
    config.title = "Conway's game of life with sickness"
    config.dimensions = 2
    config.states = (0, 1, 2)
    # ------------------------------------------------------------------------

    # ---- Override the defaults below (these may be changed at anytime) ----

    config.state_colors = [(0,0,0),(1,1,1),(0,1,0)] # black, white, green
    # config.num_generations = 150
    # config.grid_dims = (200,200)

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
