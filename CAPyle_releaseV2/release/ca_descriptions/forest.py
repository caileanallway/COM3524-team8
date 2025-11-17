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


def transition_func(grid, neighbourstates, neighbourcounts, wind_direction = 0):
    
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

    # properly unpack states
    town, water, dense_forest, canyon, chaparral, powerplant, incinerator, burning_dense_forest, burning_canyon, burning_chaparral, burned_dense_forest, burned_canyon, burned_chaparral, burned_town = neighbourcounts

    # unpack state counts for clarity
    #alive_neighbours, burning_neighbours, burned_neighbours= neighbourcounts
    alive_neighbours = town + water + dense_forest + canyon + chaparral
    
    # Powerplant and Incinerator considered burning neighbours for purposes of igniting surroundings
    burning_neighbours = burning_dense_forest + burning_canyon + burning_chaparral + powerplant + incinerator
    burned_neighbours = burned_dense_forest + burned_canyon + burned_chaparral + burned_town
    ### Town rules: Burns if at least one burning neighbour, else survives
    
    # if town and burning neighbours less than 1, survive
    town_survive = (burning_neighbours < 1) & (grid == 0)
    
    # if town has burning neighbours, become burned
    town_burned = (burning_neighbours >= 1) & (grid == 0)
   
    ### Water rules: Survives
    
    # if water, survives
    water_survive = (grid == 1)
    
    ### Dense forest rules: Low chance of igniting if burning neighbour, else survives
    
    # if dense forest, survive (ignition handled next so that survive is default)
    dense_forest_survive = (grid == 2)
    
    # if dense forest and burning neighbours >= 1, ignite with 10% chance per burning neighbour
    ignition_chance = 1 - (0.9 ** burning_neighbours)
    random_values = np.random.rand(*grid.shape)
    dense_forest_ignite = (random_values < ignition_chance) & (burning_neighbours >= 1) & (grid == 2)
    
    ### Canyon rules: High chance of igniting if burning neighbour, else survives
    
    # if canyon, survive (ignition handled next so that survive is default)
    canyon_survive = (grid == 3)
    
    # if canyon and burning neighbours >= 1, ignite with 70% chance per burning neighbour
    ignition_chance = 1 - (0.3 ** burning_neighbours)
    random_values = np.random.rand(*grid.shape)
    canyon_ignite = (random_values < ignition_chance) & (burning_neighbours >= 1) & (grid == 3)
    
    ### Chaparral rules: Medium chance of igniting if burning neighbour, else survives
    
    # if chaparral, survive (ignition handled next so that survive is default)
    chaparral_survive = (grid == 4)
    
    # if chaparral and burning neighbours >= 1, ignite with 40% chance per burning neighbour
    ignition_chance = 1 - (0.6 ** burning_neighbours)
    random_values = np.random.rand(*grid.shape)
    chaparral_ignite = (random_values < ignition_chance) & (burning_neighbours >= 1) & (grid == 4)
    
    ### Powerplant rules: Survives
    
    # if powerplant, survives
    powerplant_survive = (grid == 5)
    
    ### Incinerator rules: Survives

    # if incinerator, survives
    incinerator_survive = (grid == 6)

    ### Burning dense forest rules: Small chance to burn out to become burned dense forest, else survives
    
    # if burning dense forest, survive (burnout handled next so that survive is default)
    burning_dense_forest_survive = (grid == 7)
    
    # if burning dense forest, 10% chance to burn out
    random_values = np.random.rand(*grid.shape)
    burning_dense_forest_burnout = (random_values < 0.1) & (grid == 7)
    
    ### Burning canyon rules: High chance to burn out to become burned canyon, else survives
    
    # if burning canyon, survive (burnout handled next so that survive is default)
    burning_canyon_survive = (grid == 8)
    
    # if burning canyon, 80% chance to burn out
    random_values = np.random.rand(*grid.shape)
    burning_canyon_burnout = (random_values < 0.8) & (grid == 8)
    
    ### Burning chaparral rules: Medium chance to burn out to become burned chaparral, else survives
    
    # if burning chaparral, survive (burnout handled next so that survive is default)
    burning_chaparral_survive = (grid == 9)
    
    # if burning chaparral, 40% chance to burn out
    random_values = np.random.rand(*grid.shape)
    burning_chaparral_burnout = (random_values < 0.4) & (grid == 9)
    
    ### Burned dense forest rules: survives
    
    # if burned dense forest, survives
    burned_dense_forest_survive = (grid == 10)
    
    ### Burned canyon rules: survives
    
    # if burned canyon, survives
    burned_canyon_survive = (grid == 11)
    
    ### Burned chaparral rules: survives
    
    # if burned chaparral, survives
    burned_chaparral_survive = (grid == 12)
    
    ### Burned town rules: survives
    
    # if burned town, survives
    burned_town_survive = (grid == 13)
    
    ######################################################################################
    
    
    # Set all cells to 0 as fallback
    grid[:, :] = 0
    
    ### Town rules: Burns if at least one burning neighbour, else survives

    # Set cells to 0 where town survives
    grid[town_survive] = 0
    
    # Set cells to 13 where town burns
    grid[town_burned] = 13
    
    ### Water rules: Survives
    
    # Set cells to 1 where water survives
    grid[water_survive] = 1
    
    ### Dense forest rules: Low chance of igniting if burning neighbour, else survives

    # Set cells to 2 where dense forest survives
    grid[dense_forest_survive] = 2
    
    # Set cells to 7 where dense forest ignites
    grid[dense_forest_ignite] = 7
    
    ### Canyon rules: High chance of igniting if burning neighbour, else survives
    
    # Set cells to 3 where canyon survives
    grid[canyon_survive] = 3
    
    # Set cells to 8 where canyon ignites
    grid[canyon_ignite] = 8
    
    ### Chaparral rules: Medium chance of igniting if burning neighbour, else survives
    
    # Set cells to 4 where chaparral survives
    grid[chaparral_survive] = 4
    
    # Set cells to 9 where chaparral ignites
    grid[chaparral_ignite] = 9
    
    ### Powerplant rules: Survives
    
    # Set cells to 5 where powerplant survives
    grid[powerplant_survive] = 5
    
    ### Incinerator rules: Survives
    
    # Set cells to 6 where incinerator survives
    grid[incinerator_survive] = 6

    # Set cells to 0 where sick cells die of isolation or sickness
    #grid[isolation_death | sickness_death] = 0

    ### Burning dense forest rules: Small chance to burn out to become burned dense forest, else survives
    
    # Set cells to 7 where burning dense forest survives
    grid[burning_dense_forest_survive] = 7
    
    # Set cells to 10 where burning dense forest burns out
    grid[burning_dense_forest_burnout] = 10
    
    ### Burning canyon rules: High chance to burn out to become burned canyon, else survives
    
    # Set cells to 8 where burning canyon survives
    grid[burning_canyon_survive] = 8
    
    # Set cells to 11 where burning canyon burns out
    grid[burning_canyon_burnout] = 11
    
    ### Burning chaparral rules: Medium chance to burn out to become burned chaparral, else survives
    
    # Set cells to 9 where burning chaparral survives
    grid[burning_chaparral_survive] = 9
    
    # Set cells to 12 where burning chaparral burns out
    grid[burning_chaparral_burnout] = 12
    
    ### Burned dense forest rules: survives
    
    # Set cells to 10 where burned dense forest survives
    grid[burned_dense_forest_survive] = 10

    ### Burned canyon rules: survives
    
    # Set cells to 11 where burned canyon survives
    grid[burned_canyon_survive] = 11
    
    ### Burned chaparral rules: survives
    
    # Set cells to 12 where burned chaparral survives
    grid[burned_chaparral_survive] = 12
    
    ### Burned town rules: survives
    
    # Set cells to 13 where burned town survives
    grid[burned_town_survive] = 13
    
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
